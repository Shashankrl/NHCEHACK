#!/usr/bin/env python
"""
Advanced Interactive Financial Chat Interface for FundWise NLP
This script provides a command-line interface for users to ask questions
about stocks and financial news. It tries to use the Gemini API-powered
ChatbotNLP first, with automatic fallback to MockNLPProcessor if API issues arise.
"""
import sys
import os
import time
from datetime import datetime
import traceback
from typing import Dict, Any, List

# Add parent directory to path so we can import the fundwise package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FundWise components
from fundwise.nlp.chatbot_nlp import ChatbotNLP
from fundwise.nlp.mock_nlp import MockNLPProcessor
from fundwise.nlp.news_processor import NewsProcessor

def load_environment_variables():
    """Try to load environment variables from .env file"""
    try:
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        os.environ[key] = value
            print("Environment variables loaded from .env file")
        return True
    except Exception as e:
        print(f"Error loading .env file: {e}")
        return False

def get_sample_articles():
    """Return some sample financial news articles for demo purposes"""
    return [
        {
            'title': 'Tesla Reports Strong Q2 Earnings',
            'content': 'Tesla Inc. reported Q2 earnings that beat analyst expectations, with revenue increasing 47% year-over-year. The company cited strong demand for the Model Y and improved production efficiency at its factories. CEO Elon Musk announced plans to accelerate the rollout of Full Self-Driving technology.',
            'source': 'Bloomberg',
            'date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'title': 'Apple Faces Supply Chain Issues',
            'content': 'Apple is experiencing supply chain constraints for its iPhone production. Analysts estimate this could impact sales during the holiday quarter. The company is reportedly working with suppliers to increase production capacity.',
            'source': 'Wall Street Journal',
            'date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'title': 'Microsoft Cloud Business Growth Slows',
            'content': 'Microsoft reported its Q2 results with Azure growth declining to 26% from 31% in the previous quarter. The company still beat revenue expectations but investors are concerned about the cloud division slowdown.',
            'source': 'CNBC',
            'date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'title': 'Amazon Prime Day Sets New Sales Record',
            'content': 'Amazon announced that its Prime Day event set a new sales record with over 300 million items sold worldwide. The company saw strong demand for electronics and household essentials.',
            'source': 'Reuters',
            'date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'title': 'Netflix Subscriber Growth Exceeds Expectations',
            'content': 'Netflix reported adding 5.9 million subscribers in the latest quarter, significantly higher than the 2.3 million expected by analysts. The streaming giant credited its password-sharing crackdown and strong content lineup for the growth.',
            'source': 'Variety',
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    ]

def print_banner():
    """Print a welcome banner"""
    print("\n" + "=" * 70)
    print("                    FundWise Advanced Financial Chat")
    print("             Ask questions about stocks, markets, and trends")
    print("=" * 70)
    print("Type 'exit', 'quit', or 'q' to end the session")
    print("Type 'help' for sample questions")
    print("-" * 70 + "\n")

def print_help():
    """Print sample questions that users can ask"""
    print("\nSample questions you can ask:")
    print("  - Why is TSLA up today?")
    print("  - What's happening with AAPL?")
    print("  - Give me the latest news on AMZN")
    print("  - Should I invest in MSFT?")
    print("  - What's the sentiment around NFLX?")
    print("  - Explain recent market movements")
    print("  - How are tech stocks performing?")
    print("-" * 70 + "\n")

def initialize_nlp_system():
    """Initialize the NLP system with advanced chatbot and fallback"""
    print("Initializing FundWise NLP system...")
    
    # Try to load Gemini API key from environment
    load_environment_variables()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Initialize processors
    advanced_processor = None
    mock_processor = MockNLPProcessor()
    news_processor = None
    
    # First try to initialize the advanced processor
    if api_key:
        try:
            print("Gemini API key found. Initializing advanced NLP processor...")
            advanced_processor = ChatbotNLP(gemini_api_key=api_key)
            news_processor = NewsProcessor(gemini_api_key=api_key)
            print("Advanced NLP processor initialized successfully")
        except Exception as e:
            print(f"Error initializing advanced NLP processor: {e}")
            print("Falling back to mock processor")
            advanced_processor = None
    else:
        print("No Gemini API key found. Using mock processor")
    
    # Return both processors
    return {
        "advanced": advanced_processor,
        "mock": mock_processor,
        "news": news_processor
    }

def process_with_fallback(processors, question):
    """Process a question with automatic fallback"""
    advanced = processors.get("advanced")
    mock = processors.get("mock")
    
    # Try with advanced processor first if available
    if advanced:
        try:
            start_time = time.time()
            print("Using advanced NLP processor...")
            response = advanced.process_query(question)
            processing_time = time.time() - start_time
            print(f"Processing completed in {processing_time:.2f} seconds")
            return response.get("text", ""), response.get("detected_symbols", []), response.get("intent", "")
        except Exception as e:
            print(f"Error with advanced processor: {e}")
            print("Falling back to mock processor")
    
    # Fallback to mock processor
    print("Using mock processor...")
    symbols = mock.extract_symbols(question)
    answer = mock.answer_question(question)
    return answer, symbols, "UNKNOWN"

def main():
    """Run the interactive chat interface"""
    # Initialize the NLP system
    processors = initialize_nlp_system()
    
    # Load sample articles into the mock processor
    print("Loading financial news articles...")
    articles = get_sample_articles()
    for article in articles:
        processors["mock"].process_article(article)
    
    # If we have the news processor, load articles there too
    if processors["news"]:
        for article in articles:
            processors["news"].process_article(article)
    
    print(f"Loaded {len(articles)} financial news articles")
    
    # Print welcome banner
    print_banner()
    
    # Main chat loop
    while True:
        # Get user input
        try:
            user_input = input("\nAsk a question about stocks or financial news: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting FundWise Chat. Goodbye!")
            break
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Exiting FundWise Chat. Goodbye!")
            break
        
        # Check for help command
        if user_input.lower() == 'help':
            print_help()
            continue
        
        # Skip empty input
        if not user_input.strip():
            continue
        
        # Process the user's question
        print("\nAnalyzing your question...")
        
        try:
            # Process with automatic fallback
            answer, symbols, intent = process_with_fallback(processors, user_input)
            
            # Display detected symbols if any
            if symbols:
                print(f"Detected stock symbols: {', '.join(symbols)}")
            
            # Display intent if available
            if intent and intent != "UNKNOWN":
                print(f"Question intent: {intent}")
            
            # Display the answer
            print(f"\nAnswer: {answer}\n")
            print("-" * 70)
            
        except Exception as e:
            print(f"Error processing question: {e}")
            traceback.print_exc()
            print("Please try again with a different question")

if __name__ == "__main__":
    main() 