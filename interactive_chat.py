#!/usr/bin/env python
"""
Interactive Financial Chat Interface for FundWise NLP
This script provides a simple command-line interface for users to ask questions
about stocks and financial news. It uses the MockNLPProcessor to avoid API rate limits.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path so we can import the fundwise package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fundwise.nlp.mock_nlp import MockNLPProcessor

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
    print("\n" + "=" * 60)
    print("                FundWise Financial Chat")
    print("         Ask questions about stocks and markets")
    print("=" * 60)
    print("Type 'exit', 'quit', or 'q' to end the session")
    print("Type 'help' for sample questions")
    print("-" * 60 + "\n")

def print_help():
    """Print sample questions that users can ask"""
    print("\nSample questions you can ask:")
    print("  - Why is TSLA up today?")
    print("  - What's happening with AAPL?")
    print("  - Give me the latest news on AMZN")
    print("  - Should I invest in MSFT?")
    print("  - What's the sentiment around NFLX?")
    print("-" * 60 + "\n")

def main():
    """Run the interactive chat interface"""
    # Initialize the NLP processor
    print("Initializing FundWise NLP system...")
    processor = MockNLPProcessor()
    
    # Load sample articles
    print("Loading financial news articles...")
    articles = get_sample_articles()
    for article in articles:
        processor.process_article(article)
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
        
        # Extract symbols from the question
        symbols = processor.extract_symbols(user_input)
        if symbols:
            print(f"Detected stock symbols: {', '.join(symbols)}")
        
        # Get answer
        answer = processor.answer_question(user_input)
        print(f"\nAnswer: {answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main() 