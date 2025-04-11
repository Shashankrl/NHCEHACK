"""
Test script to run the NLP components for FundWise
"""
import os
from dotenv import load_dotenv
from summarizer.gemini_summarizer import GeminiSummarizer
from summarizer.news_processor import NewsProcessor
from summarizer.chatbot_nlp import ChatbotNLP

# Load environment variables
load_dotenv()

def main():
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in environment or .env file.")
        print("Please set your API key before running.")
        return
    
    print("=== Testing FundWise NLP Components ===")
    
    # Initialize components
    print("Initializing NLP components...")
    summarizer = GeminiSummarizer(api_key=api_key)
    processor = NewsProcessor(gemini_api_key=api_key)
    chatbot = ChatbotNLP(gemini_api_key=api_key)
    
    # Test article
    test_article = {
        "title": "Apple Reports Record Q1 Revenue as iPhone Sales Surge",
        "content": """
        Apple Inc. reported record-breaking first-quarter revenue on Tuesday, 
        with iPhone sales surging 17% year-over-year. The tech giant posted 
        revenue of $123.9 billion, exceeding analyst expectations of $118.7 billion.
        
        CEO Tim Cook attributed the strong performance to robust demand in emerging 
        markets and the successful launch of the iPhone 15 series. The company also 
        reported growth in its services segment, which includes Apple Music, iCloud, 
        and the App Store.
        
        However, supply chain constraints continue to impact the availability of certain products, 
        particularly MacBooks and iPads, which saw modest sales declines compared to the same 
        period last year.
        """,
        "source": "Financial News Daily",
        "date": "2023-11-15"
    }
    
    # Process the article
    print("\n1. Processing a sample article...")
    processed_article = processor.process_article(test_article)
    
    print(f"  Title: {processed_article['title']}")
    print(f"  Summary: {processed_article['summary']}")
    print(f"  Sentiment: {processed_article['sentiment']['label']} (Score: {processed_article['sentiment']['score']})")
    print(f"  Detected symbols: {processed_article['related_symbols']}")
    
    # Test question answering
    print("\n2. Testing question answering...")
    test_questions = [
        "Why is Apple stock up today?",
        "What's happening with tech stocks?",
        "Should I invest in NVIDIA?"
    ]
    
    for question in test_questions:
        print(f"\n  Q: {question}")
        response = chatbot.process_query(question)
        print(f"  Intent: {response['intent']}")
        print(f"  Detected symbols: {response['detected_symbols']}")
        print(f"  A: {response['text'][:150]}...")
    
    print("\n=== Test completed successfully! ===")

if __name__ == "__main__":
    main() 