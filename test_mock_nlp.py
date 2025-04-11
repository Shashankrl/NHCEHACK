from summarizer.mock_nlp import MockNLPProcessor

# Initialize the mock NLP processor
nlp = MockNLPProcessor()

# Test with a sample article
article = {
    'title': 'Tesla Reports Strong Q2 Earnings',
    'content': 'Tesla Inc. announced better than expected earnings for Q2 2023. Revenue increased by 47% year-over-year, beating analyst expectations. The company cited strong demand for Model Y and production improvements.',
    'source': 'Financial Times',
    'date': '2023-07-20'
}

# Process the article
result = nlp.process_article(article)

# Print the results
print("===== MOCK NLP PROCESSOR TEST =====")
print(f"Summary: {result['summary']}")
print(f"Sentiment: {result['sentiment']}")
print(f"Related Symbols: {result['related_symbols']}")
print("===================================")

# Test question answering
question = "Why is TSLA up today?"
answer = nlp.answer_question(question)
print(f"\nQ: {question}")
print(f"A: {answer}") 