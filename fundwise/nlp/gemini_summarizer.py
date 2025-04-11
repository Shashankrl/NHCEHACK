"""
Gemini-powered text summarization for financial news articles
"""
import os
from datetime import datetime
import google.generativeai as genai
from typing import Dict, List, Optional, Union, Any

class GeminiSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini API for summarization."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Get available models
        try:
            # Use the more current Gemini 1.5 models
            model_name = "gemini-1.5-flash"
            self.model = genai.GenerativeModel(model_name)
            print(f"Using Gemini model: {model_name}")
        except Exception as e:
            print(f"Error initializing Gemini models: {e}")
            # Create model with default name, may not work but allows class to initialize
            self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def summarize_article(self, article_text: str, max_length: int = 200) -> str:
        """Generate a concise summary of a financial news article."""
        prompt = f"""
        Summarize this financial news article in a clear, concise way. 
        Focus on key financial implications, market impact, and important facts.
        Keep it under {max_length} characters.
        
        Article: {article_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary."
    
    def analyze_sentiment(self, text: str) -> Dict[str, Union[str, float, List[str]]]:
        """Analyze sentiment of financial text."""
        prompt = f"""
        Analyze the sentiment of this financial news text and provide:
        1. Overall sentiment (Positive/Negative/Neutral)
        2. Confidence score (0-1)
        3. Key factors influencing the sentiment

        Format your response as:
        Sentiment: [sentiment]
        Score: [score between 0-1]
        Factor: [factor1]
        Factor: [factor2]
        Factor: [factor3]
        
        Text: {text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Parse the response
            sentiment_data = {
                "label": "Neutral",
                "score": 0.5,
                "factors": []
            }
            
            lines = result.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("Sentiment:"):
                    sentiment_data["label"] = line.split(":", 1)[1].strip()
                elif line.startswith("Score:"):
                    try:
                        sentiment_data["score"] = float(line.split(":", 1)[1].strip())
                    except:
                        pass
                elif line.startswith("Factor:"):
                    factor = line.split(":", 1)[1].strip()
                    sentiment_data["factors"].append(factor)
            
            return sentiment_data
        
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {"label": "Neutral", "score": 0.5, "factors": ["Error in analysis"]}
    
    def extract_stock_symbols(self, text: str) -> List[str]:
        """Extract stock symbols mentioned in text."""
        prompt = f"""
        Extract stock tickers/symbols mentioned in this text.
        Return only the symbols as a comma-separated list.
        
        Text: {text}
        
        Symbols:
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Parse symbols (comma or newline separated)
            symbols = []
            for item in result.replace(',', ' ').split():
                clean_symbol = item.strip().upper()
                if clean_symbol and len(clean_symbol) <= 5:  # Most stock symbols are 1-5 characters
                    symbols.append(clean_symbol)
            
            return symbols
        
        except Exception as e:
            print(f"Error extracting stock symbols: {e}")
            return []
    
    def answer_stock_question(self, question: str, context: str) -> str:
        """Answer a question about stocks based on context."""
        prompt = f"""
        You are a financial expert assistant. Answer the following question 
        about stocks using the provided context information.
        Be concise, accurate and focus on financial implications.
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error answering question: {e}")
            return "I'm unable to answer this question at the moment."
            
    def get_stock_impact_explanation(self, stock_symbol: str, news_articles: List[str]) -> str:
        """Explain why a stock might be up or down based on recent news."""
        combined_news = "\n\n".join(news_articles)
        
        prompt = f"""
        Explain why {stock_symbol} stock might be moving today, based on these recent news articles.
        Focus on cause and effect relationships. Be concise and factual.
        
        News articles:
        {combined_news}
        
        Explanation:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating stock impact explanation: {e}")
            return f"Unable to explain {stock_symbol} movement based on available news."
    
    # Add process_article method for compatibility with MockNLPProcessor
    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process a news article with Gemini NLP analysis"""
        # Extract the article text
        article_text = article.get('content', '') or article.get('text', '') or article.get('body', '')
        title = article.get('title', '')
        source = article.get('source', '') or article.get('publisher', '')
        url = article.get('url', '') or article.get('link', '')
        published_date = article.get('date', '') or article.get('published', '') or datetime.now().strftime('%Y-%m-%d')
        
        # Combine title and content for better context
        full_text = f"{title}\n\n{article_text}"
        
        # Process with Gemini API
        summary = self.summarize_article(full_text)
        sentiment = self.analyze_sentiment(full_text)
        symbols = self.extract_stock_symbols(full_text)
        
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
        
        return processed_article 