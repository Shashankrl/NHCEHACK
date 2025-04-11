"""
Financial news processor to handle various news sources
"""
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
from fundwise.nlp.gemini_summarizer import GeminiSummarizer

class NewsProcessor:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize the news processor with NLP capabilities."""
        self.summarizer = GeminiSummarizer(api_key=gemini_api_key)
        self.news_database = []  # In-memory store of processed news
        
    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process a news article with NLP enrichment."""
        # Extract the article text
        article_text = article.get('content', '') or article.get('text', '') or article.get('body', '')
        title = article.get('title', '')
        source = article.get('source', '') or article.get('publisher', '')
        url = article.get('url', '') or article.get('link', '')
        published_date = article.get('date', '') or article.get('published', '') or datetime.now().strftime('%Y-%m-%d')
        
        # Combine title and text for better context
        full_text = f"{title}\n\n{article_text}"
        
        # Get summary, sentiment and symbols
        try:
            summary = self.summarizer.summarize_article(full_text)
            sentiment = self.summarizer.analyze_sentiment(full_text)
            symbols = self.summarizer.extract_stock_symbols(full_text)
        except Exception as e:
            summary = f"Error processing article: {str(e)}"
            sentiment = {"label": "Neutral", "score": 0.5, "factors": []}
            symbols = []
        
        # Create processed article
        processed_article = {
            'title': title,
            'source': source,
            'url': url,
            'date': published_date,
            'summary': summary,
            'sentiment': sentiment,
            'related_symbols': symbols,
            'original_text': article_text,
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to in-memory database
        self.news_database.append(processed_article)
        
        return processed_article
    
    def batch_process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple articles."""
        processed = []
        for article in articles:
            processed.append(self.process_article(article))
        return processed
    
    def find_articles_by_symbol(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """Find articles related to a specific stock symbol within recent days."""
        symbol = symbol.upper()
        cutoff_date = (datetime.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')
        
        relevant_articles = []
        for article in self.news_database:
            try:
                article_date = article.get('date', '1900-01-01')
                if article_date >= cutoff_date:
                    if symbol in article.get('related_symbols', []):
                        relevant_articles.append(article)
            except Exception:
                continue
                
        return relevant_articles
    
    def find_articles_by_sentiment(self, sentiment: str = "Negative", days: int = 7) -> List[Dict[str, Any]]:
        """Find articles with specific sentiment."""
        sentiment = sentiment.capitalize()
        cutoff_date = (datetime.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')
        
        relevant_articles = []
        for article in self.news_database:
            try:
                article_date = article.get('date', '1900-01-01')
                if article_date >= cutoff_date:
                    if article.get('sentiment', {}).get('label', '') == sentiment:
                        relevant_articles.append(article)
            except Exception:
                continue
                
        return relevant_articles
    
    def explain_stock_movement(self, stock_symbol: str) -> str:
        """Explain why a stock might be moving based on recent news."""
        # Find relevant articles
        articles = self.find_articles_by_symbol(stock_symbol, days=3)  # Focus on very recent news
        
        if not articles:
            return f"No recent news found about {stock_symbol}."
            
        # Extract text for explanation
        article_texts = [article.get('original_text', '') for article in articles]
        
        # Use summarizer to explain
        explanation = self.summarizer.get_stock_impact_explanation(stock_symbol, article_texts)
        return explanation
        
    def answer_financial_question(self, question: str) -> str:
        """Answer a financial question."""
        # Extract potential stock symbols from the question
        potential_symbols = self.summarizer.extract_stock_symbols(question)
        
        context = ""
        if potential_symbols:
            # Get articles for the first detected symbol
            symbol = potential_symbols[0]
            articles = self.find_articles_by_symbol(symbol, days=7)
            
            # Create context from articles
            summaries = [article.get('summary', '') for article in articles]
            context = "\n\n".join(summaries)
        
        if not context:
            return "I don't have enough information to answer this question accurately."
            
        # Get answer from summarizer
        answer = self.summarizer.answer_stock_question(question, context)
        return answer 