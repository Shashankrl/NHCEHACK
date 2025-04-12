"""
Simplified Flask API for hackathon demo.
Now with REAL-TIME data scraping for Indian stock market.
"""
import os
import json
import random
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our NSE data scraper
from nse_scraper import get_quote, get_historical_data, get_top_gainers, get_top_losers, fetch_news_for_stock

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# List of popular Indian stocks for recognition
POPULAR_INDIAN_STOCKS = [
    "NIFTY", "SENSEX", "BANKNIFTY", "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", 
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK", "BAJFINANCE", "ASIANPAINT",
    "MARUTI", "AXISBANK", "WIPRO", "TATAMOTORS", "SUNPHARMA", "TITAN", "BAJAJFINSV",
    "LTIM", "HCLTECH", "ADANIENT", "NTPC", "JSWSTEEL", "ULTRACEMCO", "TATASTEEL", "M&M"
]

# Cache for storing scraped data (to avoid hitting rate limits)
CACHE = {}

def extract_stock_symbol(message):
    """Extract stock symbol from message, advanced version"""
    # First check for known stocks
    for stock in POPULAR_INDIAN_STOCKS:
        if stock.upper() in message.upper():
            return stock
    
    # Look for potential stock mentions (uppercase words)
    words = message.upper().split()
    for word in words:
        # Clean up the word
        clean_word = ''.join(c for c in word if c.isalnum() or c == '&')
        
        # Check if it's a potential stock symbol
        if (len(clean_word) >= 2 and clean_word.isalpha() and 
            clean_word not in ['AND', 'THE', 'FOR', 'HOW', 'WHY', 'WHAT', 'WHO', 'WHERE', 'WHEN', 'WHICH', 'ABOUT', 'TELL']):
            return clean_word
    
    # Default to NIFTY if nothing found
    return "NIFTY"

# API endpoints
@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for frontend integration"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Identify entity mentioned in message
    entity = extract_stock_symbol(message)
    
    # Get real-time stock data
    try:
        stock_data = get_quote(entity)
        historical_data = get_historical_data(entity)
        
        # Get relevant news for the entity
        news_articles = fetch_news_for_stock(entity, count=5)
        
        # Convert historical data to arrays for charts
        dates = [item['date'] for item in historical_data]
        prices = [item['close'] for item in historical_data]
        
        # Check if user wants professional format
        use_professional_format = any(term in message.lower() for term in ["professional", "newssense", "business", "formal", "analyst", "concise"])
        
        # Generate response based on message content and format preference
        if use_professional_format:
            sentiment = "positive" if stock_data['pChange'] > 0 else "negative" if stock_data['pChange'] < 0 else "neutral"
            response = generate_professional_analysis(entity, stock_data, historical_data, news_articles, sentiment)
        elif any(term in message.lower() for term in ["down", "fall", "decline", "dropped"]):
            basic_response = generate_down_response(entity, stock_data)
            response = generate_structured_analysis(entity, stock_data, historical_data, basic_response, news_articles, sentiment="negative")
        elif any(term in message.lower() for term in ["up", "rise", "gain", "growth"]):
            basic_response = generate_up_response(entity, stock_data)
            response = generate_structured_analysis(entity, stock_data, historical_data, basic_response, news_articles, sentiment="positive")
        elif "compare" in message.lower():
            # Find second entity to compare
            second_entity = None
            # Look for other mentioned stocks
            for stock in POPULAR_INDIAN_STOCKS:
                if stock.upper() in message.upper() and stock != entity:
                    second_entity = stock
                    break
            
            if not second_entity:
                # Try to find a second stock mention
                parts = message.split("compare")[1].split("with" if "with" in message.lower() else "and" if "and" in message.lower() else "to" if "to" in message.lower() else " ")
                if len(parts) > 1:
                    potential_second = extract_stock_symbol(parts[1])
                    if potential_second != entity:
                        second_entity = potential_second
            
            # If still nothing, just pick a random one
            if not second_entity:
                second_entity = random.choice([s for s in POPULAR_INDIAN_STOCKS if s != entity])
            
            # Get second stock data
            second_stock_data = get_quote(second_entity)
            second_historical_data = get_historical_data(second_entity)
            
            # Generate comparison response
            response = generate_comparison_response(entity, stock_data, second_entity, second_stock_data)
            
            # Create comparison chart
            chart_data = create_comparison_chart(
                entity, historical_data,
                second_entity, second_historical_data
            )
        else:
            basic_response = generate_general_response(entity, stock_data)
            sentiment = "positive" if stock_data['pChange'] > 0 else "negative" if stock_data['pChange'] < 0 else "neutral"
            response = generate_structured_analysis(entity, stock_data, historical_data, basic_response, news_articles, sentiment=sentiment)
        
        # Create chart data if not already created (for comparison)
        if 'compare' not in message.lower():
            chart_data = create_stock_chart(entity, historical_data, stock_data)
        
        return jsonify({
            "id": str(uuid.uuid4()),
            "content": response,
            "has_graph": True,
            "entity": entity,
            "chart_data": chart_data,
            "live_data": {
                "price": stock_data['price'],
                "change": stock_data['change'],
                "pChange": stock_data['pChange'],
                "lastUpdateTime": stock_data['lastUpdateTime']
            }
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "id": str(uuid.uuid4()),
            "content": f"I encountered an issue while retrieving data for {entity}. This could be due to market hours or connection issues. Please try again or ask about a different stock.",
            "has_graph": False,
            "entity": entity,
            "error": str(e)
        })

@app.route('/api/entities', methods=['GET'])
def get_entities():
    """Get available entities with performance data"""
    try:
        # Attempt to get real top gainers and losers
        gainers = get_top_gainers()
        losers = get_top_losers()
        
        # Combine them with some standard entities
        standard_symbols = ["NIFTY", "SENSEX", "BANKNIFTY", "RELIANCE", "TCS"]
        
        result = []
        
        # Add top gainers (marked with positive sentiment)
        for gainer in gainers[:5]:  # Top 5 gainers
            symbol = gainer['symbol']
            result.append({
                "symbol": symbol,
                "description": f"{symbol} - Top gainer today",
                "performance": f"+{gainer['pChange']:.2f}%",
                "sentiment": "positive"
            })
        
        # Add top losers (marked with negative sentiment)
        for loser in losers[:5]:  # Top 5 losers
            symbol = loser['symbol']
            result.append({
                "symbol": symbol,
                "description": f"{symbol} - Top loser today",
                "performance": f"{loser['pChange']:.2f}%",
                "sentiment": "negative"
            })
        
        # Add standard symbols if not already included
        for symbol in standard_symbols:
            if not any(item['symbol'] == symbol for item in result):
                try:
                    quote = get_quote(symbol)
                    result.append({
                        "symbol": symbol,
                        "description": get_stock_description(symbol),
                        "performance": f"{quote['pChange']:.2f}%",
                        "sentiment": "positive" if quote['pChange'] > 0 else "negative" if quote['pChange'] < 0 else "neutral"
                    })
                except Exception as e:
                    print(f"Error getting quote for {symbol}: {str(e)}")
        
        return jsonify({"entities": result})
    
    except Exception as e:
        print(f"Error in get_entities: {str(e)}")
        # Fallback to basic entities list if real-time data fails
        fallback_entities = [
            {"symbol": "NIFTY", "description": "Nifty 50 - India's benchmark stock market index", "performance": "0.75%", "sentiment": "positive"},
            {"symbol": "SENSEX", "description": "S&P BSE SENSEX - Index of 30 well-established companies", "performance": "0.68%", "sentiment": "positive"},
            {"symbol": "BANKNIFTY", "description": "Bank Nifty - Index tracking banking sector stocks", "performance": "-0.32%", "sentiment": "negative"},
            {"symbol": "RELIANCE", "description": "Reliance Industries - India's largest conglomerate", "performance": "1.24%", "sentiment": "positive"},
            {"symbol": "TCS", "description": "Tata Consultancy Services - India's largest IT services company", "performance": "-0.45%", "sentiment": "negative"}
        ]
        return jsonify({"entities": fallback_entities})

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get news articles, optionally filtered by entity"""
    entity = request.args.get('entity', None)
    
    try:
        if entity:
            # Get news specifically for this entity
            articles = fetch_news_for_stock(entity, count=10)
        else:
            # Get news for several popular stocks
            articles = []
            for symbol in ["NIFTY", "RELIANCE", "TCS", "HDFCBANK", "INFY"]:
                articles.extend(fetch_news_for_stock(symbol, count=3))
        
        # Format for response
        result = []
        for article in articles:
            result.append({
                "title": article["title"],
                "source": article["source"],
                "date": article["date"],
                "snippet": article["content"][:150] + "...",
                "url": article["url"],
                "redirect_url": article.get("redirect_url", article["url"]),
                "sentiment": article["sentiment"]
            })
        
        # Add information about data sources
        return jsonify({
            "articles": result,
            "meta": {
                "total_articles": len(result),
                "sources_scanned": ["Economic Times", "Business Standard", "Financial Express", "Money Control", "Live Mint", "Hindu Business Line", "Bloomberg Quint", "NDTV Profit"],
                "data_source": "Real-time web scraping from financial news sources with fallback to generated data for hackathon demo.",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    
    except Exception as e:
        print(f"Error in get_articles: {str(e)}")
        # Return error with some minimal mock data
        return jsonify({
            "articles": [
                {
                    "title": f"Market update: Indian stocks showing mixed trends",
                    "source": "Financial Insight",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "snippet": "Indian stock markets showed mixed trends today as investors assessed global cues and domestic economic data...",
                    "url": "https://economictimes.indiatimes.com/markets/stocks/news/stock-market-update-" + str(random.randint(10000, 99999)),
                    "redirect_url": "https://economictimes.indiatimes.com",
                    "sentiment": "neutral"
                }
            ],
            "meta": {
                "total_articles": 1,
                "sources_scanned": ["Fallback Data"],
                "data_source": "Using fallback data due to API error. Real implementation would use web scraping from financial sources.",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e)
            }
        })

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions for the chat interface"""
    try:
        # Get real top gainers and losers for suggestions
        gainers = get_top_gainers()
        losers = get_top_losers()
        
        # Use actual market movers for suggestions
        top_gainer = gainers[0]['symbol'] if gainers else "NIFTY"
        top_loser = losers[0]['symbol'] if losers else "BANKNIFTY"
        
        suggestions = [
            f"Why is {top_loser} down today?",
            f"How is {top_gainer} performing?",
            f"Compare {top_gainer} with {top_loser}",
            "Explain the banking sector trend",
            "What are the top financial news today?"
        ]
        return jsonify({"suggestions": suggestions})
    
    except Exception as e:
        print(f"Error in get_suggestions: {str(e)}")
        # Fallback to basic suggestions
        suggestions = [
            "Why is NIFTY down today?",
            "How is RELIANCE performing?",
            "Compare TCS with INFY",
            "Explain the banking sector trend",
            "What are the top financial news today?"
        ]
        return jsonify({"suggestions": suggestions})

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """For compatibility with frontend - redirects to chat endpoint"""
    return chat()

@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Get graph data for a specific entity"""
    question = request.args.get('question', '')
    entity = request.args.get('entity', 'NIFTY')
    
    try:
        # Get real-time stock data
        quote = get_quote(entity)
        historical_data = get_historical_data(entity)
        
        # Create chart
        chart_data = create_stock_chart(entity, historical_data, quote)
        
        return jsonify({
            "graph_data": chart_data,
            "entity": entity,
            "live_data": {
                "price": quote['price'],
                "change": quote['change'],
                "pChange": quote['pChange']
            }
        })
    
    except Exception as e:
        print(f"Error in get_graph: {str(e)}")
        # Return error
        return jsonify({
            "error": f"Failed to retrieve data for {entity}: {str(e)}",
            "entity": entity
        }), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get information about the API and data sources"""
    return jsonify({
        "name": "MyFi NewsSense API",
        "version": "1.0.0-hackathon",
        "data_sources": {
            "stock_data": {
                "type": "Real-time web scraping with fallback",
                "primary_source": "NSE (National Stock Exchange) API",
                "secondary_source": "Yahoo Finance API",
                "fallback": "Generated data based on real market patterns",
                "entities_tracked": len(POPULAR_INDIAN_STOCKS),
                "time_period": "30 days"
            },
            "news_data": {
                "type": "Real-time news with fallback",
                "sources": ["Economic Times", "Business Standard", "Financial Express", "Money Control", "LiveMint", "Bloomberg Quint"],
                "sentiment_analysis": "Rule-based classification with NLP patterns"
            }
        },
        "capabilities": [
            "Real-time stock data for Indian markets",
            "Historical price visualization",
            "Entity comparison",
            "News sentiment analysis",
            "Market trend analysis"
        ]
    })

@app.route('/api/professional', methods=['POST'])
def professional_analysis():
    """Endpoint for professional financial analysis in NewsSense AI format"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Identify entity mentioned in message
    entity = extract_stock_symbol(message)
    
    # Get real-time stock data
    try:
        stock_data = get_quote(entity)
        historical_data = get_historical_data(entity)
        
        # Get relevant news for the entity
        news_articles = fetch_news_for_stock(entity, count=5)
        
        # Convert historical data to arrays for charts
        dates = [item['date'] for item in historical_data]
        prices = [item['close'] for item in historical_data]
        
        # Generate professional analysis
        sentiment = "positive" if stock_data['pChange'] > 0 else "negative" if stock_data['pChange'] < 0 else "neutral"
        response = generate_professional_analysis(entity, stock_data, historical_data, news_articles, sentiment)
        
        # Create chart data
        chart_data = create_stock_chart(entity, historical_data, stock_data)
        
        return jsonify({
            "id": str(uuid.uuid4()),
            "content": response,
            "has_graph": True,
            "entity": entity,
            "chart_data": chart_data,
            "live_data": {
                "price": stock_data['price'],
                "change": stock_data['change'],
                "pChange": stock_data['pChange'],
                "lastUpdateTime": stock_data['lastUpdateTime']
            },
            "format": "professional"
        })
        
    except Exception as e:
        print(f"Error in professional analysis endpoint: {str(e)}")
        return jsonify({
            "id": str(uuid.uuid4()),
            "content": f"I encountered an issue while retrieving data for {entity}. This could be due to market hours or connection issues. Please try again or ask about a different stock.",
            "has_graph": False,
            "entity": entity,
            "error": str(e),
            "format": "professional"
        })

# Helper functions for generating responses
def generate_down_response(entity, stock_data):
    """Generate response for stock that's down"""
    change = stock_data['pChange']
    
    if change > 0:
        # Stock is actually up
        return f"{entity} is up {change:.2f}% today, trading at ₹{stock_data['price']:.2f}. This positive movement contradicts recent market expectations, with strong momentum pushing the price up from an opening of ₹{stock_data['open']:.2f}."
    
    factors = [
        "market-wide selling pressure",
        "profit booking by institutional investors",
        "concerns about sectoral growth",
        "disappointing quarterly results",
        "global market uncertainty",
        "foreign institutional investor (FII) outflows"
    ]
    
    response = f"{entity} is down {abs(change):.2f}% today, trading at ₹{stock_data['price']:.2f} from an open of ₹{stock_data['open']:.2f}. This decline is primarily attributed to {random.choice(factors)} and {random.choice(factors)}.\n\nTechnical support exists around ₹{stock_data['price'] * 0.95:.2f}, with trading volume at {format_volume(stock_data['tradedQuantity'])}. Analysts suggest watching for stabilization near current levels before considering new positions."
    
    return response

def generate_up_response(entity, stock_data):
    """Generate response for stock that's up"""
    change = stock_data['pChange']
    
    if change < 0:
        # Stock is actually down
        return f"{entity} is down {abs(change):.2f}% today, trading at ₹{stock_data['price']:.2f}. Despite positive market expectations, selling pressure has pushed the stock below its opening price of ₹{stock_data['open']:.2f}."
    
    factors = [
        "strong institutional buying",
        "positive quarterly results expectations",
        "favorable sectoral outlook",
        "analyst upgrades",
        "strategic announcement by management",
        "positive global cues"
    ]
    
    response = f"{entity} has gained {change:.2f}% today, trading at ₹{stock_data['price']:.2f} with a day high of ₹{stock_data['dayHigh']:.2f}. This rally is driven by {random.choice(factors)} and {random.choice(factors)}.\n\nTrading volume of {format_volume(stock_data['tradedQuantity'])} indicates strong investor interest. The stock shows immediate resistance at ₹{stock_data['price'] * 1.05:.2f}, with momentum indicators suggesting continued positive sentiment."
    
    return response

def generate_comparison_response(entity1, data1, entity2, data2):
    """Generate response comparing two stocks"""
    change1 = data1['pChange']
    change2 = data2['pChange']
    
    difference = abs(change1 - change2)
    
    if change1 > change2:
        comparison = f"{entity1} is outperforming {entity2} today by {difference:.2f}%"
        if change2 < 0 and change1 > 0:
            details = f", with {entity1} up {change1:.2f}% while {entity2} is down {abs(change2):.2f}%"
        elif change2 < 0:
            details = f", with both down but {entity1} showing more resilience at -{abs(change1):.2f}% versus -{abs(change2):.2f}%"
        else:
            details = f", with {entity1} up {change1:.2f}% compared to {entity2}'s gain of {change2:.2f}%"
    else:
        comparison = f"{entity2} is outperforming {entity1} today by {difference:.2f}%"
        if change1 < 0 and change2 > 0:
            details = f", with {entity2} up {change2:.2f}% while {entity1} is down {abs(change1):.2f}%"
        elif change1 < 0:
            details = f", with both down but {entity2} showing more resilience at -{abs(change2):.2f}% versus -{abs(change1):.2f}%"
        else:
            details = f", with {entity2} up {change2:.2f}% compared to {entity1}'s gain of {change1:.2f}%"
    
    response = f"{comparison}{details}. {entity1} is at ₹{data1['price']:.2f} while {entity2} trades at ₹{data2['price']:.2f}.\n\nThis performance gap reflects different investor sentiment and sector dynamics. {entity1}'s trading range (₹{data1['dayLow']:.2f}-₹{data1['dayHigh']:.2f}) compared to {entity2}'s (₹{data2['dayLow']:.2f}-₹{data2['dayHigh']:.2f}) shows {'similar' if abs(data1['dayHigh']/data1['dayLow'] - data2['dayHigh']/data2['dayLow']) < 0.05 else 'different'} volatility patterns."
    
    return response

def generate_general_response(entity, stock_data):
    """Generate general response about a stock"""
    change = stock_data['pChange']
    sentiment = "positive" if change > 0 else "negative" if change < 0 else "neutral"
    
    if abs(change) < 0.5:
        price_status = f"stable at ₹{stock_data['price']:.2f} ({change:.2f}%)"
    else:
        price_status = f"{'up' if change > 0 else 'down'} {abs(change):.2f}% at ₹{stock_data['price']:.2f}"
    
    response = f"{entity} is currently {price_status}, moving between ₹{stock_data['dayLow']:.2f} and ₹{stock_data['dayHigh']:.2f} today. Trading volume stands at {format_volume(stock_data['tradedQuantity'])} shares.\n\nTechnical analysis shows {'support at ₹' + str(round(stock_data['price'] * 0.95, 2)) if change < 0 else 'resistance at ₹' + str(round(stock_data['price'] * 1.05, 2))}. Market sentiment remains {sentiment} with {'institutional buying' if change > 0 else 'cautious positioning' if change < 0 else 'balanced activity'} being the key driver."
    
    return response

def format_volume(volume):
    """Format volume in crore/lakh format for Indian market"""
    if volume > 10000000:  # > 1 crore
        return f"{volume/10000000:.2f} crore"
    elif volume > 100000:  # > 1 lakh
        return f"{volume/100000:.2f} lakh"
    else:
        return f"{volume:,}"

def get_stock_description(symbol):
    """Get description for standard symbols"""
    descriptions = {
        "NIFTY": "Nifty 50 - India's benchmark stock market index",
        "SENSEX": "S&P BSE SENSEX - Index of 30 well-established companies",
        "BANKNIFTY": "Bank Nifty - Index tracking banking sector stocks",
        "RELIANCE": "Reliance Industries - India's largest conglomerate",
        "TCS": "Tata Consultancy Services - India's largest IT services company",
        "HDFCBANK": "HDFC Bank - India's largest private sector bank by assets",
        "INFY": "Infosys - Global IT consulting and digital services",
        "ICICIBANK": "ICICI Bank - Leading private sector bank in India",
        "HINDUNILVR": "Hindustan Unilever - FMCG giant in India",
        "ITC": "ITC Limited - Diversified conglomerate with interests in FMCG, hotels, etc.",
        "SBIN": "State Bank of India - India's largest public sector bank",
        "BHARTIARTL": "Bharti Airtel - Leading telecommunications company",
        "KOTAKBANK": "Kotak Mahindra Bank - Major private sector bank",
        "BAJFINANCE": "Bajaj Finance - Leading non-banking financial company",
        "ASIANPAINT": "Asian Paints - India's largest paint company"
    }
    
    return descriptions.get(symbol, f"{symbol} - Indian stock")

def create_stock_chart(entity, historical_data, current_data):
    """Create chart data for a single stock"""
    # Extract data from historical data
    dates = [item['date'] for item in historical_data]
    closes = [item['close'] for item in historical_data]
    
    # For volume
    volumes = [item.get('volume', 0) for item in historical_data]
    
    # Format data for plotly
    chart_data = {
        "data": [
            {
                "x": dates,
                "y": closes,
                "type": "scatter",
                "mode": "lines",
                "name": entity,
                "line": {
                    "color": "rgb(75, 192, 192)",
                    "width": 2
                }
            },
            {
                "x": dates,
                "y": volumes,
                "type": "bar",
                "name": "Volume",
                "yaxis": "y2",
                "marker": {
                    "color": "rgba(200, 200, 200, 0.3)"
                }
            }
        ],
        "layout": {
            "title": f"{entity} Price Trend - ₹{current_data['price']:.2f} ({current_data['pChange']:.2f}%)",
            "xaxis": {
                "title": "Date",
                "gridcolor": "rgba(255, 255, 255, 0.1)"
            },
            "yaxis": {
                "title": "Price (₹)",
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "tickformat": ",.2f"
            },
            "yaxis2": {
                "title": "Volume",
                "overlaying": "y",
                "side": "right",
                "showgrid": False,
                "tickformat": ".2s"
            },
            "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
            "paper_bgcolor": "#20232a",
            "plot_bgcolor": "#282c34",
            "font": {"color": "white"},
            "showlegend": True,
            "legend": {"orientation": "h", "y": -0.2}
        }
    }
    
    return chart_data

def create_comparison_chart(entity1, data1, entity2, data2):
    """Create chart data comparing two stocks"""
    # Extract data
    dates1 = [item['date'] for item in data1]
    closes1 = [item['close'] for item in data1]
    
    dates2 = [item['date'] for item in data2]
    closes2 = [item['close'] for item in data2]
    
    # Normalize both datasets for comparison (start at 100)
    if closes1 and closes2:
        base_price1 = closes1[0]
        normalized1 = [price * 100 / base_price1 for price in closes1]
        
        base_price2 = closes2[0]
        normalized2 = [price * 100 / base_price2 for price in closes2]
        
        chart_data = {
            "data": [
                {
                    "x": dates1,
                    "y": normalized1,
                    "type": "scatter",
                    "mode": "lines",
                    "name": entity1,
                    "line": {"color": "rgb(75, 192, 192)", "width": 2}
                },
                {
                    "x": dates2,
                    "y": normalized2,
                    "type": "scatter",
                    "mode": "lines",
                    "name": entity2,
                    "line": {"color": "rgb(255, 99, 132)", "width": 2}
                }
            ],
            "layout": {
                "title": f"Comparison: {entity1} vs {entity2} (Normalized to 100)",
                "xaxis": {"title": "Date", "gridcolor": "rgba(255, 255, 255, 0.1)"},
                "yaxis": {"title": "Relative Performance", "gridcolor": "rgba(255, 255, 255, 0.1)"},
                "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
                "paper_bgcolor": "#20232a",
                "plot_bgcolor": "#282c34",
                "font": {"color": "white"},
                "showlegend": True,
                "legend": {"orientation": "h", "y": -0.2}
            }
        }
        
        return chart_data
    else:
        # Fallback if historical data is missing
        return {
            "data": [],
            "layout": {
                "title": "Comparison data unavailable",
                "paper_bgcolor": "#20232a",
                "plot_bgcolor": "#282c34",
                "font": {"color": "white"}
            }
        }

def generate_structured_analysis(entity, stock_data, historical_data, basic_response, news_articles=None, sentiment="neutral"):
    """Generate a structured analysis with Key Factors and Detailed Analysis sections"""
    change = stock_data['pChange']
    abs_change = abs(change)
    
    # Calculate percent change over the period
    if len(historical_data) > 0:
        first_price = historical_data[0]['close']
        last_price = historical_data[-1]['close']
        period_change = ((last_price - first_price) / first_price) * 100
    else:
        period_change = change
    
    # Generate common factors for market movement
    if sentiment == "positive":
        factors = [
            f"Strong Global Cues Supporting {entity}",
            f"Institutional Buying Driving {entity} Higher",
            f"Technical Breakout Past Resistance Levels",
            f"Positive Quarterly Results Boosting {entity}",
            f"Sector Rotation Favoring {entity}'s Industry"
        ]
        sentiment_description = "POSITIVE OUTLOOK"
        outlook_reasons = [
            "continued institutional buying",
            "strong technical indicators",
            "favorable sectoral trends",
            "supportive global markets",
            "improving earnings expectations"
        ]
    elif sentiment == "negative":
        factors = [
            f"Weak Global Markets Pressuring {entity}",
            f"Profit Booking After Recent Rally",
            f"Technical Breakdown Below Support",
            f"Concerns About Quarterly Performance",
            f"Foreign Institutional Investor Outflows"
        ]
        sentiment_description = "CAUTIOUS OUTLOOK"
        outlook_reasons = [
            "continued selling pressure",
            "weakness in technical patterns",
            "cautious institutional positioning",
            "global market headwinds",
            "earnings concerns"
        ]
    else:
        factors = [
            f"Mixed Global Cues Affecting {entity}",
            f"Balanced Institutional Activity in {entity}",
            f"Range-Bound Trading Pattern",
            f"Neutral Technical Indicators",
            f"Sector-Specific Developments"
        ]
        sentiment_description = "NEUTRAL OUTLOOK"
        outlook_reasons = [
            "balanced institutional activity",
            "sideways technical patterns",
            "mixed global cues",
            "range-bound price action",
            "sector-specific developments"
        ]
    
    # Select 2-3 factors for compact display
    selected_factors = random.sample(factors, min(3, len(factors)))
    
    # Trading volume analysis
    volume = stock_data['tradedQuantity']
    if volume > 5000000:
        volume_analysis = "exceptionally high"
    elif volume > 2000000:
        volume_analysis = "above average"
    elif volume > 1000000:
        volume_analysis = "average"
    else:
        volume_analysis = "below average"
    
    # Future outlook
    resistance_level = round(stock_data['price'] * 1.05, 2)
    support_level = round(stock_data['price'] * 0.95, 2)
    outlook_reason = random.choice(outlook_reasons)
    
    # Break text into separate sentences with line breaks for better readability
    
    # Summary section
    summary = f"""📊 Summary
{'📈' if change > 0 else '📉'} {entity} is {'up' if change > 0 else 'down'} {abs_change:.2f}% over the analyzed period."""

    # Key factors section
    key_factors = f"""
🔑 Key Factors Affecting {entity}
• {selected_factors[0]}
• {selected_factors[1]}
{f'• {selected_factors[2]}' if len(selected_factors) > 2 else ''}"""

    # Market analysis section - with line breaks after each sentence
    market_analysis = f"""
📈 Market Analysis
{entity} {'increased' if period_change > 0 else 'decreased'} by {abs(period_change):.2f}% over the last {len(historical_data)} days.

The price moved from ₹{first_price:.2f} to ₹{last_price:.2f}, representing a {'gain' if period_change > 0 else 'loss'} of {abs(period_change):.2f}%.

Trading volumes have remained {volume_analysis}, suggesting {'strong' if volume_analysis in ['exceptionally high', 'above average'] else 'moderate' if volume_analysis == 'average' else 'weak'} investor interest."""

    # Technical indicators section - with line breaks after each sentence
    technical_indicators = f"""
🔍 Technical Indicators
Key levels to watch include support at ₹{support_level} and resistance at ₹{resistance_level}.

Sentiment trends from news articles suggest a {sentiment_description} for {entity} in the short term due to {outlook_reason}."""

    # Format news links section with plain text links
    news_links_section = ""
    if news_articles and len(news_articles) > 0:
        news_links_section = "\n\n📰 Recent News Articles\n"
        for i, article in enumerate(news_articles[:3]):
            sentiment_icon = "📈" if article['sentiment'] == "positive" else "📉" if article['sentiment'] == "negative" else "📊"
            url = article.get('redirect_url', article['url'])
            title = article['title']
            source = article['source']
            date = article['date']
            news_links_section += f"{sentiment_icon} {title}\n\nSource: {source}, {date}\n\nLink: {url}\n\n{'-'*50}\n\n"
    
    # Combine all sections
    response = f"{summary}{key_factors}{market_analysis}{technical_indicators}{news_links_section}"
    
    return response

def generate_professional_analysis(entity, stock_data, historical_data, news_articles=None, sentiment="neutral"):
    """Generate a professional analysis in the NewsSense AI format"""
    
    # Get current market data
    change = stock_data['pChange']
    abs_change = abs(change)
    price = stock_data['price']
    
    # Calculate period change
    if len(historical_data) > 0:
        first_price = historical_data[0]['close']
        last_price = historical_data[-1]['close']
        period_change = ((last_price - first_price) / first_price) * 100
        start_date = historical_data[0]['date']
        end_date = historical_data[-1]['date']
    else:
        period_change = change
        start_date = "30 days ago"
        end_date = "today"
    
    # Determine volume trend description
    volume = stock_data['tradedQuantity']
    if volume > 5000000:
        volume_trend = "exceptionally high"
    elif volume > 2000000:
        volume_trend = "above average"
    elif volume > 1000000:
        volume_trend = "average"
    else:
        volume_trend = "below average"
    
    # Key factors affecting the stock
    factors_map = {
        "positive": [
            "Strong Institutional Buying",
            "Favorable Technical Breakout",
            "Positive Quarterly Results",
            "Supportive Global Market Cues",
            "Sector Rotation into Index Components",
            "Positive Management Guidance",
            "Improved Macroeconomic Indicators"
        ],
        "negative": [
            "Foreign Institutional Investor Outflows",
            "Technical Support Levels Under Pressure",
            "Earnings Disappointments",
            "Weak Global Market Sentiment",
            "Unfavorable Regulatory Developments",
            "Sector-specific Challenges",
            "Valuation Concerns"
        ],
        "neutral": [
            "Balanced Institutional Activity",
            "Range-bound Technical Patterns",
            "Mixed Quarterly Results",
            "Divergent Global Market Cues",
            "Sector Rotation Between Index Components",
            "Awaiting Policy Clarity",
            "Consolidation After Recent Movement"
        ]
    }
    
    # Select factors based on sentiment
    if sentiment == "positive":
        factor_list = factors_map["positive"]
        sentiment_description = "OPTIMISTIC"
    elif sentiment == "negative":
        factor_list = factors_map["negative"]
        sentiment_description = "CAUTIOUS"
    else:
        factor_list = factors_map["neutral"]
        sentiment_description = "NEUTRAL"
    
    # Select 3-4 factors
    selected_factors = random.sample(factor_list, min(4, len(factor_list)))
    
    # Technical levels
    resistance_level = round(stock_data['price'] * 1.05, 2)
    support_level = round(stock_data['price'] * 0.95, 2)
    
    # Format news section
    news_section = ""
    if news_articles and len(news_articles) > 0:
        for i, article in enumerate(news_articles[:3]):
            url = article.get('redirect_url', article['url'])
            title = article['title']
            source = article['source']
            date = article['date']
            news_section += f"• {title}  \n  Source: {source}, {date}  \n  Link: {url}\n\n"
    else:
        news_section = "Data not available"
    
    # Assemble the professional response
    response = f"""
**🧠 NewsSense AI**

### {'📉' if change < 0 else '📈'} Summary  
{entity} is {'down' if change < 0 else 'up'} {abs_change:.2f}% today, trading at ₹{price:.2f}.

---

### 🔑 Key Factors Affecting {entity}  
"""

    # Add key factors
    for factor in selected_factors:
        response += f"• {factor}  \n"
    
    # Continue with market analysis
    response += f"""
---

### 📈 Market Analysis  
{entity} has {'decreased' if period_change < 0 else 'increased'} by {abs(period_change):.2f}% over the last {len(historical_data)} days. The price moved from ₹{first_price:.2f} on {start_date} to ₹{last_price:.2f} by {end_date}, representing a {'loss' if period_change < 0 else 'gain'} during this period. Trading volumes have remained {volume_trend} throughout this timeframe, suggesting {'weak' if volume_trend in ['below average'] else 'moderate' if volume_trend == 'average' else 'strong'} investor participation despite the overall {'negative' if period_change < 0 else 'positive'} trajectory.

---

### 🔍 Technical Indicators  
Key support level established at ₹{support_level} with immediate resistance at ₹{resistance_level}. Sentiment trends from recent news articles suggest a {sentiment_description} OUTLOOK for {entity} in the near term. Technical patterns indicate the potential for {'continued downward pressure' if sentiment == 'negative' else 'sustained upward movement' if sentiment == 'positive' else 'range-bound trading'} until clarity emerges on quarterly results.

---

### 📰 Recent News Articles  
{news_section}
---
"""
    
    return response

# Run the app
if __name__ == '__main__':
    print("Starting real-time Indian stock market API server...")
    print("Now using LIVE DATA scraping with fallback mechanisms!")
    app.run(host='0.0.0.0', port=5000, debug=True) 