"""
Chatbot NLP component for handling user financial queries
"""
import re
import os
from typing import Dict, List, Optional, Any, Tuple
import google.generativeai as genai
from fundwise.nlp.gemini_summarizer import GeminiSummarizer
from fundwise.nlp.news_processor import NewsProcessor

class ChatbotNLP:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize the chatbot NLP component."""
        self.api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print(f"Using Gemini model: gemini-1.5-flash for chatbot")
        
        # Initialize summarizer and news processor
        self.summarizer = GeminiSummarizer(api_key=self.api_key)
        self.news_processor = NewsProcessor(gemini_api_key=self.api_key)
        
        # Keep conversation history for context
        self.conversation_history = []
        
    def detect_intent(self, query: str) -> Dict[str, Any]:
        """Detect the intent of the user query."""
        prompt = f"""
        Categorize this user query related to stocks/finance into one of these intents:
        1. STOCK_PRICE - User is asking about current stock price
        2. STOCK_NEWS - User is asking about recent news for a stock
        3. STOCK_EXPLANATION - User is asking why a stock is up/down
        4. MARKET_OVERVIEW - User is asking about overall market
        5. COMPANY_INFO - User is asking about company information
        6. OTHER - Other financial query
        
        Also extract any stock symbols/tickers mentioned.
        
        Format response as:
        INTENT: [intent category]
        SYMBOLS: [comma-separated stock symbols if any]
        
        Query: {query}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            intent_data = {
                "intent": "OTHER",
                "symbols": []
            }
            
            lines = result.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("INTENT:"):
                    intent_data["intent"] = line.split(":", 1)[1].strip()
                elif line.startswith("SYMBOLS:"):
                    symbols_str = line.split(":", 1)[1].strip()
                    if symbols_str:
                        intent_data["symbols"] = [s.strip().upper() for s in symbols_str.split(',')]
            
            return intent_data
            
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return {"intent": "OTHER", "symbols": []}
    
    def extract_stock_symbol(self, query: str) -> str:
        """Extract stock symbol from query."""
        # Try to extract using the summarizer
        symbols = self.summarizer.extract_stock_symbols(query)
        if symbols:
            return symbols[0]
            
        # Fallback to simple pattern matching
        # Look for ticker patterns like $AAPL or AAPL
        matches = re.findall(r'\$([A-Z]{1,5})|[^A-Za-z]([A-Z]{1,5})[^A-Za-z]', ' ' + query + ' ')
        if matches:
            for match in matches:
                if match[0]:
                    return match[0]
                if match[1]:
                    return match[1]
        
        # Try to match common stock names
        common_stocks = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'amazon': 'AMZN',
            'google': 'GOOGL',
            'tesla': 'TSLA',
            'facebook': 'META',
            'meta': 'META',
            'nvidia': 'NVDA',
            'netflix': 'NFLX',
            'disney': 'DIS'
        }
        
        lower_query = query.lower()
        for name, symbol in common_stocks.items():
            if name in lower_query:
                return symbol
        
        return ""
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and generate a response."""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        # Detect intent and extract symbols
        intent_data = self.detect_intent(query)
        intent = intent_data["intent"]
        symbols = intent_data["symbols"]
        
        # If no symbols detected through intent classification, try direct extraction
        if not symbols:
            symbol = self.extract_stock_symbol(query)
            if symbol:
                symbols = [symbol]
        
        response = {
            "text": "",
            "detected_symbols": symbols,
            "intent": intent
        }
        
        # Handle different intents
        if intent == "STOCK_EXPLANATION" and symbols:
            stock_symbol = symbols[0]
            explanation = self.news_processor.explain_stock_movement(stock_symbol)
            response["text"] = explanation
            
        elif intent == "STOCK_NEWS" and symbols:
            stock_symbol = symbols[0]
            articles = self.news_processor.find_articles_by_symbol(stock_symbol)
            if articles:
                summaries = [f"• {article.get('title', '')}: {article.get('summary', '')}" 
                            for article in articles[:3]]
                response["text"] = f"Recent news about {stock_symbol}:\n\n" + "\n\n".join(summaries)
            else:
                response["text"] = f"No recent news found for {stock_symbol}."
                
        elif intent == "MARKET_OVERVIEW":
            # For market overview, we would use general news
            negative_articles = self.news_processor.find_articles_by_sentiment("Negative", days=1)
            positive_articles = self.news_processor.find_articles_by_sentiment("Positive", days=1)
            
            market_summary = f"Market overview based on recent news:\n\n"
            
            if positive_articles:
                pos_headlines = [f"• {a.get('title', '')}" for a in positive_articles[:2]]
                market_summary += "Positive developments:\n" + "\n".join(pos_headlines) + "\n\n"
                
            if negative_articles:
                neg_headlines = [f"• {a.get('title', '')}" for a in negative_articles[:2]]
                market_summary += "Concerning developments:\n" + "\n".join(neg_headlines)
                
            response["text"] = market_summary
            
        else:
            # For other intents or when no specific handler, use general QA
            context = ""
            
            # If symbols were detected, include relevant article summaries
            if symbols:
                stock_symbol = symbols[0]
                articles = self.news_processor.find_articles_by_symbol(stock_symbol)
                summaries = [article.get('summary', '') for article in articles[:5]]
                context = f"Information about {stock_symbol}:\n\n" + "\n\n".join(summaries)
            
            answer = self.summarizer.answer_stock_question(query, context)
            response["text"] = answer
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response["text"]})
        
        return response
        
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = [] 