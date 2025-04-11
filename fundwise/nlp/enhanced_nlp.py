"""
Enhanced NLP Processor for FundWise
This module provides advanced NLP capabilities including sentiment analysis,
entity recognition, and keyword extraction for financial news analysis.
"""
import os
import json
import datetime
import emoji
import re
from typing import Dict, List, Any, Tuple, Optional

try:
    import spacy
    spacy_available = True
except ImportError:
    spacy_available = False

import yake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EnhancedNLPProcessor:
    """Enhanced NLP processor with sentiment analysis, entity recognition, and visualization."""
    
    def __init__(self):
        """Initialize the Enhanced NLP processor with required models and analyzers."""
        # Load spaCy model for entity recognition if available
        self.spacy_available = spacy_available
        
        if self.spacy_available:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                print("Successfully loaded spaCy model")
            except (OSError, ImportError) as e:
                print(f"Could not load spaCy model: {str(e)}")
                print("Using fallback NLP approach")
                self.spacy_available = False
        
        # Initialize VADER sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize YAKE keyword extractor
        self.keyword_extractor = yake.KeywordExtractor(
            lan="en", 
            n=2,  # extract 1-2 word keywords
            dedupLim=0.9, 
            dedupFunc='seqm', 
            windowsSize=1, 
            top=10  # extract top 10 keywords
        )
        
        # Dictionary of stock/fund symbols and their alternative names
        self.entity_mapping = {
            "NIFTY": ["nifty", "nifty50", "nifty 50", "sensex"],
            "AAPL": ["apple", "iphone", "apple inc", "tim cook"],
            "MSFT": ["microsoft", "azure", "microsoft corporation", "satya nadella"],
            "AMZN": ["amazon", "amazon.com", "aws", "bezos"],
            "GOOGL": ["google", "alphabet", "youtube", "sundar pichai"],
            "META": ["facebook", "meta platforms", "instagram", "zuckerberg"],
            "NVDA": ["nvidia", "nvidia corporation", "jensen huang"],
            "TSLA": ["tesla", "tesla motors", "elon musk", "cybertruck"],
            "SBI": ["sbi mutual fund", "sbi amc", "state bank of india amc"]
        }
        
        # Dictionary mapping entity types to emoji
        self.emoji_mapping = {
            "up": "📈",
            "down": "📉",
            "news": "📰",
            "positive": "🔼",
            "negative": "🔽",
            "neutral": "➡️",
            "stock": "💹",
            "fund": "💰",
            "technology": "💻",
            "energy": "⚡",
            "finance": "💸",
            "market": "📊"
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of text using VADER.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing sentiment scores and classification
        """
        scores = self.sentiment_analyzer.polarity_scores(text)
        
        # Determine sentiment classification
        if scores['compound'] >= 0.05:
            classification = "positive"
            emoji_icon = self.emoji_mapping["positive"]
        elif scores['compound'] <= -0.05:
            classification = "negative"
            emoji_icon = self.emoji_mapping["negative"]
        else:
            classification = "neutral"
            emoji_icon = self.emoji_mapping["neutral"]
            
        return {
            "scores": scores,
            "classification": classification,
            "emoji": emoji_icon,
            "compound": scores['compound']
        }
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text using spaCy or fallback approach.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of entities with their types and normalized forms
        """
        entities = []
        
        # Extract named entities using spaCy if available
        if self.spacy_available:
            doc = self.nlp(text)
            for ent in doc.ents:
                entity_info = {
                    "text": ent.text,
                    "type": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                }
                entities.append(entity_info)
        
        # Look for financial entities using our custom mapping
        for symbol, alternatives in self.entity_mapping.items():
            text_lower = text.lower()
            for alt in alternatives:
                if alt in text_lower:
                    entity_info = {
                        "text": alt,
                        "normalized": symbol,
                        "type": "FINANCIAL_ENTITY",
                        "start": text_lower.find(alt),
                        "end": text_lower.find(alt) + len(alt)
                    }
                    entities.append(entity_info)
        
        # Fallback approach: use regex to find potential entities if spaCy isn't available
        if not self.spacy_available:
            # Look for capitalized words that might be company names
            potential_orgs = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
            for org in potential_orgs:
                if len(org) > 1 and org not in ["I", "A", "The"]:
                    entity_info = {
                        "text": org,
                        "type": "ORG",
                        "start": text.find(org),
                        "end": text.find(org) + len(org)
                    }
                    entities.append(entity_info)
            
            # Look for dollar amounts
            money_entities = re.findall(r'\$\d+(?:\.\d+)?(?:\s?[mb]illion)?|\d+(?:\.\d+)?\s?(?:dollars|rupees|₹)', text, re.IGNORECASE)
            for money in money_entities:
                entity_info = {
                    "text": money,
                    "type": "MONEY",
                    "start": text.find(money),
                    "end": text.find(money) + len(money)
                }
                entities.append(entity_info)
            
            # Look for percentage values
            percent_entities = re.findall(r'\d+(?:\.\d+)?%', text)
            for percent in percent_entities:
                entity_info = {
                    "text": percent,
                    "type": "PERCENT",
                    "start": text.find(percent),
                    "end": text.find(percent) + len(percent)
                }
                entities.append(entity_info)
        
        return entities
    
    def extract_keywords(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract keywords from text using YAKE.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of keyword tuples (keyword, score) - lower score is better
        """
        keywords = self.keyword_extractor.extract_keywords(text)
        # Sort by score (lower is better in YAKE)
        return sorted(keywords, key=lambda x: x[1])
    
    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a news article.
        
        Args:
            article: Dictionary containing article data
            
        Returns:
            Dictionary with analysis results
        """
        # Combine title and content for analysis
        full_text = f"{article['title']}. {article['content']}"
        
        # Perform sentiment analysis
        sentiment = self.analyze_sentiment(full_text)
        
        # Extract entities
        entities = self.extract_entities(full_text)
        
        # Extract keywords
        keywords = self.extract_keywords(full_text)
        
        # Identify financial entities
        financial_entities = [
            entity for entity in entities 
            if entity.get("type") == "FINANCIAL_ENTITY"
        ]
        
        # Find primary entity (most mentioned)
        entity_counts = {}
        for entity in financial_entities:
            normalized = entity.get("normalized", entity["text"])
            entity_counts[normalized] = entity_counts.get(normalized, 0) + 1
        
        primary_entity = None
        if entity_counts:
            primary_entity = max(entity_counts.items(), key=lambda x: x[1])[0]
        
        # Create result with appropriate emojis
        result = {
            "sentiment": sentiment,
            "entities": entities,
            "financial_entities": financial_entities,
            "primary_entity": primary_entity,
            "keywords": [kw[0] for kw in keywords[:5]],  # Top 5 keywords
            "analysis_date": datetime.datetime.now().isoformat()
        }
        
        # Add emoji for the article based on sentiment and content
        if primary_entity and primary_entity in self.entity_mapping:
            if sentiment["classification"] == "positive":
                result["emoji"] = f"{self.emoji_mapping['stock']} {self.emoji_mapping['up']}"
            elif sentiment["classification"] == "negative":
                result["emoji"] = f"{self.emoji_mapping['stock']} {self.emoji_mapping['down']}"
            else:
                result["emoji"] = f"{self.emoji_mapping['stock']} {self.emoji_mapping['neutral']}"
        else:
            result["emoji"] = f"{self.emoji_mapping['news']}"
        
        return result
    
    def create_sentiment_graph(self, 
                              articles: List[Dict[str, Any]], 
                              entity: str = None,
                              include_price_data: bool = False,
                              price_data: Dict[str, List[float]] = None) -> Dict[str, Any]:
        """
        Create an interactive sentiment graph for a collection of articles.
        
        Args:
            articles: List of analyzed articles
            entity: Optional entity to filter articles by
            include_price_data: Whether to include price data in the graph
            price_data: Optional dictionary with price data
            
        Returns:
            Dictionary with graph data
        """
        # Filter articles if an entity is specified
        if entity:
            filtered_articles = []
            for article in articles:
                if not article.get("analysis"):
                    # Skip articles without analysis
                    continue
                    
                analysis = article["analysis"]
                financial_entities = analysis.get("financial_entities", [])
                entity_symbols = [e.get("normalized", "") for e in financial_entities]
                
                if entity in entity_symbols:
                    filtered_articles.append(article)
            
            articles_to_plot = filtered_articles
        else:
            articles_to_plot = [a for a in articles if a.get("analysis")]
        
        # If no articles to plot, return empty graph
        if not articles_to_plot:
            return {"error": "No articles found for the given entity"}
        
        # Sort articles by date
        articles_to_plot = sorted(articles_to_plot, key=lambda x: x.get("date", ""))
        
        # Extract dates and sentiment scores
        dates = [a.get("date", "") for a in articles_to_plot]
        sentiment_scores = [a.get("analysis", {}).get("sentiment", {}).get("compound", 0) 
                           for a in articles_to_plot]
        titles = [a.get("title", "No title") for a in articles_to_plot]
        
        # Create figure with secondary y-axis if including price data
        if include_price_data and price_data and entity in price_data:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add price data
            price_dates = price_data.get("dates", [])
            price_values = price_data.get(entity, [])
            
            if price_dates and price_values and len(price_dates) == len(price_values):
                fig.add_trace(
                    go.Scatter(
                        x=price_dates,
                        y=price_values,
                        name=f"{entity} Price",
                        line=dict(color="blue")
                    ),
                    secondary_y=False
                )
                
                # Add sentiment data
                fig.add_trace(
                    go.Scatter(
                        x=dates,
                        y=sentiment_scores,
                        name="News Sentiment",
                        mode="markers+lines",
                        marker=dict(
                            size=12,
                            color=["red" if s < 0 else "green" if s > 0 else "gray" 
                                  for s in sentiment_scores],
                            symbol=["triangle-down" if s < 0 else "triangle-up" if s > 0 else "circle" 
                                   for s in sentiment_scores]
                        ),
                        text=titles,
                        hovertemplate="%{text}<br>Sentiment: %{y:.2f}<extra></extra>"
                    ),
                    secondary_y=True
                )
                
                # Set axis titles
                fig.update_yaxes(title_text=f"{entity} Price", secondary_y=False)
                fig.update_yaxes(title_text="Sentiment Score", secondary_y=True)
                
                # Add annotations for significant news events
                for i, score in enumerate(sentiment_scores):
                    if abs(score) > 0.5:  # Only annotate significant sentiment articles
                        fig.add_annotation(
                            x=dates[i],
                            y=sentiment_scores[i],
                            text=f"{self.emoji_mapping['news']}",
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor="black",
                            arrowwidth=1,
                            ax=0,
                            ay=-40,
                            secondary_y=True
                        )
            
        else:
            # Create simple sentiment graph
            fig = go.Figure()
            
            # Add sentiment data
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=sentiment_scores,
                    name="News Sentiment",
                    mode="markers+lines",
                    marker=dict(
                        size=12,
                        color=["red" if s < 0 else "green" if s > 0 else "gray" 
                              for s in sentiment_scores],
                        symbol=["triangle-down" if s < 0 else "triangle-up" if s > 0 else "circle" 
                               for s in sentiment_scores]
                    ),
                    text=titles,
                    hovertemplate="%{text}<br>Sentiment: %{y:.2f}<extra></extra>"
                )
            )
            
            # Add a horizontal line at y=0
            fig.add_shape(
                type="line",
                x0=min(dates),
                y0=0,
                x1=max(dates),
                y1=0,
                line=dict(color="gray", width=1, dash="dash")
            )
            
            # Add annotations for news articles
            for i, score in enumerate(sentiment_scores):
                if abs(score) > 0.3:  # Only annotate more significant sentiment articles
                    fig.add_annotation(
                        x=dates[i],
                        y=sentiment_scores[i],
                        text=f"{self.emoji_mapping['news']}",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="black",
                        arrowwidth=1,
                        ax=0,
                        ay=-40
                    )
        
        # Update layout
        entity_title = entity if entity else "Market"
        fig.update_layout(
            title=f"{entity_title} News Sentiment Analysis {self.emoji_mapping['news']}",
            xaxis_title="Date",
            hovermode="closest",
            template="plotly_white"
        )
        
        # Convert to JSON
        graph_json = fig.to_json()
        
        return {
            "graph_json": graph_json,
            "entity": entity,
            "article_count": len(articles_to_plot)
        }
    
    def add_emojis_to_response(self, response: str, analysis: Dict[str, Any]) -> str:
        """
        Add relevant emojis to a text response based on analysis data.
        
        Args:
            response: The original text response
            analysis: Analysis data
            
        Returns:
            Response with emojis added
        """
        # Get sentiment classification
        sentiment = analysis.get("sentiment", {}).get("classification", "neutral")
        
        # Add sentiment emoji
        if sentiment == "positive":
            emoji_prefix = f"{self.emoji_mapping['up']} "
        elif sentiment == "negative":
            emoji_prefix = f"{self.emoji_mapping['down']} "
        else:
            emoji_prefix = f"{self.emoji_mapping['neutral']} "
            
        # Add entity type emoji if available
        primary_entity = analysis.get("primary_entity")
        if primary_entity and "fund" in primary_entity.lower():
            emoji_prefix += f"{self.emoji_mapping['fund']} "
        elif primary_entity:
            emoji_prefix += f"{self.emoji_mapping['stock']} "
        else:
            emoji_prefix += f"{self.emoji_mapping['market']} "
            
        # Add news emoji
        emoji_prefix += f"{self.emoji_mapping['news']} "
        
        return emoji_prefix + response

    def format_chat_response(self, response: str, analysis: Dict[str, Any], add_graph_prompt: bool = True) -> str:
        """
        Format a chat response with emojis and additional prompts.
        
        Args:
            response: The original chat response
            analysis: Analysis data
            add_graph_prompt: Whether to add a prompt about viewing a graph
            
        Returns:
            Formatted response
        """
        # Add emojis to response
        response_with_emojis = self.add_emojis_to_response(response, analysis)
        
        # Add graph prompt if requested
        if add_graph_prompt:
            response_with_emojis += "\n\n(Say 'graph' or 'show chart' to see visual data)"
            
        return response_with_emojis 