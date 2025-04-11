"""
Comprehensive demonstration of all FundWise NLP components working together
"""
import os
import sys
# Add the project root to the path (for running the example directly)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not found, skipping .env loading")

from fundwise.nlp import MockNLPProcessor, NewsProcessor, ChatbotNLP
try:
    from fundwise.nlp import GeminiSummarizer
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

def main():
    """Run a comprehensive demonstration of all FundWise NLP components."""
    print("FundWise NLP Components - Comprehensive Demo")
    print("=" * 50)
    
    # Check if Gemini API key is available
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    
    if gemini_api_key and HAS_GEMINI:
        print("Gemini API key found. Using GeminiSummarizer.")
        # Initialize with Gemini
        summarizer = GeminiSummarizer(api_key=gemini_api_key)
        news_processor = NewsProcessor(gemini_api_key=gemini_api_key)
        chatbot = ChatbotNLP(gemini_api_key=gemini_api_key)
    else:
        print("No Gemini API key found or Gemini package not available.")
        print("Using MockNLPProcessor as fallback.")
        # Initialize with Mock processor
        summarizer = MockNLPProcessor()
        news_processor = None
        chatbot = None
    
    # Sample articles
    articles = [
        {
            'title': 'Tesla Reports Strong Q2 Earnings',
            'content': 'Tesla Inc. announced better than expected earnings for Q2 2023. Revenue increased by 47% year-over-year, beating analyst expectations. The company cited strong demand for Model Y and production improvements.',
            'source': 'Financial Times',
            'date': '2023-07-20'
        },
        {
            'title': 'Apple Faces Supply Chain Issues',
            'content': 'Apple is experiencing supply chain constraints for its iPhone production. The company warned that this could impact Q3 revenue. Analysts have lowered their expectations due to these concerns.',
            'source': 'Wall Street Journal',
            'date': '2023-07-15'
        },
        {
            'title': 'Microsoft Cloud Business Growth Slows',
            'content': 'Microsoft reported its Q2 results with Azure growth declining to 26% from 31% in the previous quarter. The slowdown in cloud growth has raised concerns among investors about the broader tech sector.',
            'source': 'Bloomberg',
            'date': '2023-07-18'
        }
    ]
    
    # PART 1: Basic NLP processing
    print("\nPART 1: BASIC NLP PROCESSING")
    print("-" * 50)
    
    # Process a single article
    print("Processing article with summarizer...")
    article = articles[0]  # Tesla article
    
    # Process the article
    result = summarizer.process_article(article)
    
    # Display results
    print(f"Title: {article['title']}")
    print(f"Summary: {result['summary']}")
    print(f"Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
    if 'factors' in result['sentiment']:
        print(f"Key factors: {', '.join(result['sentiment']['factors'])}")
    print(f"Related symbols: {', '.join(result['related_symbols'])}")
    
    # PART 2: News processing (if available)
    if news_processor:
        print("\nPART 2: NEWS PROCESSING")
        print("-" * 50)
        
        # Process all articles
        print("Processing all articles with news processor...")
        for article in articles:
            news_processor.process_article(article)
        
        # Find articles by symbol
        print("\nFinding articles by symbol:")
        tesla_articles = news_processor.find_articles_by_symbol("TSLA")
        print(f"Found {len(tesla_articles)} articles about TSLA")
        
        # Find articles by sentiment
        print("\nFinding articles by sentiment:")
        positive_articles = news_processor.find_articles_by_sentiment("Positive")
        negative_articles = news_processor.find_articles_by_sentiment("Negative")
        print(f"Positive articles: {len(positive_articles)}")
        print(f"Negative articles: {len(negative_articles)}")
        
        # Explain stock movement
        print("\nExplaining stock movement:")
        explanation = news_processor.explain_stock_movement("TSLA")
        print(f"TSLA explanation: {explanation}")
    
    # PART 3: Chatbot (if available)
    if chatbot:
        print("\nPART 3: CHATBOT NLP")
        print("-" * 50)
        
        # Process user queries
        print("Processing user queries with chatbot...")
        
        queries = [
            "Why is Tesla stock up today?",
            "What's the latest news on AAPL?",
            "Give me an overview of the market"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            response = chatbot.process_query(query)
            print(f"Intent: {response['intent']}")
            if response['detected_symbols']:
                print(f"Detected symbols: {', '.join(response['detected_symbols'])}")
            print(f"Response: {response['text']}")
    
    print("\nDemo completed.")

if __name__ == "__main__":
    main() 