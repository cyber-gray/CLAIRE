import os
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time
from tools.reg_search import reg_search, list_available_frameworks
from tools.risk_score import assess_ai_risk, quick_risk_check
from tools.checklist_gen import generate_compliance_checklist, export_checklist, list_checklist_templates 

load_dotenv()

MIC_INDEX = 2  # MacBook Pro Microphone
TRIGGER_WORD = "claire"
CONVERSATION_TIMEOUT = 45  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG) # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize LLM
llm = ChatOllama(model="llama3.2:latest", reasoning=False)

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

# Tool list
tools = [
    get_time,
    reg_search,
    list_available_frameworks,
    assess_ai_risk,
    quick_risk_check,
    generate_compliance_checklist,
    export_checklist,
    list_checklist_templates
]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are CLAIRE (Compliance & Legal AI Risk Engine), an expert AI governance and compliance assistant. Your mission is to help organizations navigate complex AI regulations, frameworks, and risk assessments with precision and clarity. You provide authoritative guidance on AI compliance matters including EU AI Act, NIST AI RMF, OECD principles, and ISO standards. Always cite sources when referencing regulatory content, provide clear risk assessments, and offer actionable compliance recommendations. Keep responses professional yet accessible, and always prioritize accuracy over speed. When uncertain, clearly state limitations and suggest consulting legal counsel."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# TTS setup
def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        for voice in engine.getProperty('voices'):
            if "jamie" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")

# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 CLAIRE activated by: {transcript}")
                            speak_text("Hello, I'm CLAIRE. How can I assist with your compliance needs?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"📥 Command: {command}")

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

if __name__ == "__main__":
    write()
