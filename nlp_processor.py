import google.generativeai as genai
from datetime import datetime
import re
from typing import List, Dict, Tuple
import pandas as pd
import os

class NLPProcessor:
    def __init__(self, api_key: str = None):
        # Initialize Gemini
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_gemini_response(self, prompt: str) -> str:
        """Get response from Gemini model."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error processing request"
    
    def process_article(self, article_text: str, article_date: str = None) -> Dict:
        """Process a complete article using Gemini API."""
        try:
            # Generate summary
            summary_prompt = f"""
            Please provide a concise summary of the following financial news article, focusing on key events and their potential impact:
            
            {article_text}
            """
            summary = self.get_gemini_response(summary_prompt)
            
            # Analyze sentiment
            sentiment_prompt = f"""
            Analyze the sentiment of this financial news article and provide:
            1. Overall sentiment (Positive/Negative/Neutral)
            2. Confidence score (0-1)
            3. Key factors influencing the sentiment
            
            Article:
            {article_text}
            
            Format your response as:
            Sentiment: [sentiment]
            Score: [score]
            Factor: [factor1]
            Factor: [factor2]
            Factor: [factor3]
            """
            sentiment_response = self.get_gemini_response(sentiment_prompt)
            
            # Extract keywords
            keywords_prompt = f"""
            Extract the most important keywords and phrases from this financial news article, focusing on:
            1. Company names
            2. Financial terms
            3. Market sectors
            4. Key events
            
            Article:
            {article_text}
            
            Format your response as a simple numbered list with one keyword per line:
            1. [keyword1]
            2. [keyword2]
            3. [keyword3]
            etc.
            """
            keywords_response = self.get_gemini_response(keywords_prompt)
            
            # Process sentiment response
            sentiment_lines = sentiment_response.split('\n')
            sentiment_label = "Neutral"
            sentiment_score = 0.5
            sentiment_factors = []
            
            for line in sentiment_lines:
                line = line.strip()
                if line.startswith("Sentiment:"):
                    sentiment_label = line.split(":", 1)[1].strip()
                elif line.startswith("Score:"):
                    try:
                        sentiment_score = float(line.split(":", 1)[1].strip())
                    except:
                        sentiment_score = 0.5
                elif line.startswith("Factor:"):
                    factor = line.split(":", 1)[1].strip()
                    sentiment_factors.append(factor)
            
            # Process keywords
            keywords = []
            for line in keywords_response.split('\n'):
                line = line.strip()
                if re.match(r'^\d+\.', line):
                    keyword = re.sub(r'^\d+\.\s*', '', line)
                    keywords.append(keyword)
            
            return {
                'date': article_date or datetime.now().strftime('%Y-%m-%d'),
                'summary': summary,
                'sentiment': {
                    'label': sentiment_label,
                    'score': sentiment_score,
                    'factors': sentiment_factors
                },
                'keywords': keywords,
                'original_text': article_text
            }
        except Exception as e:
            print(f"Error processing article: {e}")
            return {
                'date': article_date or datetime.now().strftime('%Y-%m-%d'),
                'summary': "Error generating summary",
                'sentiment': {'label': 'Neutral', 'score': 0.5, 'factors': []},
                'keywords': [],
                'original_text': article_text
            }
    
    def answer_question(self, question: str, context: str) -> str:
        """Generate an answer to a question using Gemini."""
        try:
            qa_prompt = f"""
            Based on the following financial news article, answer the question. 
            Focus on explaining the reasons and impacts clearly.
            
            Question: {question}
            
            Article:
            {context}
            """
            return self.get_gemini_response(qa_prompt)
        except Exception as e:
            print(f"Error answering question: {e}")
            return "I'm sorry, I couldn't process that request at the moment."
    
    def find_relevant_articles(self, query: str, articles: List[Dict], 
                             sentiment_filter: str = None, 
                             date_range: Tuple[str, str] = None) -> List[Dict]:
        """Find articles relevant to a query with optional filters."""
        relevant_articles = []
        
        for article in articles:
            # Check date range if specified
            if date_range:
                try:
                    article_date = datetime.strptime(article['date'], '%Y-%m-%d')
                    start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
                    end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
                    if not (start_date <= article_date <= end_date):
                        continue
                except Exception as e:
                    print(f"Error checking date range: {e}")
                    continue
            
            # Check sentiment if specified
            if sentiment_filter and article.get('sentiment', {}).get('label', '').lower() != sentiment_filter.lower():
                continue
            
            # Simple keyword matching instead of API call to save API usage
            if query.lower() in article['original_text'].lower():
                relevant_articles.append(article)
                continue
                
            # Check keywords if available
            keywords = article.get('keywords', [])
            if any(query.lower() in keyword.lower() for keyword in keywords):
                relevant_articles.append(article)
                continue
        
        return relevant_articles 