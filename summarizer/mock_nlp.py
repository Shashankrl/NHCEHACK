"""
Mock NLP processor for testing purposes, doesn't require an API key
"""
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

class MockNLPProcessor:
    """Mock NLP processor for testing when API keys are not available"""
    
    def __init__(self):
        """Initialize the mock NLP processor"""
        self.news_database = []
    
    def summarize_text(self, text: str) -> str:
        """Generate a simple summary by extracting the first sentence"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        if sentences:
            # Return first sentence as summary
            return sentences[0]
        return "No summary available"
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Simple sentiment analysis based on keyword matching"""
        text = text.lower()
        
        # Positive keywords
        positive_words = ["increase", "rise", "up", "gain", "growth", "profit", "positive", 
                          "strong", "success", "beat", "exceed", "higher", "record"]
        
        # Negative keywords
        negative_words = ["decrease", "drop", "down", "decline", "loss", "negative", 
                          "weak", "fail", "miss", "lower", "concern", "risk", "issue"]
        
        # Count occurrences
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Determine sentiment
        if positive_count > negative_count:
            label = "Positive"
            score = min(0.5 + (positive_count - negative_count) * 0.1, 0.9)
            factors = [word for word in positive_words if word in text][:3]
        elif negative_count > positive_count:
            label = "Negative"
            score = min(0.5 + (negative_count - positive_count) * 0.1, 0.9)
            factors = [word for word in negative_words if word in text][:3]
        else:
            label = "Neutral"
            score = 0.5
            factors = []
            
        return {
            "label": label,
            "score": score,
            "factors": factors
        }
    
    def extract_symbols(self, text: str) -> List[str]:
        """Extract stock symbols from text using regex patterns"""
        # Find patterns like $AAPL or ticker: AAPL
        matches = re.findall(r'\$([A-Z]{1,5})|ticker[s]?[:]\s*([A-Z]{1,5})', text)
        
        # Also try to find company names
        company_symbols = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "amazon": "AMZN",
            "google": "GOOGL",
            "tesla": "TSLA",
            "facebook": "META",
            "netflix": "NFLX",
            "nvidia": "NVDA"
        }
        
        symbols = []
        
        # Add symbols from regex
        for match in matches:
            if match[0]:
                symbols.append(match[0])
            if match[1]:
                symbols.append(match[1])
        
        # Add symbols from company names
        text_lower = text.lower()
        for company, symbol in company_symbols.items():
            if company in text_lower:
                symbols.append(symbol)
        
        # Remove duplicates and return
        return list(set(symbols))
    
    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process a news article with mock NLP analysis"""
        # Extract the article text
        article_text = article.get('content', '') or article.get('text', '') or article.get('body', '')
        title = article.get('title', '')
        source = article.get('source', '') or article.get('publisher', '')
        url = article.get('url', '') or article.get('link', '')
        published_date = article.get('date', '') or article.get('published', '') or datetime.now().strftime('%Y-%m-%d')
        
        # Combine title and content for better context
        full_text = f"{title}\n\n{article_text}"
        
        # Process with mock methods
        summary = self.summarize_text(full_text)
        sentiment = self.analyze_sentiment(full_text)
        symbols = self.extract_symbols(full_text)
        
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
        
        # Add to database
        self.news_database.append(processed_article)
        
        return processed_article
    
    def batch_process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple articles"""
        return [self.process_article(article) for article in articles]
    
    def find_articles_by_symbol(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """Find articles related to a symbol"""
        symbol = symbol.upper()
        return [article for article in self.news_database 
                if symbol in article.get('related_symbols', [])]
    
    def find_articles_by_sentiment(self, sentiment: str = "Negative", days: int = 7) -> List[Dict[str, Any]]:
        """Find articles with a specific sentiment"""
        sentiment = sentiment.capitalize()
        return [article for article in self.news_database 
                if article.get('sentiment', {}).get('label', '') == sentiment]
    
    def answer_question(self, question: str, context: str = "") -> str:
        """Generate a simple answer to a question"""
        question = question.lower()
        
        # Extract symbols from question
        symbols = self.extract_symbols(question)
        symbol_text = symbols[0] if symbols else "the stock"
        
        # Check question intent
        if "why" in question and any(word in question for word in ["up", "rise", "increase"]):
            return f"{symbol_text} is up due to positive market sentiment and recent favorable news coverage."
        
        elif "why" in question and any(word in question for word in ["down", "fall", "decrease"]):
            return f"{symbol_text} is down due to market concerns and recent negative press coverage."
        
        elif "news" in question or "happening" in question:
            return f"Recent news about {symbol_text} includes quarterly earnings reports and market analysis."
        
        elif "should" in question and "invest" in question:
            return "I cannot provide investment advice. Please consult with a financial advisor for personalized recommendations."
        
        else:
            return f"I don't have specific information about {symbol_text} at this time." 