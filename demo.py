"""
MyFi NewsSense Demo
A simple demonstration of the enhanced NLP features
"""

import sys
import tempfile
import webbrowser
import time
from datetime import datetime

# Import required modules
from fundwise.nlp.enhanced_nlp import EnhancedNLPProcessor
from market_data import get_market_articles
from nifty_data import get_nifty_news_articles, get_nifty_price_data

def main():
    print("\n" + "=" * 70)
    print("                MyFi NewsSense Demo")
    print("           Powered by enhanced NLP with visualizations")
    print("=" * 70)
    
    # Initialize the NLP processor
    print("\nInitializing MyFi NewsSense NLP system...")
    nlp_processor = EnhancedNLPProcessor()
    
    # Load data
    print("Loading news articles...")
    articles = get_market_articles() + get_nifty_news_articles()
    print(f"Loaded {len(articles)} financial news articles")
    
    print("Loading price data...")
    price_data = get_nifty_price_data()
    
    print("\nDemonstrating key features:\n")
    
    # 1. Sentiment Analysis with Emojis
    print("1. SENTIMENT ANALYSIS WITH EMOJIS")
    print("-" * 70)
    
    # Analyze a sample article with negative sentiment
    negative_article = next((a for a in articles if "down" in a["title"].lower()), articles[0])
    neg_analysis = nlp_processor.analyze_article(negative_article)
    print(f"Article: {negative_article['title']}")
    print(f"Sentiment: {neg_analysis['sentiment']['classification']} {neg_analysis['sentiment']['emoji']}")
    print(f"Score: {neg_analysis['sentiment']['compound']:.4f}")
    
    # Analyze a sample article with positive sentiment
    positive_article = next((a for a in articles if any(word in a["title"].lower() for word in ["up", "rise", "surge"])), articles[1])
    pos_analysis = nlp_processor.analyze_article(positive_article)
    print(f"\nArticle: {positive_article['title']}")
    print(f"Sentiment: {pos_analysis['sentiment']['classification']} {pos_analysis['sentiment']['emoji']}")
    print(f"Score: {pos_analysis['sentiment']['compound']:.4f}")
    
    # 2. Entity Recognition
    print("\n\n2. ENTITY RECOGNITION")
    print("-" * 70)
    sample_text = "NIFTY fell 2% today due to global concerns, while SBI Mutual Fund reported strong growth. HDFC AMC launched a new fund targeting the Nifty Next 50."
    entities = nlp_processor.extract_entities(sample_text)
    
    print(f"Sample text: {sample_text}")
    print("\nExtracted entities:")
    for entity in entities:
        if entity.get("type") == "FINANCIAL_ENTITY":
            print(f"- {entity['text']} → Normalized to: {entity.get('normalized', entity['text'])} (Financial Entity)")
        else:
            print(f"- {entity['text']} ({entity.get('type', 'Unknown')})")
    
    # 3. Interactive Visualization
    print("\n\n3. INTERACTIVE VISUALIZATION")
    print("-" * 70)
    
    # Analyze articles for a specific entity (NIFTY)
    entity = "NIFTY"
    entity_articles = []
    for article in articles:
        if entity.lower() in (article["title"] + article["content"]).lower():
            article["analysis"] = nlp_processor.analyze_article(article)
            entity_articles.append(article)
    
    # Create a graph
    print(f"Creating visualization for {entity} with price data and sentiment...")
    graph_data = nlp_processor.create_sentiment_graph(
        entity_articles, 
        entity=entity,
        include_price_data=True,
        price_data=price_data
    )
    
    # Create HTML and show in browser
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        html_path = f.name
    
    # Create HTML content with the graph
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MyFi NewsSense - {entity} Demo</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            .chart-container {{ width: 100%; height: 600px; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>📊 {entity} Analysis - Interactive Visualization Demo</h1>
        <p>This visualization demonstrates dual-axis graphs showing price and sentiment data with contextual annotations.</p>
        <div class="chart-container" id="chart"></div>
        <script>
            var graphData = {graph_data['graph_json']};
            Plotly.newPlot('chart', graphData.data, graphData.layout);
        </script>
    </body>
    </html>
    """
    
    # Write to the temp file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open in browser
    print(f"Opening graph in your browser...")
    webbrowser.open('file://' + html_path)
    
    # 4. Fund Comparison
    print("\n\n4. FUND COMPARISON")
    print("-" * 70)
    
    # Compare two funds/indices
    entity1 = "NIFTY"
    entity2 = "SBI"
    print(f"Comparing {entity1} with {entity2}:")
    
    if price_data and entity1 in price_data and entity2 in price_data:
        entity1_change = ((price_data[entity1][-1] - price_data[entity1][0]) / price_data[entity1][0]) * 100
        entity2_change = ((price_data[entity2][-1] - price_data[entity2][0]) / price_data[entity2][0]) * 100
        
        emoji1 = "📈" if entity1_change > 0 else "📉"
        emoji2 = "📈" if entity2_change > 0 else "📉"
        
        print(f"{entity1}: {emoji1} {entity1_change:.2f}% over the last 30 days")
        print(f"{entity2}: {emoji2} {entity2_change:.2f}% over the last 30 days")
        
        if entity1_change > entity2_change:
            print(f"\n{entity1} has outperformed {entity2} by {(entity1_change - entity2_change):.2f}%")
        else:
            print(f"\n{entity2} has outperformed {entity1} by {(entity2_change - entity1_change):.2f}%")
    
    # 5. Enhanced Chat Response
    print("\n\n5. ENHANCED CHAT RESPONSE")
    print("-" * 70)
    
    # Format a chat response with emojis and prompts
    sample_response = f"Nifty is down primarily due to global tariff concerns. Foreign institutional investors were net sellers. The market may remain volatile in the near term as investors assess the impact of tariff policies."
    
    analysis_context = {
        "sentiment": {"classification": "negative"},
        "primary_entity": "NIFTY"
    }
    
    formatted_response = nlp_processor.format_chat_response(sample_response, analysis_context)
    print(formatted_response)
    
    # Conclusion
    print("\n\nDemonstration Complete!")
    print("=" * 70)
    print("These features have been integrated into both the web interface (flask_app.py)")
    print("and the command-line chat interface (nifty_chat.py).")
    print("=" * 70)
    
    time.sleep(3)  # Give time to read the output

if __name__ == "__main__":
    main() 