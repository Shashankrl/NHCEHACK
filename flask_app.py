"""
Simplified Flask Web Application for MyFi NewsSense
This version has minimal dependencies and provides mock data for hackathon demonstration.
"""
import os
import json
import time
import uuid
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'my-secret-key-for-newssense')
CORS(app)  # Enable CORS for all routes

# Mock data for the hackathon demo
mock_articles = [
    {
        "title": "Nifty drops 2% as global markets react to interest rate concerns",
        "source": "Financial Times",
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "content": "Nifty index dropped 2% today as global markets reacted negatively to central bank announcements regarding potential interest rate increases. Banking and technology sectors were the most affected, with major companies reporting significant losses."
    },
    {
        "title": "SBI Mutual Fund outperforms market with 15% annual growth",
        "source": "Economic Times",
        "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "content": "SBI Mutual Fund has reported impressive 15% annual growth, significantly outperforming the broader market. The fund's strategic investments in energy and healthcare sectors have paid off, despite overall market volatility."
    },
    {
        "title": "HDFC Bank announces acquisition plans, shares surge 3%",
        "source": "Business Standard",
        "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "content": "HDFC Bank shares surged 3% following announcement of strategic acquisition plans. The bank's expansion strategy aims to strengthen its position in the competitive financial services market."
    },
    {
        "title": "ICICI introduces new digital banking features, analysts optimistic",
        "source": "Financial Express",
        "date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
        "content": "ICICI Bank has introduced innovative digital banking features, attracting positive responses from analysts. The new technologies are expected to improve customer experience and operational efficiency."
    },
    {
        "title": "Bank Nifty volatility increases amid sector-wide regulatory changes",
        "source": "Money Control",
        "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "content": "Bank Nifty has shown increased volatility as financial institutions adjust to new regulatory requirements. Analysts expect short-term fluctuations but improved stability in the long term."
    }
]

# Mock price data
mock_price_data = {
    "NIFTY": generate_price_data(18500, volatility=0.015),
    "SBI": generate_price_data(550, volatility=0.02, trend=0.005),
    "HDFC": generate_price_data(1650, volatility=0.01, trend=0.003),
    "ICICI": generate_price_data(900, volatility=0.018),
    "BANKNIFTY": generate_price_data(42500, volatility=0.02, trend=-0.002),
}

def generate_price_data(start_price, days=30, volatility=0.01, trend=0):
    """Generate mock price data with specified volatility and trend"""
    prices = [start_price]
    for _ in range(days - 1):
        change = prices[-1] * random.uniform(-volatility, volatility) + (prices[-1] * trend)
        prices.append(max(0.1, prices[-1] + change))  # Ensure price doesn't go too low
    return prices

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to ask a question and get a response with potential graph data"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Process the question (simplified for hackathon)
        entity = extract_entity(question)
        
        # Generate response based on detected entity and question
        if "down" in question.lower() or "drop" in question.lower() or "fall" in question.lower():
            response_text = generate_negative_response(entity)
            has_graph = True
        elif "up" in question.lower() or "rise" in question.lower() or "gain" in question.lower() or "growth" in question.lower():
            response_text = generate_positive_response(entity)
            has_graph = True
        elif "compare" in question.lower():
            response_text = generate_comparison_response(question)
            has_graph = True
        else:
            response_text = generate_general_response(entity)
            has_graph = random.choice([True, False, True])  # Mostly show graphs
        
        return jsonify({
            'text': response_text,
            'has_graph': has_graph,
            'entity': entity
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for the chat interface in the frontend"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Process the question (simplified for hackathon)
        entity = extract_entity(message)
        
        # Generate response based on detected entity and question
        if "down" in message.lower() or "drop" in message.lower() or "fall" in message.lower():
            response_text = generate_negative_response(entity)
            has_graph = True
        elif "up" in message.lower() or "rise" in message.lower() or "gain" in message.lower() or "growth" in message.lower():
            response_text = generate_positive_response(entity)
            has_graph = True
        elif "compare" in message.lower():
            response_text = generate_comparison_response(message)
            has_graph = True
        else:
            response_text = generate_general_response(entity)
            has_graph = random.choice([True, False, True])  # Mostly show graphs
        
        # Generate chart data if needed
        chart_data = None
        if has_graph:
            chart_data = generate_chart_data(entity, message)
        
        result = {
            'id': str(uuid.uuid4()),
            'content': response_text,
            'has_graph': has_graph,
            'entity': entity
        }
        
        if chart_data:
            result['chart_data'] = chart_data
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/graph', methods=['GET'])
def get_graph_data():
    """API endpoint to get the graph data for the last question"""
    question = request.args.get('question', '')
    entity = request.args.get('entity', None)
    
    try:
        # Generate response with graph data
        if not entity:
            entity = extract_entity(question)
        
        chart_data = generate_chart_data(entity, question)
        
            return jsonify({
            'graph_data': chart_data,
            'entity': entity
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entities', methods=['GET'])
def get_entities():
    """API endpoint to get the list of available entities (funds/indices)"""
    entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
    
    # Add descriptions
    entity_descriptions = {
        "NIFTY": "Nifty 50 - India's benchmark stock market index",
        "SBI": "SBI Mutual Fund - India's largest asset management company",
        "HDFC": "HDFC AMC - One of India's leading fund houses",
        "ICICI": "ICICI Prudential - Major financial services provider",
        "BANKNIFTY": "Bank Nifty - Index tracking banking sector stocks"
    }
    
    result = []
    for entity in entities:
        # Get performance data if available
        performance = "N/A"
        if entity in mock_price_data:
            start_price = mock_price_data[entity][0]
            end_price = mock_price_data[entity][-1]
            percent_change = ((end_price - start_price) / start_price) * 100
            performance = f"{percent_change:.2f}%"
        
        result.append({
            'symbol': entity,
            'description': entity_descriptions.get(entity, ""),
            'performance': performance
        })
    
    return jsonify({'entities': result})

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """API endpoint to get the list of news articles"""
    entity_filter = request.args.get('entity', None)
    
    filtered_articles = []
    for article in mock_articles:
        # Include basic article data
        article_data = {
            'title': article['title'],
            'source': article['source'],
            'date': article['date'],
            'snippet': article['content'][:150] + "..."
        }
        
        # Add to results if no filter or matches filter
        if not entity_filter:
            filtered_articles.append(article_data)
        elif entity_filter.upper() in article['title'].upper() or entity_filter.upper() in article['content'].upper():
            filtered_articles.append(article_data)
    
    return jsonify({'articles': filtered_articles})

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """API endpoint to get suggested questions for the chat interface"""
    suggestions = [
        "Why is NIFTY down today?",
        "How is SBI Mutual Fund performing?",
        "Compare NIFTY with HDFC AMC",
        "Explain the banking sector trend",
        "What are the top financial news today?"
    ]
    return jsonify({'suggestions': suggestions})

def extract_entity(question):
    """Extract the entity from the question"""
    entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
    for entity in entities:
        if entity.upper() in question.upper():
            return entity
    return "NIFTY"  # Default to NIFTY if no entity found

def generate_negative_response(entity):
    """Generate a response for negative market movement"""
    responses = [
        f"{entity} has experienced a downturn primarily due to global market uncertainty and foreign institutional investor (FII) outflows. Recent economic data indicating slower growth has triggered risk-off sentiment.",
        f"The decline in {entity} can be attributed to multiple factors: rising inflation concerns, recent regulatory developments, and profit-taking after the previous rally. Technical indicators suggest oversold conditions.",
        f"{entity} is down as investors react to disappointing quarterly results from key constituents. Additionally, concerns about interest rate hikes have pressured valuations across the sector.",
        f"The {entity} downturn reflects broader market anxiety about fiscal policies and international trade tensions. However, domestic institutional buying provides some support at lower levels."
    ]
    return random.choice(responses)

def generate_positive_response(entity):
    """Generate a response for positive market movement"""
    responses = [
        f"{entity} has shown strong upward momentum driven by robust institutional buying and positive economic indicators. Corporate earnings have largely beaten expectations, supporting the rally.",
        f"The impressive performance of {entity} can be attributed to favorable policy announcements, improved liquidity conditions, and renewed foreign investor interest in Indian markets.",
        f"{entity} is trending higher as recent data points to economic resilience and controlled inflation. The outlook remains positive with strong technical support levels.",
        f"The uptrend in {entity} reflects increasing investor confidence in the growth prospects. Sector rotation into these assets suggests a sustainable medium-term rally."
    ]
    return random.choice(responses)

def generate_comparison_response(question):
    """Generate a response comparing entities"""
    entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
    mentioned = []
    
    for entity in entities:
        if entity.upper() in question.upper():
            mentioned.append(entity)
    
    if len(mentioned) < 2:
        # If not enough entities mentioned, add NIFTY as comparison
        if "NIFTY" not in mentioned:
            mentioned.append("NIFTY")
        # If still need one more, add a random one
        if len(mentioned) < 2:
            remaining = [e for e in entities if e not in mentioned]
            mentioned.append(random.choice(remaining))
    
    # Take the first two mentioned entities
    entity1, entity2 = mentioned[:2]
    
    # Get performance data
    perf1 = "stable"
    perf2 = "stable"
    
    if entity1 in mock_price_data and entity2 in mock_price_data:
        start_price1 = mock_price_data[entity1][0]
        end_price1 = mock_price_data[entity1][-1]
        percent_change1 = ((end_price1 - start_price1) / start_price1) * 100
        
        start_price2 = mock_price_data[entity2][0]
        end_price2 = mock_price_data[entity2][-1]
        percent_change2 = ((end_price2 - start_price2) / start_price2) * 100
        
        if percent_change1 > percent_change2 + 1:
            comparison = f"{entity1} has outperformed {entity2} by {abs(percent_change1 - percent_change2):.2f}% over the analyzed period"
        elif percent_change2 > percent_change1 + 1:
            comparison = f"{entity2} has outperformed {entity1} by {abs(percent_change2 - percent_change1):.2f}% over the analyzed period"
        else:
            comparison = f"{entity1} and {entity2} have shown similar performance patterns with less than 1% difference"
            
        if percent_change1 > 0:
            perf1 = "positive"
        elif percent_change1 < 0:
            perf1 = "negative"
            
        if percent_change2 > 0:
            perf2 = "positive"
        elif percent_change2 < 0:
            perf2 = "negative"
    else:
        comparison = f"Comparing {entity1} and {entity2} shows interesting contrasts in their market behavior"
    
    responses = [
        f"Comparative analysis of {entity1} and {entity2}: {comparison}. {entity1} has shown {perf1} momentum influenced by sector-specific factors, while {entity2} has demonstrated {perf2} trends due to its distinctive market positioning.",
        f"{comparison}. The divergence can be explained by different sectoral exposures and institutional investor preferences. {entity1} is more sensitive to global cues, whereas {entity2} responds strongly to domestic economic indicators.",
        f"When analyzing {entity1} versus {entity2}, {comparison}. This reflects their different risk profiles and market capitalization characteristics. Trading volumes indicate shifting investor sentiment between these options."
    ]
    
    return random.choice(responses)

def generate_general_response(entity):
    """Generate a general response about an entity"""
    responses = [
        f"{entity} has been showing mixed signals with periods of consolidation followed by directional moves. Key technical levels to watch include support at recent lows and resistance at the moving averages.",
        f"Analysis of {entity} indicates that market sentiment remains cautiously optimistic despite recent volatility. Institutional positioning suggests accumulation at current levels.",
        f"The outlook for {entity} depends on upcoming economic data releases and policy decisions. Current price action indicates a phase of price discovery with balanced volumes.",
        f"{entity} performance has been influenced by sectoral rotation and liquidity flows. Recent price patterns suggest a potential trend change, though confirmation is needed."
    ]
    return random.choice(responses)

def generate_chart_data(entity, question):
    """Generate chart data for visualization"""
    # Get price data for the entity
    price_data = mock_price_data.get(entity, mock_price_data["NIFTY"])
    
    # Generate dates for the x-axis (last 30 days)
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
    
    # Base chart with price data
    chart_data = [
        {
            "x": dates,
            "y": price_data,
            "type": "scatter",
            "mode": "lines",
            "name": f"{entity} Price",
            "line": {"color": "rgb(75, 192, 192)", "width": 2}
        }
    ]
    
    # If it's a comparison, add the second entity
    if "compare" in question.lower():
        other_entity = None
        for e in ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]:
            if e.upper() in question.upper() and e != entity:
                other_entity = e
                break
        
        if not other_entity:
            # Pick a random different entity
            entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
            other_entities = [e for e in entities if e != entity]
            other_entity = random.choice(other_entities)
        
        other_price_data = mock_price_data.get(other_entity, mock_price_data["SBI"])
        
        # Normalize both datasets for comparison (start at 100)
        base_price = price_data[0]
        normalized_price = [price * 100 / base_price for price in price_data]
        
        other_base_price = other_price_data[0]
        other_normalized_price = [price * 100 / other_base_price for price in other_price_data]
        
        chart_data = [
            {
                "x": dates,
                "y": normalized_price,
                "type": "scatter",
                "mode": "lines",
                "name": entity,
                "line": {"color": "rgb(75, 192, 192)", "width": 2}
            },
            {
                "x": dates,
                "y": other_normalized_price,
                "type": "scatter",
                "mode": "lines",
                "name": other_entity,
                "line": {"color": "rgb(255, 99, 132)", "width": 2}
            }
        ]
    
    # Add layout
    layout = {
        "title": f"{entity} Market Performance",
        "xaxis": {"title": "Date"},
        "yaxis": {"title": "Price"},
        "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
        "paper_bgcolor": "#20232a",
        "plot_bgcolor": "#282c34",
        "font": {"color": "#ffffff"},
        "showlegend": True,
        "legend": {"orientation": "h", "y": -0.2}
    }
    
    return {
        "data": chart_data,
        "layout": layout
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True) 