"""
Example of integrating FundWise NLP with Flask
This is just an example - not a fully functional application
"""
import sys
import os
# Add the project root to the path (for running the example directly)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# This is just an example - Flask is not required to be installed
# to view this sample code
"""
from flask import Flask, request, jsonify
from fundwise.nlp import MockNLPProcessor
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize NLP processor
# In a real application, you'd want to initialize this based on
# available API keys and environment variables
nlp = MockNLPProcessor()

@app.route('/api/process-article', methods=['POST'])
def process_article():
    """Process a news article and return analysis"""
    article = request.json
    if not article:
        return jsonify({'error': 'No article provided'}), 400
    
    # Process the article
    result = nlp.process_article(article)
    return jsonify(result)

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Answer a question about stocks"""
    data = request.json
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    question = data['question']
    context = data.get('context', '')
    
    # Get the answer
    answer = nlp.answer_question(question, context)
    return jsonify({'answer': answer})

@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of financial text"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    sentiment = nlp.analyze_sentiment(text)
    return jsonify(sentiment)

@app.route('/api/extract-symbols', methods=['POST'])
def extract_symbols():
    """Extract stock symbols from text"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    symbols = nlp.extract_symbols(text)
    return jsonify({'symbols': symbols})

@app.route('/api/find-by-symbol/<symbol>', methods=['GET'])
def find_by_symbol(symbol):
    """Find articles by stock symbol"""
    articles = nlp.find_articles_by_symbol(symbol)
    return jsonify({'symbol': symbol, 'articles': articles})

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
"""

def main():
    """Display the Flask integration example."""
    print("This is an example of how to integrate FundWise NLP with Flask.")
    print("The actual code is commented out to avoid requiring Flask installation.")
    print("To use this example, create a Flask app and copy the routes from this file.")

if __name__ == "__main__":
    main() 