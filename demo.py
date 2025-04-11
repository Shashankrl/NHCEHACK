#!/usr/bin/env python
"""
NewsSense Demo - Integrate NLP processing with news and financial data
"""

import os
import json
from datetime import datetime, timedelta
from nlp_processor import NLPProcessor
from qa_system import QASystem

class NewsSenseDemo:
    def __init__(self):
        # Check for API key
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("Warning: GEMINI_API_KEY environment variable not set")
            self.api_key = input("Enter your Gemini API key: ")
            os.environ['GEMINI_API_KEY'] = self.api_key
        
        # Initialize NLP components
        self.nlp_processor = NLPProcessor(self.api_key)
        self.qa_system = QASystem(self.nlp_processor)
        
        # Paths for article data
        self.articles_file = "data/processed_articles.json"
        self.raw_articles_file = "data/raw_articles.json"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Load or initialize articles database
        self.articles = self.load_articles()
    
    def load_articles(self):
        """Load processed articles from file or create empty database."""
        try:
            with open(self.articles_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No existing articles database found at {self.articles_file}.")
            print("Starting with empty database.")
            return []
    
    def save_articles(self):
        """Save processed articles to file."""
        with open(self.articles_file, 'w') as f:
            json.dump(self.articles, f, indent=2)
    
    def process_new_articles(self):
        """Process any new articles from the raw articles file."""
        try:
            # Load raw articles that would come from your scraper
            with open(self.raw_articles_file, 'r') as f:
                raw_articles = json.load(f)
            
            # Get existing article URLs to avoid duplicates
            processed_urls = [article.get('url', '') for article in self.articles]
            
            # Process each new article
            new_count = 0
            for article in raw_articles:
                if article.get('url', '') not in processed_urls:
                    processed = self.nlp_processor.process_article(
                        article['content'], 
                        article.get('date')
                    )
                    
                    # Add metadata
                    processed['url'] = article.get('url', '')
                    processed['source'] = article.get('source', '')
                    processed['title'] = article.get('title', '')
                    
                    # Add to database
                    self.articles.append(processed)
                    new_count += 1
            
            print(f"Processed {new_count} new articles.")
            
            # Save updated database
            self.save_articles()
            
        except FileNotFoundError:
            print(f"No raw articles file found at {self.raw_articles_file}.")
            print("Create this file by running your news scraper first.")
    
    def simulate_news_data(self, num_articles=5):
        """Simulate scraped news data for testing."""
        print(f"Simulating {num_articles} financial news articles...")
        
        companies = ["HDFC Bank", "SBI", "Reliance", "TCS", "Infosys", "Nifty", "Sensex"]
        events = [
            {"event": "quarterly results", "sentiment": "Positive"},
            {"event": "regulatory issues", "sentiment": "Negative"},
            {"event": "new product launch", "sentiment": "Positive"},
            {"event": "CEO resignation", "sentiment": "Negative"},
            {"event": "merger announcement", "sentiment": "Positive"},
            {"event": "data breach", "sentiment": "Negative"}
        ]
        
        raw_articles = []
        for i in range(num_articles):
            company = companies[i % len(companies)]
            event = events[i % len(events)]
            days_ago = i % 7
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            # Generate simulated article content
            if event["sentiment"] == "Positive":
                content = f"""
                {company} reported strong performance today after {event['event']}.
                Analysts are bullish on the stock, with multiple brokerages raising their target price.
                The company's management expressed confidence in continued growth.
                Market observers note that this development is likely to have positive ripple effects across the sector.
                """
            else:
                content = f"""
                {company} faced challenges today due to {event['event']}.
                The stock declined as investors reacted to the news.
                Analysts have expressed concerns about short-term headwinds.
                Industry experts are watching closely to see how this might impact the broader market.
                """
            
            article = {
                "title": f"{company} {event['event']} - Market Update",
                "content": content,
                "date": date,
                "url": f"https://example.com/news/{company.lower().replace(' ', '-')}-{i}",
                "source": "Demo Financial News"
            }
            
            raw_articles.append(article)
        
        # Save simulated raw articles
        os.makedirs("data", exist_ok=True)
        with open(self.raw_articles_file, 'w') as f:
            json.dump(raw_articles, f, indent=2)
        
        print(f"Created {num_articles} simulated articles in {self.raw_articles_file}")
    
    def answer_question(self, question):
        """Process a user question and provide an answer."""
        print(f"\nProcessing question: {question}")
        
        if not self.articles:
            return "No articles available. Please process news articles first."
        
        result = self.qa_system.process_question(question, self.articles)
        
        print(f"Found {len(result['relevant_articles'])} relevant articles.")
        print(f"Confidence score: {result['confidence_score']:.2f}")
        
        return result['answer']

def main():
    print("=" * 50)
    print("NewsSense Demo - Financial News QA System")
    print("=" * 50)
    
    demo = NewsSenseDemo()
    
    # Simulate news data if needed
    simulate = input("Simulate news data for testing? (y/n): ").lower() == 'y'
    if simulate:
        num_articles = int(input("How many articles to simulate? (default: 5): ") or "5")
        demo.simulate_news_data(num_articles)
    
    # Process articles
    process = input("Process articles? (y/n): ").lower() == 'y'
    if process:
        demo.process_new_articles()
    
    # Answer questions
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        answer = demo.answer_question(question)
        print("\nAnswer:")
        print(answer)
    
    print("\nThank you for using NewsSense Demo!")

if __name__ == "__main__":
    main() 