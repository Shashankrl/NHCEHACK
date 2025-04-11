"""
Test script to verify FundWise article and symbol matching
"""
from summarizer.mock_nlp import MockNLPProcessor

# Initialize the processor
nlp = MockNLPProcessor()

# Sample articles
sample_articles = [
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
    },
    {
        'title': 'Amazon Prime Day Sets New Sales Record',
        'content': 'Amazon announced that its Prime Day event set new sales records with over 375 million items purchased worldwide. The company reported that this was the largest Prime Day event in its history.',
        'source': 'CNBC',
        'date': '2023-07-14'
    },
    {
        'title': 'Nvidia Stock Surges on AI Chip Demand',
        'content': 'Nvidia shares jumped 8% today as demand for AI chips continues to surge. The company has been a key beneficiary of the artificial intelligence boom, with its GPUs being essential for training large language models.',
        'source': 'Reuters',
        'date': '2023-07-21'
    }
]

# Process articles
print("Processing articles...")
processed_articles = []
for article in sample_articles:
    result = nlp.process_article(article)
    processed_articles.append(result)
    print(f"Processed: {article['title']}")
    print(f"  Extracted symbols: {result['related_symbols']}")
    
# Company keywords map
symbol_mapping = {
    "tesla": ["TSLA", "tesla", "musk", "model y", "electric vehicle"],
    "apple": ["AAPL", "apple", "iphone", "mac", "ios", "cupertino"],
    "microsoft": ["MSFT", "microsoft", "azure", "windows", "satya"],
    "amazon": ["AMZN", "amazon", "prime", "bezos", "aws", "e-commerce"],
    "nvidia": ["NVDA", "nvidia", "graphics", "gpu", "ai chips", "jensen"]
}

# Test queries
test_queries = [
    "Tell me about Tesla",
    "What's happening with TSLA?", 
    "Why is Apple down today?",
    "Latest news on AAPL",
    "Microsoft Azure growth",
    "How is NVDA performing?",
    "Amazon Prime Day results",
    "What do you know about Musk's company?",
    "Tell me about companies not in the database"
]

print("\n" + "=" * 60)
print("TESTING ARTICLE MATCHING".center(60))
print("=" * 60)

# Process each query
for query in test_queries:
    print(f"\nQuery: {query}")
    question_lower = query.lower()
    
    # Find matching articles
    matching_articles = []
    
    # Check for company names and keywords
    for company, keywords in symbol_mapping.items():
        for keyword in keywords:
            if keyword.lower() in question_lower:
                # Find symbol for this company
                symbol = keywords[0]  # First item is always the symbol
                
                # Search for articles with this symbol
                for article in processed_articles:
                    if symbol in article.get('related_symbols', []) and article not in matching_articles:
                        matching_articles.append((article, company, symbol))
    
    # Display results
    if matching_articles:
        print(f"Found {len(matching_articles)} matching articles:")
        for i, (article, company, symbol) in enumerate(matching_articles, 1):
            print(f"  {i}. {article['title']} ({symbol})")
            print(f"     Related to: {company}")
            
        # If asking about why a stock is up/down, provide specific response
        if "why" in question_lower and any(term in question_lower for term in ["up", "down", "rising", "falling", "increase", "decrease"]):
            first_article = matching_articles[0][0]
            sentiment = first_article['sentiment']
            company_name = matching_articles[0][1].title()
            
            if isinstance(sentiment, dict) and sentiment.get('label') == 'Positive':
                print(f"  Reason: {company_name} is performing well because of positive factors like: {', '.join(sentiment.get('factors', []))}")
            elif isinstance(sentiment, dict) and sentiment.get('label') == 'Negative':
                print(f"  Reason: {company_name} is facing challenges due to: {', '.join(sentiment.get('factors', []))}")
    else:
        print("  No matching articles found")
        answer = nlp.answer_question(query)
        print(f"  Default answer: {answer}")
    
    print("-" * 60) 