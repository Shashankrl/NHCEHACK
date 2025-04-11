"""
Basic demonstration of FundWise NLP capabilities using MockNLPProcessor
"""
import sys
import os
# Add the project root to the path (for running the example directly)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fundwise.nlp import MockNLPProcessor

def main():
    """Run a basic demonstration of the FundWise NLP system."""
    print("Initializing FundWise NLP (Mock Processor)...")
    nlp = MockNLPProcessor()
    
    # Sample financial news articles
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
        }
    ]
    
    # Process articles
    print("\nProcessing articles...")
    processed_articles = []
    for article in articles:
        result = nlp.process_article(article)
        processed_articles.append(result)
        
        print(f"\nProcessed: {article['title']}")
        print(f"  Summary: {result['summary']}")
        print(f"  Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
        if result['sentiment']['factors']:
            print(f"  Key factors: {', '.join(result['sentiment']['factors'])}")
        print(f"  Related symbols: {', '.join(result['related_symbols'])}")
    
    # Ask questions
    print("\nAsking stock-related questions...")
    questions = [
        "Why is TSLA up today?",
        "What's happening with AAPL?",
        "Should I invest in Microsoft?"
    ]
    
    for question in questions:
        answer = nlp.answer_question(question)
        print(f"\nQ: {question}")
        print(f"A: {answer}")
    
    # Find articles by symbol
    print("\nFinding articles by stock symbol...")
    tesla_articles = nlp.find_articles_by_symbol("TSLA")
    print(f"Found {len(tesla_articles)} articles about TSLA")
    
    # Find articles by sentiment
    print("\nFinding articles by sentiment...")
    positive_articles = nlp.find_articles_by_sentiment("Positive")
    negative_articles = nlp.find_articles_by_sentiment("Negative")
    
    print(f"Positive articles: {len(positive_articles)}")
    print(f"Negative articles: {len(negative_articles)}")

if __name__ == "__main__":
    main() 