from summarizer.mock_nlp import MockNLPProcessor
from pprint import pprint

# Initialize the mock NLP processor
print("Initializing MockNLPProcessor...")
nlp = MockNLPProcessor()

# Create sample articles
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
    },
    {
        'title': 'Amazon Prime Day Sets New Sales Record',
        'content': 'Amazon announced that its Prime Day event set new sales records with over 375 million items purchased worldwide. The company reported that this was the largest Prime Day event in its history.',
        'source': 'CNBC',
        'date': '2023-07-14'
    }
]

# 1. Test batch processing
print("\n1. BATCH PROCESSING ARTICLES")
print("=" * 50)
processed_articles = nlp.batch_process_articles(articles)
print(f"Processed {len(processed_articles)} articles")

# 2. Test finding by symbol
print("\n2. FINDING ARTICLES BY SYMBOL")
print("=" * 50)
tesla_articles = nlp.find_articles_by_symbol("TSLA")
print(f"Found {len(tesla_articles)} articles about TSLA")
if tesla_articles:
    print(f"Title: {tesla_articles[0]['title']}")

apple_articles = nlp.find_articles_by_symbol("AAPL")
print(f"Found {len(apple_articles)} articles about AAPL")
if apple_articles:
    print(f"Title: {apple_articles[0]['title']}")

# 3. Test finding by sentiment
print("\n3. FINDING ARTICLES BY SENTIMENT")
print("=" * 50)
positive_articles = nlp.find_articles_by_sentiment("Positive")
print(f"Found {len(positive_articles)} positive articles")
for article in positive_articles:
    print(f"- {article['title']} (Sentiment: {article['sentiment']['label']})")

negative_articles = nlp.find_articles_by_sentiment("Negative")
print(f"Found {len(negative_articles)} negative articles")
for article in negative_articles:
    print(f"- {article['title']} (Sentiment: {article['sentiment']['label']})")

# 4. Test question answering
print("\n4. TESTING QUESTION ANSWERING")
print("=" * 50)
questions = [
    "Why is TSLA up today?",
    "Why is AAPL down today?",
    "What's happening with MSFT?",
    "Should I invest in AMZN?",
    "What's the latest news about Google?"
]

for question in questions:
    answer = nlp.answer_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    print("-" * 50)

# 5. Test summarization
print("\n5. TESTING TEXT SUMMARIZATION")
print("=" * 50)
long_text = """
The Federal Reserve kept interest rates steady on Wednesday but left the door open to a September rate cut, 
noting that inflation has eased over the past year. Fed Chair Jerome Powell said 
the central bank was moving toward cutting rates but wanted to see more evidence of 
inflation slowing before beginning to ease monetary policy. The S&P 500 rose following 
the announcement, as investors took comfort in Powell's acknowledgment that the time for 
rate cuts is approaching. Treasury yields initially fell but then rebounded as Powell 
emphasized that the Fed would remain data-dependent in its approach to policy changes.
"""
summary = nlp.summarize_text(long_text)
print(f"Original length: {len(long_text)} characters")
print(f"Summary length: {len(summary)} characters")
print(f"Summary: {summary}")

print("\nTest completed successfully!") 