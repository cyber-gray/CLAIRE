import os
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time, get_date_info, get_world_clocks
from tools.reg_search import reg_search, list_available_frameworks
from tools.risk_score import assess_ai_risk, quick_risk_check
from tools.checklist_gen import generate_compliance_checklist, export_checklist, list_checklist_templates
from tools.news import get_ai_policy_news, get_general_news
from tools.weather import get_current_weather, get_weather_forecast 
import pygame
import io
import threading
import queue 

load_dotenv()

MIC_INDEX = 1  # MacBook Pro Microphone (corrected from speakers)
TRIGGER_WORD = "claire"
CONVERSATION_TIMEOUT = 45  # seconds of inactivity before exiting conversation mode

# Global flags for interruption and exit
interrupt_speech = False
exit_session = False
speech_queue = queue.Queue()

logging.basicConfig(level=logging.DEBUG) # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Improve speech recognition settings
recognizer.energy_threshold = 300  # Lower threshold for better sensitivity
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.2  # Longer pause before considering speech complete (was 0.8)

def initialize_llm():
    """Initialize LLM based on available configuration"""
    # Try Azure OpenAI first (best quality)
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if azure_api_key and azure_endpoint and azure_deployment:
        logging.info("🔵 Using Azure OpenAI")
        return AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            api_key=azure_api_key,
            temperature=0.1
        )
    
    # Fallback to regular OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        logging.info("🟢 Using OpenAI")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            organization=os.getenv("OPENAI_ORG_ID"),
            temperature=0.1
        )
    
    # Final fallback to Ollama (local)
    logging.info("🟡 Using Ollama (local)")
    return ChatOllama(model="llama3.2:latest", reasoning=False, temperature=0.1)

# Initialize LLM
llm = initialize_llm()

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

# Tool list
tools = [
    get_time,
    get_date_info,
    get_world_clocks,
    reg_search,
    list_available_frameworks,
    assess_ai_risk,
    quick_risk_check,
    generate_compliance_checklist,
    export_checklist,
    list_checklist_templates,
    get_ai_policy_news,
    get_general_news,
    get_current_weather,
    get_weather_forecast
]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are CLAIRE (Compliance & Legal AI Risk Engine), an expert AI governance and compliance assistant. 

CORE MISSION: Help organizations navigate complex AI regulations, frameworks, and risk assessments with precision and clarity.

CAPABILITIES:
- AI compliance guidance (Canada's AIDA, EU AI Act, NIST AI RMF, OECD principles, ISO standards)
- Risk assessments and scoring
- Compliance checklist generation
- Real-time AI policy news monitoring
- General assistance (weather, time, news)

COMMUNICATION STYLE:
- Professional yet accessible and conversational
- Always cite sources when referencing regulatory content
- Provide clear risk assessments and actionable recommendations
- Prioritize accuracy over speed
- When uncertain, clearly state limitations and suggest consulting legal counsel

VOICE INTERACTION GUIDELINES:
- Keep responses brief and conversational (1-2 sentences per point max)
- Summarize news with just: headline and key point
- Skip URLs, formatting, and "read more" references entirely
- Use casual language: "I found 3 news stories" instead of formal lists
- Speak naturally as if talking to a colleague

CONVERSATIONAL ENGAGEMENT:
- Ask clarifying questions when requests are genuinely vague or incomplete
- Use follow-up questions sparingly and only when truly needed for clarity
- Prefer statements over questions for voice interactions
- When asking questions, keep them simple and direct
- Avoid multiple questions in one response
- Focus on providing complete, helpful answers first

RESPONSE STRUCTURE:
1. Provide the core answer concisely and completely
2. Only ask follow-up if critical information is missing
3. Keep total response under 2-3 sentences for voice interactions

CONTEXT AWARENESS:
- You can access real-time news about AI policy and regulations
- You can check weather and time for better user experience
- You maintain conversation context across interactions
- You understand both technical and business stakeholder needs

Remember: You're not just providing information - you're having a professional conversation to truly help solve their compliance challenges."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# TTS setup
def speak_text(text: str):
    try:
        # Clean text for better voice output
        voice_text = clean_text_for_voice(text)
        
        # Always use ElevenLabs for natural voice (with fallback only if it fails)
        if not use_elevenlabs_tts(voice_text):
            logging.warning("🟡 ElevenLabs failed, no fallback to maintain voice quality")
        
    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")

def speak_filler_response(query_type: str = "general"):
    """Speak an immediate filler response while processing the actual query"""
    filler_responses = {
        "search": [
            "Let me search through the regulations for you.",
            "I'll look that up in the compliance database.",
            "Give me a moment to find the relevant information.",
            "Let me dig into the regulatory framework for that."
        ],
        "risk": [
            "Let me assess that risk for you.",
            "I'll run through the risk analysis framework.",
            "Give me a second to evaluate the compliance implications.",
            "Let me check the risk factors for that scenario."
        ],
        "news": [
            "Let me check the latest AI policy updates.",
            "I'll pull the most recent regulatory news.",
            "Give me a moment to gather the latest information.",
            "Let me see what's happening in AI governance today."
        ],
        "checklist": [
            "I'll generate that compliance checklist for you.",
            "Let me create a customized checklist.",
            "Give me a moment to compile the requirements.",
            "I'll put together those compliance steps for you."
        ],
        "weather": [
            "Let me check the weather for you.",
            "I'll get the current conditions.",
            "Give me a second to pull the weather data."
        ],
        "general": [
            "Sure, give me one moment while I look that up.",
            "Let me help you with that.",
            "I'll check on that for you right away.",
            "Give me just a second to process that.",
            "Great question, let me find that information."
        ]
    }
    
    import random
    response = random.choice(filler_responses.get(query_type, filler_responses["general"]))
    
    # Use ElevenLabs for filler too (it's short so should be faster)
    if not use_elevenlabs_tts(response):
        logging.warning("🟡 Filler response failed")

def determine_query_type(query: str) -> str:
    """Determine the type of query to select appropriate filler response"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['search', 'find', 'regulation', 'framework', 'standard']):
        return "search"
    elif any(word in query_lower for word in ['risk', 'assess', 'score', 'evaluation']):
        return "risk"
    elif any(word in query_lower for word in ['news', 'update', 'policy', 'latest']):
        return "news"
    elif any(word in query_lower for word in ['checklist', 'compliance', 'requirements']):
        return "checklist"
    elif any(word in query_lower for word in ['weather', 'temperature', 'forecast']):
        return "weather"
    else:
        return "general"

def check_for_interruption():
    """Background thread to listen for interruption while speaking"""
    global interrupt_speech, exit_session
    
    temp_recognizer = sr.Recognizer()
    temp_recognizer.energy_threshold = 2000  # Much higher threshold to avoid self-interruption
    temp_recognizer.dynamic_energy_threshold = False  # Disable adaptive threshold
    temp_recognizer.pause_threshold = 2.0  # Much longer pause required before considering speech
    
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            while True:
                try:
                    # Quick listen for interruption with stricter settings
                    audio = temp_recognizer.listen(source, timeout=1.0, phrase_time_limit=5)  # Longer phrase limit
                    transcript = temp_recognizer.recognize_google(audio).lower()
                    
                    # Filter out likely self-speech patterns
                    self_speech_indicators = [
                        "hello i'm claire",
                        "let me check",
                        "give me a moment",
                        "i'll look that up",
                        "sure give me",
                        "sounds good",
                        "let me help",
                        "i found",
                        "here's what",
                        "does that help",
                        "what else can",
                        "would you like",
                        "let me dig into",
                        "great question",
                        "let me see what's",
                        "are you referring",
                        "could you provide",
                        "any clarification",
                        "dive deeper into",
                        "what specific",
                        "need more details",
                        "want me to explain",
                        "help you with",
                        "more context about",
                        "which aspect",
                        "tell me more about",
                        "what would you like",
                        "anything else",
                        "follow up",
                        "clarify",
                        "highlights concerns",
                        "discusses china",
                        "ai ambitions",
                        "efficiency proposals",
                        "ai leadership",
                        "datacenter operators",
                        "cybersecurity in ai",
                        "ai systems",
                        "ai governance",
                        "compliance needs",
                        "regulatory",
                        "frameworks",
                        "risk assessment"
                    ]
                    
                    # Skip if it sounds like CLAIRE's own speech
                    if any(indicator in transcript for indicator in self_speech_indicators):
                        logging.debug(f"🔇 Ignoring self-speech: {transcript}")
                        continue
                    
                    # Only process if it's a clear user interruption
                    if len(transcript.strip()) > 3:  # Must be substantial
                        # Check for exit commands
                        exit_phrases = [
                            "that's all for now",
                            "that's all thanks", 
                            "thanks that's all",
                            "goodbye claire",
                            "exit",
                            "stop session",
                            "end session",
                            "that's enough"
                        ]
                        
                        if any(phrase in transcript for phrase in exit_phrases):
                            logging.info(f"🚪 Exit command detected: {transcript}")
                            exit_session = True
                            interrupt_speech = True
                            break
                        
                        # Check for clear user interruption (very specific words only)
                        user_interruption_words = [
                            "wait wait", "stop stop", "excuse me", "hold on", 
                            "interrupt", "pause", "one moment", "actually wait"
                        ]
                        
                        # Must be a very clear interruption phrase, not just any speech
                        is_clear_interruption = any(word in transcript for word in user_interruption_words)
                        
                        if is_clear_interruption:
                            logging.info(f"⏸️ User interruption detected: {transcript}")
                            interrupt_speech = True
                            speech_queue.put(transcript)
                        else:
                            logging.debug(f"🔇 Ignoring unclear audio: {transcript}")
                        
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    logging.debug(f"Interruption detection error: {e}")
                    continue
                    
    except Exception as e:
        logging.error(f"❌ Interruption thread error: {e}")

def is_exit_command(text: str) -> bool:
    """Check if the text contains an exit command"""
    text_lower = text.lower()
    exit_phrases = [
        "that's all for now",
        "that's all thanks", 
        "thanks that's all",
        "goodbye claire",
        "exit",
        "stop session", 
        "end session",
        "that's enough",
        "bye claire"
    ]
    return any(phrase in text_lower for phrase in exit_phrases)

def use_elevenlabs_tts(text: str) -> bool:
    """Use ElevenLabs for natural speech synthesis with interruption support"""
    global interrupt_speech
    
    try:
        from elevenlabs.client import ElevenLabs
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            logging.warning("🟡 ElevenLabs API key not found, using fallback")
            return False
        
        client = ElevenLabs(api_key=api_key)
        
        # Generate speech with Hope voice (optimized for lower latency)
        audio = client.text_to_speech.convert(
            voice_id="uYXf8XasLslADfZ2MB4u",  # Hope - Your Conversational Bestie
            text=text,
            model_id="eleven_turbo_v2_5",  # Faster model
            voice_settings={
                "stability": 0.5,  # Lower for faster processing
                "similarity_boost": 0.3,  # Lower for speed
                "style": 0.0,
                "use_speaker_boost": False  # Disable for speed
            }
        )
        
        # Initialize pygame mixer for playback control
        pygame.mixer.init()
        
        # Convert audio to bytes and load into pygame
        audio_bytes = b''.join(audio)
        audio_io = io.BytesIO(audio_bytes)
        
        # Reset interrupt flag before starting
        interrupt_speech = False
        
        # Only enable interruption for longer responses (avoid self-interruption on short responses)
        enable_interruption = len(text) > 100  # Only for responses longer than 100 characters
        interrupt_thread = None
        
        if enable_interruption:
            # Wait a moment before starting interruption detection to avoid picking up our own voice
            time.sleep(0.5)  # Give CLAIRE's voice time to start playing
            # Start interruption detection in background
            interrupt_thread = threading.Thread(target=check_for_interruption, daemon=True)
            interrupt_thread.start()
            logging.debug("🎧 Interruption detection enabled")
        
        # Play audio with optional interruption capability
        pygame.mixer.music.load(audio_io)
        pygame.mixer.music.play()
        
        # Monitor for interruption while playing (only if enabled)
        while pygame.mixer.music.get_busy():
            if enable_interruption and interrupt_speech:
                pygame.mixer.music.stop()
                logging.info("🛑 Speech interrupted by user")
                break
            time.sleep(0.1)
        
        logging.info("🎙️ Used ElevenLabs TTS")
        return True
        
    except Exception as e:
        logging.warning(f"⚠️ ElevenLabs TTS failed: {e}, using fallback")
        return False

def use_system_tts(text: str):
    """Fallback to system TTS"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Use Samantha (most natural macOS voice)
        for voice in voices:
            if 'samantha' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Natural speech settings
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.95)
        engine.say(text)
        engine.runAndWait()
        logging.info("🔊 Used system TTS")
        
    except Exception as e:
        logging.error(f"❌ System TTS failed: {e}")

def clean_text_for_voice(text: str) -> str:
    """Clean text to make it more suitable for voice output"""
    import re
    
    # Remove URLs and "Read more" links
    text = re.sub(r'\[Read more\]\([^)]+\)', '', text)
    text = re.sub(r'https?://[^\s\]]+', '', text)
    
    # Remove markdown formatting but keep the content
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
    text = re.sub(r'`([^`]+)`', r'\1', text)        # Code
    
    # Simplify news format - remove bullets and formatting
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)  # Remove numbered lists
    text = re.sub(r'^\s*[-*]\s*', '', text, flags=re.MULTILINE)  # Remove bullets
    
    # Clean up extra whitespace and newlines
    text = re.sub(r'\n+', '. ', text)  # Replace newlines with periods
    text = re.sub(r'\s+', ' ', text)   # Collapse multiple spaces
    text = text.strip()
    
    return text

# Main interaction loop
def write():
    global interrupt_speech, exit_session, speech_queue
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            print("🎤 Adjusting for ambient noise... (speak now to test)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"✅ Ready! Energy threshold: {recognizer.energy_threshold}")
            print(f"🗣️  Say '{TRIGGER_WORD}' to activate CLAIRE")
            print("💡 You can interrupt CLAIRE while speaking or say 'That's all for now, thanks' to exit")
            
            while not exit_session:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 CLAIRE activated by: {transcript}")
                            speak_text("Hello, I'm CLAIRE. How can I assist with your compliance needs?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        # Also check for common misheard variations
                        elif any(word in transcript.lower() for word in ['eclair', 'clear', 'clair', 'clere']):
                            logging.info(f"🗣 CLAIRE activated by variation: {transcript}")
                            speak_text("Hello, I'm CLAIRE. How can I assist with your compliance needs?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        # Check if there's an interruption in the queue first
                        command = None
                        try:
                            command = speech_queue.get_nowait()
                            logging.info(f"📥 Processing interruption: {command}")
                        except queue.Empty:
                            # No interruption, listen normally with longer timeout for complete questions
                            logging.info("🎤 Listening for next command...")
                            audio = recognizer.listen(source, timeout=2, phrase_time_limit=15)  # Extended time for full questions
                            command = recognizer.recognize_google(audio)
                            logging.info(f"📥 Command: {command}")

                        # Check for exit command
                        if is_exit_command(command):
                            logging.info("🚪 Exit command received")
                            speak_text("Thank you for using CLAIRE. Have a great day!")
                            exit_session = True
                            break

                        # Immediately give a filler response while processing
                        query_type = determine_query_type(command)
                        speak_filler_response(query_type)
                        
                        # Reset interrupt flag before processing
                        interrupt_speech = False

                        logging.info("🤖 Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        
                        # Clean up response by removing thinking tags
                        if "<think>" in content and "</think>" in content:
                            # Extract everything before <think> and after </think>
                            before_think = content.split("<think>")[0].strip()
                            after_think = content.split("</think>")[-1].strip()
                            content = (before_think + " " + after_think).strip()
                        
                        logging.info(f"✅ CLAIRE responded: {content}")

                        print("CLAIRE:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("⚠️ Timeout waiting for audio.")
                    if conversation_mode and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("⌛ No input in conversation mode. Returning to wake word mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")
    
    finally:
        print("👋 CLAIRE session ended. Goodbye!")
        pygame.mixer.quit()

if __name__ == "__main__":
    write()
