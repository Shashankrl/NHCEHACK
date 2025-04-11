# FundWise NLP

FundWise NLP is a financial news analysis system that processes financial news articles and provides insights about stock movements, sentiment analysis, and answers questions about the market.

## Features

- Process financial news articles
- Extract sentiment (positive/negative/neutral)
- Identify mentioned stock symbols
- Answer questions like "Why is [stock] down today?"
- Explain stock movements based on recent news

## Components

The system consists of the following main components:

1. **GeminiSummarizer**: Uses Google's Gemini API for advanced NLP capabilities
2. **MockNLPProcessor**: A fallback solution that doesn't require API keys
3. **News Processor**: Processes and filters news articles by stock symbol and sentiment
4. **Chatbot NLP**: Handles user queries about stocks and market movements

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fundwise-nlp.git
cd fundwise-nlp

# Install dependencies
pip install -r requirements.txt

# Configure API keys (optional)
cp .env.example .env
# Edit .env to add your Gemini API key
```

## Usage

### Basic Demo

```python
from fundwise.nlp import MockNLPProcessor

# Initialize the NLP processor
nlp = MockNLPProcessor()

# Process a news article
article = {
    'title': 'Tesla Reports Strong Q2 Earnings',
    'content': 'Tesla Inc. announced better than expected earnings for Q2 2023...',
    'source': 'Financial Times',
    'date': '2023-07-20'
}

# Process the article
result = nlp.process_article(article)
print(f"Summary: {result['summary']}")
print(f"Sentiment: {result['sentiment']}")
print(f"Related Symbols: {result['related_symbols']}")

# Ask a question about a stock
answer = nlp.answer_question("Why is TSLA up today?")
print(f"Answer: {answer}")
```

### Using Gemini API (Recommended)

```python
import os
from fundwise.nlp import GeminiSummarizer

# Initialize with API key
api_key = os.environ.get("GEMINI_API_KEY")
nlp = GeminiSummarizer(api_key=api_key)

# Process article and ask questions
# (same methods as MockNLPProcessor)
```

## Project Structure

```
fundwise/
├── nlp/
│   ├── __init__.py
│   ├── gemini_summarizer.py  # Gemini-powered NLP
│   ├── mock_nlp.py           # No-API fallback
│   ├── news_processor.py     # News article processing
│   └── chatbot_nlp.py        # Question answering
├── tests/
│   ├── test_nlp.py
│   └── test_news_processor.py
├── examples/
│   ├── basic_demo.py
│   └── interactive_demo.py
└── requirements.txt
```

## Integration

### Integration with Flask API

The NLP components can be easily integrated with a Flask API:

```python
from flask import Flask, request, jsonify
from fundwise.nlp import MockNLPProcessor

app = Flask(__name__)
nlp = MockNLPProcessor()

@app.route('/api/process-article', methods=['POST'])
def process_article():
    article = request.json
    result = nlp.process_article(article)
    return jsonify(result)

@app.route('/api/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    answer = nlp.answer_question(question)
    return jsonify({'answer': answer})
```

### Integration with React Frontend

The API endpoints can be consumed by a React frontend:

```javascript
// Example fetch calls
const processArticle = async (article) => {
  const response = await fetch('/api/process-article', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(article)
  });
  return await response.json();
};

const askQuestion = async (question) => {
  const response = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  return await response.json();
};
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.