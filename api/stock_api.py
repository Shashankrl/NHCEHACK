"""
Mock stock API functions for testing
"""
from flask import jsonify
from datetime import datetime

def get_stock_data(symbol):
    """Get mock stock data for testing"""
    # Mock data for a few symbols
    stocks = {
        "AAPL": {
            "name": "Apple Inc.",
            "price": 182.63,
            "previousClose": 180.75,
            "change": 1.88,
            "changePercent": 1.04,
            "summary": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
        },
        "MSFT": {
            "name": "Microsoft Corporation",
            "price": 405.32,
            "previousClose": 402.56,
            "change": 2.76,
            "changePercent": 0.69,
            "summary": "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide."
        },
        "AMZN": {
            "name": "Amazon.com, Inc.",
            "price": 177.58,
            "previousClose": 175.89,
            "change": 1.69,
            "changePercent": 0.96,
            "summary": "Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions in North America and internationally."
        }
    }
    
    # Return data for the requested symbol, or error if not found
    if symbol.upper() in stocks:
        data = stocks[symbol.upper()]
        return jsonify({
            "symbol": symbol.upper(),
            "name": data["name"],
            "price": data["price"],
            "previousClose": data["previousClose"],
            "change": data["change"],
            "changePercent": data["changePercent"],
            "summary": data["summary"],
            "news": [],
            "market_data": {},
            "company_info": {},
            "updated_at": datetime.now().isoformat(),
            "request_time": datetime.now().isoformat()
        }), 200
    else:
        return jsonify({
            "error": f"Stock symbol '{symbol}' not found",
            "timestamp": datetime.now().isoformat()
        }), 404 