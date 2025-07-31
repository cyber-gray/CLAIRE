#!/usr/bin/env python3
"""
CLAIRE Setup Script
Initializes corpus, tests APIs, and prepares CLAIRE for use
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add current directory to path
sys.path.append('.')

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_environment():
    """Check environment variables and API keys"""
    load_dotenv()
    
    print("🔍 Checking Environment Configuration...")
    
    # Check LLM configuration
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") 
    
    if azure_key and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("✅ Azure OpenAI configured")
    elif openai_key:
        print("✅ OpenAI configured")
    else:
        print("⚠️ No cloud LLM configured - will use Ollama (local)")
    
    # Check API keys
    news_key = os.getenv("NEWS_API_KEY")
    weather_key = os.getenv("WEATHER_API_KEY")
    
    print(f"📰 News API: {'✅ Configured' if news_key else '❌ Not configured'}")
    print(f"🌤️ Weather API: {'✅ Configured' if weather_key else '❌ Not configured'}")
    
    if not news_key:
        print("   Get a free key at: https://newsapi.org/register")
    if not weather_key:
        print("   Get a free key at: https://openweathermap.org/api")

def initialize_corpus():
    """Initialize the corpus with sample documents"""
    print("\n📚 Initializing AI Policy Corpus...")
    
    try:
        from utils.corpus_loader import setup_corpus_database
        
        vectorstore = setup_corpus_database(force_reload=False)
        if vectorstore:
            print("✅ Corpus database initialized successfully")
            
            # Test search
            try:
                results = vectorstore.similarity_search("high-risk AI systems", k=2)
                print(f"✅ Test search successful - found {len(results)} relevant chunks")
            except Exception as e:
                print(f"⚠️ Search test failed: {e}")
        else:
            print("❌ Failed to initialize corpus database")
            
    except Exception as e:
        print(f"❌ Error initializing corpus: {e}")
        print("   Make sure you have a 'corpus' folder with AI policy documents")

def test_tools():
    """Test CLAIRE's tools"""
    print("\n🛠️ Testing CLAIRE Tools...")
    
    try:
        # Test time tool
        from tools.time import get_time
        time_result = get_time.invoke({'city': 'local'})
        print(f"✅ Time Tool: {time_result}")
        
        # Test risk assessment
        from tools.risk_score import quick_risk_check
        risk_result = quick_risk_check.invoke({
            'system_description': 'chatbot for customer service'
        })
        print("✅ Risk Assessment Tool: Working")
        
        # Test news (if configured)
        news_key = os.getenv("NEWS_API_KEY")
        if news_key:
            from tools.news import get_ai_policy_news
            try:
                news_result = get_ai_policy_news.invoke({
                    'query': 'AI regulation',
                    'max_articles': 2
                })
                print("✅ News API: Working")
            except Exception as e:
                print(f"⚠️ News API test failed: {e}")
        
        # Test weather (if configured)
        weather_key = os.getenv("WEATHER_API_KEY")
        if weather_key:
            from tools.weather import get_current_weather
            try:
                weather_result = get_current_weather.invoke({'location': 'London'})
                print("✅ Weather API: Working")
            except Exception as e:
                print(f"⚠️ Weather API test failed: {e}")
                
    except Exception as e:
        print(f"❌ Tool testing failed: {e}")

def create_sample_env():
    """Create sample .env file if it doesn't exist"""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("\n📝 Creating sample .env file...")
        with open(env_path, 'w') as f:
            f.write("""# CLAIRE Environment Variables

# Azure OpenAI Configuration (Recommended for best quality)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# News API Configuration
NEWS_API_KEY=your_newsapi_key_here

# Weather API Configuration
WEATHER_API_KEY=your_openweather_api_key_here

# Optional: OpenAI Fallback
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ORG_ID=your_openai_org_id_here
""")
        print("✅ Created .env file - please add your API keys")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    setup_logging()
    
    print("🎯 CLAIRE (Compliance & Legal AI Risk Engine) Setup")
    print("=" * 60)
    
    # Create sample .env
    create_sample_env()
    
    # Check environment
    check_environment()
    
    # Initialize corpus
    initialize_corpus()
    
    # Test tools
    test_tools()
    
    print("\n" + "=" * 60)
    print("🎉 CLAIRE Setup Complete!")
    print("\n🚀 Next Steps:")
    print("1. Add your API keys to the .env file")
    print("2. Add AI policy documents to the 'corpus' folder")
    print("3. Run: python main.py")
    print("4. Say 'Hey CLAIRE' to activate voice mode")
    print("\n💡 For corpus setup, you can add:")
    print("   - EU AI Act PDF/text files")
    print("   - NIST AI RMF documents")
    print("   - ISO 42001 standards")
    print("   - Any other AI governance documents")

if __name__ == "__main__":
    main()
