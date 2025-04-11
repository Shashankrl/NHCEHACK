"""
Chatbot API integration for FundWise
"""
import os
from datetime import datetime
from flask import jsonify, request
from summarizer.chatbot_nlp import ChatbotNLP
from summarizer.news_processor import NewsProcessor

# Initialize the chatbot with API key from environment
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    chatbot = ChatbotNLP(api_key)
    news_processor = NewsProcessor(api_key)
    
    # Flag to track initialization status
    chatbot_initialized = True
except Exception as e:
    print(f"Error initializing chatbot: {e}")
    chatbot_initialized = False
    chatbot = None
    news_processor = None

def process_chat_request():
    """Process incoming chat request"""
    # Check if chatbot is initialized
    if not chatbot_initialized:
        return jsonify({
            "response": "Chatbot service is currently unavailable. Please check API keys.",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False
        }), 503
    
    # Get request data
    data = request.json
    if not data or 'message' not in data:
        return jsonify({
            "response": "Please provide a message in your request.",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False
        }), 400
    
    user_message = data['message']
    
    # Process the message
    try:
        result = chatbot.process_query(user_message)
        
        response = {
            "response": result['text'],
            "timestamp": datetime.now().isoformat(),
            "request_processed": True
        }
        
        # Include detected symbols if any
        if result.get('detected_symbols'):
            response["detected_symbol"] = result['detected_symbols'][0]
            
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error processing chat request: {e}")
        return jsonify({
            "response": "I encountered an error processing your request. Please try again.",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False,
            "error": str(e)
        }), 500

def get_stock_news(symbol):
    """Get news for a specific stock"""
    if not chatbot_initialized:
        return jsonify({
            "response": "News service is currently unavailable. Please check API keys.",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False
        }), 503
    
    try:
        articles = news_processor.find_articles_by_symbol(symbol, days=7)
        
        # Process articles into a simpler format
        processed_news = []
        for article in articles:
            news_item = {
                "title": article.get('title', ''),
                "source": article.get('source', ''),
                "url": article.get('url', ''),
                "date": article.get('date', ''),
                "summary": article.get('summary', ''),
                "sentiment": article.get('sentiment', {}).get('label', 'Neutral')
            }
            processed_news.append(news_item)
        
        return jsonify({
            "symbol": symbol,
            "news_count": len(processed_news),
            "news": processed_news,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return jsonify({
            "response": f"Error fetching news for {symbol}",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False,
            "error": str(e)
        }), 500

def get_stock_explanation(symbol):
    """Get explanation for why a stock is up or down"""
    if not chatbot_initialized:
        return jsonify({
            "response": "Explanation service is currently unavailable. Please check API keys.",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False
        }), 503
    
    try:
        explanation = news_processor.explain_stock_movement(symbol)
        
        return jsonify({
            "symbol": symbol,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error generating explanation for {symbol}: {e}")
        return jsonify({
            "response": f"Error generating explanation for {symbol}",
            "timestamp": datetime.now().isoformat(),
            "request_processed": False,
            "error": str(e)
        }), 500 