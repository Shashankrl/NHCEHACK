"""
Demonstration of FundWise NLP components using only MockNLPProcessor
"""
import sys
import os
# Add the project root to the path (for running the example directly)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import directly to avoid issues
from fundwise.nlp.mock_nlp import MockNLPProcessor

def main():
    """Run a demonstration using only the MockNLPProcessor."""
    print("FundWise NLP Components - Mock Processor Demo")
    print("=" * 50)
    
    # Initialize the mock processor
    print("Initializing MockNLPProcessor...")
    processor = MockNLPProcessor()
    
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
    
    # Process all articles
    print("\nProcessing articles...")
    for article in articles:
        result = processor.process_article(article)
        print(f"\nProcessed: {article['title']}")
        print(f"  Summary: {result['summary']}")
        print(f"  Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
        print(f"  Related symbols: {', '.join(result['related_symbols'])}")
    
    # Find articles by symbol
    print("\nFinding articles by symbol:")
    tesla_articles = processor.find_articles_by_symbol("TSLA")
    print(f"Found {len(tesla_articles)} articles about TSLA")
    
    apple_articles = processor.find_articles_by_symbol("AAPL")
    print(f"Found {len(apple_articles)} articles about AAPL")
    
    # Answer questions
    print("\nAnswering questions:")
    questions = [
        "Why is TSLA up today?",
        "What's happening with AAPL?",
        "Should I invest in MSFT?"
    ]
    
    for question in questions:
        answer = processor.answer_question(question)
        print(f"\nQ: {question}")
        print(f"A: {answer}")
    
    print("\nDemo completed.")

if __name__ == "__main__":
    main() 