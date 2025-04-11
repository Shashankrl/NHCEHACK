"""
API routes for FundWise
"""
from flask import Blueprint, request, jsonify
from api.chatbot_api import process_chat_request, get_stock_news, get_stock_explanation
from api.stock_api import get_stock_data  # Assuming this exists in your codebase

# Create blueprint
api_bp = Blueprint('api', __name__)

# Chat endpoint
@api_bp.route('/chat', methods=['POST'])
def chat():
    """Process a chat message"""
    return process_chat_request()

# Stock data endpoint
@api_bp.route('/stock', methods=['GET'])
def stock():
    """Get stock data"""
    symbol = request.args.get('symbol', '')
    if not symbol:
        return jsonify({
            "error": "Symbol parameter is required",
            "example": "/api/stock?symbol=AAPL"
        }), 400
    
    return get_stock_data(symbol)

# Stock news endpoint
@api_bp.route('/news/<symbol>', methods=['GET'])
def news(symbol):
    """Get news for a specific stock"""
    return get_stock_news(symbol)

# Stock explanation endpoint
@api_bp.route('/explain/<symbol>', methods=['GET'])
def explain(symbol):
    """Get explanation for why a stock is up or down"""
    return get_stock_explanation(symbol)

# Market overview endpoint
@api_bp.route('/market', methods=['GET'])
def market():
    """Get market overview"""
    # This could be implemented in the stock_api.py file
    # For now, return a simple response
    return jsonify({
        "message": "Market overview endpoint not implemented yet",
        "status": "coming_soon"
    }), 501 