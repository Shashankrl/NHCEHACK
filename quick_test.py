"""
Quick test of MockNLPProcessor without importing other modules
"""
import sys
import os
sys.path.insert(0, os.path.abspath("."))

# Import directly to avoid importing other modules through __init__.py
from fundwise.nlp.mock_nlp import MockNLPProcessor

def test_mock_nlp():
    print("Initializing MockNLPProcessor...")
    processor = MockNLPProcessor()
    
    # Test article
    article = {
        'title': 'Tesla Reports Strong Q2 Earnings',
        'content': 'Tesla Inc. announced better than expected earnings for Q2 2023. Revenue increased by 47% year-over-year, beating analyst expectations. The company cited strong demand for Model Y and production improvements.',
        'source': 'Financial Times',
        'date': '2023-07-20'
    }
    
    # Process article
    print("\nProcessing article...")
    result = processor.process_article(article)
    
    # Display results
    print(f"\nTitle: {result['title']}")
    print(f"Summary: {result['summary']}")
    print(f"Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
    print(f"Key factors: {', '.join(result['sentiment']['factors'])}")
    print(f"Related symbols: {', '.join(result['related_symbols'])}")
    
    # Test question answering
    question = "Why is TSLA up today?"
    print(f"\nQuestion: {question}")
    answer = processor.answer_question(question)
    print(f"Answer: {answer}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_mock_nlp() 