"""
Test script for the FundWise NLP components
"""
import os
from dotenv import load_dotenv
from summarizer.gemini_summarizer import GeminiSummarizer
from summarizer.news_processor import NewsProcessor
from summarizer.chatbot_nlp import ChatbotNLP

# Load environment variables (including API key)
load_dotenv()

def test_gemini_summarizer():
    """Test the Gemini summarizer component"""
    print("\n===== Testing GeminiSummarizer =====")
    
    # Initialize summarizer
    summarizer = GeminiSummarizer()
    
    # Test article text
    test_article = """
    Apple Inc. reported better-than-expected quarterly earnings on Thursday, with iPhone sales
    rising 6% year-over-year. The tech giant posted revenue of $94.8 billion for the quarter, 
    exceeding analyst expectations of $92.9 billion. CEO Tim Cook highlighted strong performance 
    in emerging markets, particularly India, where sales reached a new all-time high.
    
    However, the company's services segment, which includes Apple Music, iCloud, and the App Store,
    showed slower growth than in previous quarters. Apple's stock rose 3.5% in after-hours trading
    following the announcement.
    """
    
    print("\nTesting article summarization...")
    summary = summarizer.summarize_article(test_article)
    print(f"Summary: {summary}")
    
    print("\nTesting sentiment analysis...")
    sentiment = summarizer.analyze_sentiment(test_article)
    print(f"Sentiment: {sentiment['label']}")
    print(f"Score: {sentiment['score']}")
    print(f"Factors: {sentiment['factors']}")
    
    print("\nTesting stock symbol extraction...")
    symbols = summarizer.extract_stock_symbols(test_article)
    print(f"Extracted symbols: {symbols}")

def test_news_processor():
    """Test the news processor component"""
    print("\n===== Testing NewsProcessor =====")
    
    # Initialize news processor
    processor = NewsProcessor()
    
    # Create test articles
    test_articles = [
        {
            "title": "Tesla Beats Q1 Delivery Estimates",
            "content": "Tesla Inc. delivered more vehicles than expected in the first quarter, despite challenges in the EV market. The company announced 422,875 deliveries, surpassing analyst estimates of 420,000.",
            "source": "Market News",
            "date": "2023-04-02"
        },
        {
            "title": "Microsoft Cloud Revenue Surges",
            "content": "Microsoft reported strong cloud growth in its latest earnings, with Azure revenue increasing 27% year-over-year. The company's stock rose 5% following the announcement.",
            "source": "Tech Daily",
            "date": "2023-04-25"
        }
    ]
    
    print("\nProcessing test articles...")
    processed = processor.batch_process_articles(test_articles)
    
    print("\nTest article #1 results:")
    print(f"Title: {processed[0]['title']}")
    print(f"Summary: {processed[0]['summary']}")
    print(f"Sentiment: {processed[0]['sentiment']['label']}")
    print(f"Detected symbols: {processed[0]['related_symbols']}")
    
    # Test finding articles by symbol
    print("\nFinding articles by symbol 'TSLA'...")
    tesla_articles = processor.find_articles_by_symbol("TSLA")
    print(f"Found {len(tesla_articles)} articles about Tesla")

def test_chatbot():
    """Test the chatbot component"""
    print("\n===== Testing ChatbotNLP =====")
    
    # Initialize chatbot
    chatbot = ChatbotNLP()
    
    # Test queries
    test_queries = [
        "Why is Apple stock up today?",
        "Tell me the latest news about Tesla",
        "What's happening in the tech sector?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = chatbot.process_query(query)
        print(f"Intent: {response['intent']}")
        print(f"Detected symbols: {response['detected_symbols']}")
        print(f"Response: {response['text'][:150]}...")

def main():
    """Main test function"""
    print("Starting FundWise NLP tests...")
    
    try:
        # Test Gemini summarizer
        test_gemini_summarizer()
        
        # Test news processor
        test_news_processor()
        
        # Test chatbot
        test_chatbot()
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        print("Please make sure your GEMINI_API_KEY is set correctly in the .env file")

if __name__ == "__main__":
    main() 