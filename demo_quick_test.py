from summarizer.mock_nlp import MockNLPProcessor

# Initialize the processor
nlp = MockNLPProcessor()

# Sample articles with clear stock symbols
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

# Process the articles
print("Processing articles...")
processed_articles = []
for article in articles:
    result = nlp.process_article(article)
    processed_articles.append(result)
    print(f"Processed: {article['title']}")
    print(f"  Extracted symbols: {result['related_symbols']}")
    print(f"  Sentiment: {result['sentiment']['label']} ({result['sentiment']['score']})")
    print()

# Test queries
test_queries = [
    "Tell me about Tesla",
    "What's happening with TSLA?",
    "Why is Apple down?",
    "Latest news on AAPL",
    "Should I invest in Microsoft?",
    "Tell me about a company not in our database"
]

print("\nTesting queries...")
print("=" * 50)

for query in test_queries:
    print(f"\nQuery: {query}")
    
    # Search for matches in processed articles
    found = False
    for article in processed_articles:
        # Check for company names in query
        if "tesla" in query.lower() and "TSLA" in article['related_symbols']:
            print(f"Found match: {article['title']}")
            print(f"  Summary: {article['summary']}")
            print(f"  Sentiment: {article['sentiment']['label']}")
            found = True
            break
        elif "apple" in query.lower() or "aapl" in query.lower():
            if "AAPL" in article['related_symbols']:
                print(f"Found match: {article['title']}")
                print(f"  Summary: {article['summary']}")
                print(f"  Sentiment: {article['sentiment']['label']}")
                found = True
                break
    
    if not found:
        answer = nlp.answer_question(query)
        print(f"No specific match found. Default answer: {answer}") 