#!/usr/bin/env python
"""
Enhanced MyFi NewsSense NLP Chat Interface with Interactive Graphs and Emoji Support
This script provides a command-line interface for asking questions about
Nifty, Indian mutual funds, and market trends with interactive visualization.
"""
import sys
import os
import time
import json
from datetime import datetime
import traceback
from typing import Dict, List, Any, Optional
import re
import webbrowser
import tempfile

# Add parent directory to path if needed
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Plotly for visualization
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import data and NLP modules
from fundwise.nlp.enhanced_nlp import EnhancedNLPProcessor
from market_data import get_market_articles
from nifty_data import get_nifty_news_articles, get_nifty_price_data

def print_banner():
    """Print a welcome banner"""
    print("\n" + "=" * 70)
    print("                MyFi NewsSense - Why is my Nifty down?")
    print("           Financial insights with interactive visualization")
    print("=" * 70)
    print("Type 'exit', 'quit', or 'q' to end the session")
    print("Type 'help' for sample questions")
    print("Type 'list' to see all available news articles")
    print("Type 'market' for the market summary")
    print("Type 'graph' or 'chart' after an answer to visualize the data")
    print("-" * 70 + "\n")

def print_help():
    """Print sample questions that users can ask"""
    print("\n📱 Sample questions you can ask:")
    print("  - Why is Nifty down today? 📉")
    print("  - How is SBI Mutual Fund performing? 💰")
    print("  - Compare Nifty with HDFC AMC 📊")
    print("  - What's happening with Bank Nifty? 🏦")
    print("  - Tell me about market sentiment 📰")
    print("  - How did IT stocks affect Nifty recently? 💻")
    print("  - What's the latest on interest rates? 💸")
    print("  - Show me Nifty performance vs sentiment 📈")
    print("-" * 70 + "\n")

def print_article_list(articles):
    """Print a list of available news articles with emojis"""
    print("\n📰 Available News Articles:")
    print("-" * 70)
    for i, article in enumerate(articles, 1):
        # Get emoji based on title
        emoji = "📉" if any(word in article['title'].lower() for word in ["down", "plunge", "fall", "drop"]) else \
                "📈" if any(word in article['title'].lower() for word in ["up", "rise", "surge", "jump", "gain"]) else "📊"
        
        print(f"{i}. {emoji} {article['title']} ({article['source']}, {article['date']})")
    print("-" * 70 + "\n")

def search_articles_by_keywords(articles, keywords):
    """Search articles for specific keywords"""
    matching_articles = []
    for article in articles:
        # Search in both title and content
        full_text = (article['title'] + ' ' + article['content']).lower()
        if any(keyword.lower() in full_text for keyword in keywords):
            matching_articles.append(article)
    return matching_articles

def search_articles_by_entity(articles, entity):
    """Search articles for a specific entity (fund or index)"""
    entity_mappings = {
        "NIFTY": ["nifty", "nifty50", "nifty 50", "sensex", "market"],
        "SBI": ["sbi", "sbi mutual fund", "sbi amc", "state bank"],
        "HDFC": ["hdfc", "hdfc amc", "hdfc mutual fund", "housing development"],
        "ICICI": ["icici", "icici prudential", "icici mutual fund"],
        "BANKNIFTY": ["bank nifty", "banking index", "financial sector"],
    }
    
    entity = entity.upper()
    if entity not in entity_mappings:
        return []
    
    search_terms = entity_mappings[entity]
    matching_articles = []
    
    for article in articles:
        full_text = (article['title'] + ' ' + article['content']).lower()
        if any(term.lower() in full_text for term in search_terms):
            matching_articles.append(article)
            
    return matching_articles

def get_article_by_index(articles, index):
    """Get a specific article by its index"""
    try:
        index = int(index)
        if 1 <= index <= len(articles):
            return articles[index-1]
    except:
        pass
    return None

def generate_answer(nlp_processor, question, articles, price_data=None):
    """Generate an answer based on the question and relevant articles"""
    question_lower = question.lower()
    
    # Check for entity-specific questions
    entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
    
    # Special case for "why is nifty down" query
    if re.search(r"why\s+is\s+(my\s+)?nifty\s+down", question_lower):
        # Look for articles that explain Nifty's decline
        nifty_articles = search_articles_by_entity(articles, "NIFTY")
        decline_articles = []
        
        for article in nifty_articles:
            if any(word in article['title'].lower() for word in ["down", "plunge", "fall", "drop", "decline"]):
                decline_articles.append(article)
        
        if decline_articles:
            # Analyze articles for sentiment and entities
            analyzed_articles = []
            for article in decline_articles:
                analysis = nlp_processor.analyze_article(article)
                article['analysis'] = analysis
                analyzed_articles.append(article)
            
            # Generate answer from the most relevant article
            main_article = analyzed_articles[0]
            main_title = main_article['title']
            summary = main_article['content'][:150] + "..."
            
            # Find specific reasons mentioned in the content
            reasons = []
            reason_indicators = [
                r"due to ([^\.]+)",
                r"because of ([^\.]+)",
                r"following ([^\.]+)",
                r"amid ([^\.]+)",
                r"as ([^\.]+) concerns"
            ]
            
            for pattern in reason_indicators:
                matches = re.findall(pattern, main_article['content'])
                if matches:
                    reasons.extend(matches)
            
            reason_text = "; ".join(reasons) if reasons else "various market factors"
            
            # Format response with emojis and prompt for visualization
            response = f"Nifty is down primarily due to {reason_text}. {main_title}\n\n{summary}"
            
            # Add analysis context for the response formatter
            analysis_context = {
                "sentiment": {"classification": "negative"},
                "primary_entity": "NIFTY"
            }
            
            # Format the response with emojis
            formatted_response = nlp_processor.format_chat_response(response, analysis_context)
            
            # Create graph data that will be used if user asks for visualization
            graph_data = nlp_processor.create_sentiment_graph(
                analyzed_articles, 
                entity="NIFTY",
                include_price_data=True,
                price_data=price_data
            )
            
            return {
                "text": formatted_response,
                "graph_data": graph_data,
                "entity": "NIFTY"
            }
    
    # Extract mentioned entities from question
    mentioned_entities = [entity for entity in entities if entity.lower() in question_lower]
    
    # Also check for entity names
    entity_names = {
        "nifty": "NIFTY",
        "sensex": "NIFTY",
        "sbi mutual fund": "SBI",
        "sbi amc": "SBI",
        "hdfc mutual fund": "HDFC",
        "hdfc amc": "HDFC",
        "icici prudential": "ICICI",
        "bank nifty": "BANKNIFTY"
    }
    
    for name, symbol in entity_names.items():
        if name in question_lower and symbol not in mentioned_entities:
            mentioned_entities.append(symbol)
    
    # Extract topic keywords from question
    keywords = []
    
    # Performance keywords
    if any(word in question_lower for word in ["up", "rise", "increase", "gain", "growing"]):
        keywords.extend(["growth", "exceed", "record", "jump", "strong", "beat", "positive"])
    if any(word in question_lower for word in ["down", "fall", "decrease", "drop", "declining"]):
        keywords.extend(["drop", "decline", "fall", "challenge", "pressure", "concern", "negative"])
    
    # Specific comparison questions
    compare_match = re.search(r"compare\s+(\w+)\s+with\s+(\w+)", question_lower)
    if compare_match:
        entity1 = compare_match.group(1).upper()
        entity2 = compare_match.group(2).upper()
        
        if entity1 in entities and entity2 in entities:
            entity1_articles = search_articles_by_entity(articles, entity1)
            entity2_articles = search_articles_by_entity(articles, entity2)
            
            # Analyze performance from articles and price data
            if price_data and entity1 in price_data and entity2 in price_data:
                entity1_change = ((price_data[entity1][-1] - price_data[entity1][0]) / price_data[entity1][0]) * 100
                entity2_change = ((price_data[entity2][-1] - price_data[entity2][0]) / price_data[entity2][0]) * 100
                
                comparison_text = f"Over the last 30 days, {entity1} has moved {entity1_change:.2f}% while {entity2} moved {entity2_change:.2f}%. "
                
                if entity1_change > entity2_change:
                    comparison_text += f"{entity1} has outperformed {entity2}. "
                else:
                    comparison_text += f"{entity2} has outperformed {entity1}. "
                
                # Add news context if available
                if entity1_articles and entity2_articles:
                    comparison_text += f"\n\nRecent news for {entity1}: {entity1_articles[0]['title']}"
                    comparison_text += f"\n\nRecent news for {entity2}: {entity2_articles[0]['title']}"
                
                # Add analysis context for the response formatter
                analysis_context = {
                    "sentiment": {"classification": "neutral"},
                    "primary_entity": entity1
                }
                
                # Format response
                formatted_response = nlp_processor.format_chat_response(comparison_text, analysis_context)
                
                # Prepare the comparison graph
                fig = make_subplots(specs=[[{"secondary_y": False}]])
                
                # Normalize price data for comparison (starting at 100)
                entity1_normalized = [price * 100 / price_data[entity1][0] for price in price_data[entity1]]
                entity2_normalized = [price * 100 / price_data[entity2][0] for price in price_data[entity2]]
                
                fig.add_trace(
                    go.Scatter(
                        x=price_data["dates"],
                        y=entity1_normalized,
                        name=entity1,
                        line=dict(color="blue")
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=price_data["dates"],
                        y=entity2_normalized,
                        name=entity2,
                        line=dict(color="red")
                    )
                )
                
                fig.update_layout(
                    title=f"Comparison: {entity1} vs {entity2} (Base 100)",
                    xaxis_title="Date",
                    yaxis_title="Normalized Price (Base 100)",
                    hovermode="x unified",
                    template="plotly_white"
                )
                
                graph_data = {
                    "graph_json": fig.to_json(),
                    "entity": f"{entity1} vs {entity2}",
                    "article_count": len(entity1_articles) + len(entity2_articles)
                }
                
                return {
                    "text": formatted_response,
                    "graph_data": graph_data,
                    "entity": f"{entity1} vs {entity2}"
                }
    
    # Find relevant articles
    relevant_articles = []
    
    # First priority: entity-specific articles if an entity was mentioned
    if mentioned_entities:
        for entity in mentioned_entities:
            entity_articles = search_articles_by_entity(articles, entity)
            relevant_articles.extend(entity_articles)
    
    # Second priority: topic-specific articles
    if keywords and (not relevant_articles or len(relevant_articles) < 3):
        topic_articles = search_articles_by_keywords(articles, keywords)
        for article in topic_articles:
            if article not in relevant_articles:
                relevant_articles.append(article)
    
    # Fallback: return general market articles
    if not relevant_articles:
        market_keywords = ["market", "index", "sector", "trend", "stock"]
        relevant_articles = search_articles_by_keywords(articles, market_keywords)
    
    # Still nothing? Just return the most recent articles
    if not relevant_articles:
        relevant_articles = articles[:3]
    
    # Limit to top 3 most relevant articles
    relevant_articles = relevant_articles[:3]
    
    # Analyze relevant articles
    for article in relevant_articles:
        article['analysis'] = nlp_processor.analyze_article(article)
    
    # Determine the main entity being discussed
    entity_counts = {}
    for article in relevant_articles:
        financial_entities = article['analysis'].get('financial_entities', [])
        for entity in financial_entities:
            if 'normalized' in entity:
                norm = entity['normalized']
                entity_counts[norm] = entity_counts.get(norm, 0) + 1
    
    main_entity = None
    if entity_counts:
        main_entity = max(entity_counts.items(), key=lambda x: x[1])[0]
    
    # Construct answer based on question type
    # For entity performance questions
    if mentioned_entities and any(word in question_lower for word in ["how", "performance", "performing", "doing"]):
        entity = mentioned_entities[0]
        
        # Use price data if available
        price_trend = ""
        if price_data and entity in price_data:
            start_price = price_data[entity][0]
            end_price = price_data[entity][-1]
            percent_change = ((end_price - start_price) / start_price) * 100
            trend = "up" if percent_change > 0 else "down"
            
            price_trend = f"{entity} is {trend} {abs(percent_change):.2f}% over the last 30 days. "
            
            # Add recent movement
            recent_change = ((price_data[entity][-1] - price_data[entity][-2]) / price_data[entity][-2]) * 100
            price_trend += f"Most recently, it moved {recent_change:.2f}% in the last day. "
        
        # Add news context
        news_insights = []
        for article in relevant_articles:
            sentiment = article['analysis']['sentiment']['classification']
            news_insights.append(f"• {article['title']} ({sentiment})")
        
        answer = f"{price_trend}\n\nRecent news about {entity}:\n\n" + "\n".join(news_insights)
        
        # Add analysis context for the response formatter
        analysis_context = {
            "sentiment": {"classification": "positive" if percent_change > 0 else "negative"},
            "primary_entity": entity
        }
        
        # Format response
        formatted_response = nlp_processor.format_chat_response(answer, analysis_context)
        
        # Prepare graph data
        graph_data = nlp_processor.create_sentiment_graph(
            relevant_articles, 
            entity=entity,
            include_price_data=True,
            price_data=price_data
        )
        
        return {
            "text": formatted_response,
            "graph_data": graph_data,
            "entity": entity
        }
    
    # For general inquiries about mentioned entities
    elif mentioned_entities:
        entity = mentioned_entities[0]
        
        # Prepare a summary from articles
        summaries = []
        for article in relevant_articles:
            sentiment = article['analysis']['sentiment']['classification']
            sentiment_emoji = "📈" if sentiment == "positive" else "📉" if sentiment == "negative" else "📊"
            summaries.append(f"• {sentiment_emoji} {article['title']}: {article['content'][:100]}...")
        
        answer = f"Here's the latest information about {entity}:\n\n" + "\n\n".join(summaries)
        
        # Add analysis context for the response formatter
        analysis_context = {
            "sentiment": {"classification": "neutral"},
            "primary_entity": entity
        }
        
        # Format response
        formatted_response = nlp_processor.format_chat_response(answer, analysis_context)
        
        # Prepare graph data
        graph_data = nlp_processor.create_sentiment_graph(
            relevant_articles, 
            entity=entity,
            include_price_data=True,
            price_data=price_data
        )
        
        return {
            "text": formatted_response,
            "graph_data": graph_data,
            "entity": entity
        }
    
    # For general market or topic inquiries
    else:
        # Determine if there's a specific topic
        topics = {
            "interest rates": ["interest", "rates", "rbi", "reserve bank", "monetary policy"],
            "it sector": ["it stocks", "technology", "tech stocks", "software", "infotech"],
            "banking": ["bank", "banking", "financial", "finance", "banks"],
            "market sentiment": ["sentiment", "mood", "investor confidence", "market view"]
        }
        
        detected_topic = None
        for topic, keywords in topics.items():
            if any(kw in question_lower for kw in keywords):
                detected_topic = topic
                break
        
        # Prepare summaries
        summaries = []
        for article in relevant_articles:
            sentiment = article['analysis']['sentiment']['classification']
            sentiment_emoji = "📈" if sentiment == "positive" else "📉" if sentiment == "negative" else "📊"
            summaries.append(f"• {sentiment_emoji} {article['title']}: {article['content'][:100]}...")
        
        if detected_topic:
            answer = f"Here's the latest information about {detected_topic}:\n\n" + "\n\n".join(summaries)
        else:
            answer = f"Here's some relevant market information:\n\n" + "\n\n".join(summaries)
        
        # Add analysis context for the response formatter
        analysis_context = {
            "sentiment": {"classification": "neutral"},
            "primary_entity": main_entity if main_entity else "NIFTY"
        }
        
        # Format response
        formatted_response = nlp_processor.format_chat_response(answer, analysis_context)
        
        # Prepare graph data
        graph_data = nlp_processor.create_sentiment_graph(
            relevant_articles, 
            entity=main_entity,
            include_price_data=main_entity is not None,
            price_data=price_data
        )
        
        return {
            "text": formatted_response,
            "graph_data": graph_data,
            "entity": main_entity if main_entity else "Market"
        }

def show_graph(graph_data):
    """Display an interactive graph from graph data"""
    if not graph_data or "graph_json" not in graph_data:
        print("📊 No graph data available to display.")
        return
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        html_path = f.name
        
    # Create HTML content with the graph
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MyFi NewsSense - {graph_data.get('entity', 'Market')} Chart</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            .chart-container {{ width: 100%; height: 600px; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>📊 {graph_data.get('entity', 'Market')} Analysis</h1>
        <div class="chart-container" id="chart"></div>
        <script>
            var graphData = {graph_data['graph_json']};
            Plotly.newPlot('chart', graphData.data, graphData.layout);
        </script>
    </body>
    </html>
    """
    
    # Write to the temp file
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    # Open in browser
    webbrowser.open('file://' + html_path)
    print(f"📊 Displaying graph for {graph_data.get('entity', 'Market')} in your browser...")

def main():
    """Main function to run the chat interface"""
    print_banner()
    
    try:
        print("Initializing MyFi NewsSense NLP system...")
        nlp_processor = EnhancedNLPProcessor()
        
        print("Loading news articles...")
        # Combine market and Nifty articles
        articles = get_market_articles() + get_nifty_news_articles()
        print(f"Loaded {len(articles)} financial news articles covering multiple companies and sectors")
        
        print("Loading price data...")
        price_data = get_nifty_price_data()
        
        # Main interaction loop
        last_response = None
        
        while True:
            print("\n----------------------------------------------------------------------")
            question = input("Ask a question 👉 ").strip()
            print("----------------------------------------------------------------------\n")
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("Thanks for using MyFi NewsSense! Goodbye! 👋")
                break
                
            if question.lower() == 'help':
                print_help()
                continue
                
            if question.lower() == 'list':
                print_article_list(articles)
                continue
            
            # Check for graph request
            if question.lower() in ['graph', 'chart', 'show chart', 'show graph'] and last_response:
                if 'graph_data' in last_response:
                    show_graph(last_response['graph_data'])
                else:
                    print("📊 No graph data available for the previous response.")
                continue
            
            # Generate answer
            print("Analyzing your question...")
            try:
                response = generate_answer(nlp_processor, question, articles, price_data)
                print(response['text'])
                last_response = response
            except Exception as e:
                print(f"Sorry, I encountered an error while processing your question: {str(e)}")
                traceback.print_exc()
                last_response = None
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 