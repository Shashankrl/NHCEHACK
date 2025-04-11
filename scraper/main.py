#!/usr/bin/env python
"""
NewsSense - "Why Is My Nifty Down?" - Main Application
This script integrates the news scraper, stock data scraper, and NLP analyzer
to provide answers about stock market movements.
"""
import os
import sys
import logging
import json
import argparse
from datetime import datetime, timedelta
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our components
from scraper.news_scraper import NewsScraperIndia
from scraper.stock_data import StockScraperIndia
from scraper.nlp_analyzer import NLPAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("newssense.log"), logging.StreamHandler()]
)
logger = logging.getLogger("NewsSense")

class NewsSense:
    """Main application class that integrates all components"""
    
    def __init__(self, refresh_interval=3600):
        """Initialize the NewsSense application"""
        logger.info("Initializing NewsSense")
        
        # Initialize components
        self.news_scraper = NewsScraperIndia()
        self.stock_scraper = StockScraperIndia()
        self.nlp_analyzer = NLPAnalyzer()
        
        # Settings
        self.refresh_interval = refresh_interval  # Default refresh every hour
        self.last_refresh_time = None
        
        # Load existing data if available
        self.load_data()
    
    def load_data(self):
        """Load existing data from files"""
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Try to load processed articles
        try:
            if os.path.exists('data/processed_articles.json'):
                with open('data/processed_articles.json', 'r') as f:
                    self.nlp_analyzer.article_cache = json.load(f)
                    logger.info(f"Loaded {len(self.nlp_analyzer.article_cache)} processed articles from file")
        except Exception as e:
            logger.error(f"Error loading processed articles: {str(e)}")
    
    def refresh_data(self, force=False):
        """Refresh data from sources if needed"""
        current_time = datetime.now()
        
        # Check if we need to refresh
        if not force and self.last_refresh_time and (current_time - self.last_refresh_time).total_seconds() < self.refresh_interval:
            logger.info("Using cached data (refresh not needed)")
            return False
        
        logger.info("Refreshing data from sources")
        
        # Scrape news articles
        articles = self.news_scraper.scrape_all_sources(limit_per_source=10)
        
        # Process articles with NLP
        processed_articles = self.nlp_analyzer.process_articles(articles)
        
        # Update last refresh time
        self.last_refresh_time = current_time
        
        logger.info(f"Data refresh complete. Processed {len(processed_articles)} new articles")
        return True
    
    def answer_question(self, question):
        """Answer a question about the stock market"""
        # Refresh data if needed
        self.refresh_data()
        
        # Extract potential stock symbols from the question
        entities = self.nlp_analyzer.extract_entities(question)
        symbols = entities.get('symbols', [])
        
        # If there's a stock symbol, get its current price data
        stock_data = None
        if symbols:
            symbol = symbols[0]
            stock_data = self.stock_scraper.fetch_stock_data(symbol)
        
        # Process the question with NLP analyzer
        answer = self.nlp_analyzer.answer_market_question(question)
        
        # Add current stock data if available
        if stock_data and stock_data['price'] != 'N/A':
            answer += f"\n\nCurrent price for {stock_data['symbol']}: {stock_data['price']} "
            if stock_data['change'] != 'N/A':
                answer += f"({stock_data['change']}, {stock_data['percent_change']}%)"
        
        return answer
    
    def get_market_summary(self):
        """Get a summary of current market conditions"""
        # Refresh data if needed
        self.refresh_data()
        
        # Get basic market data
        try:
            nifty_data = self.stock_scraper.fetch_nifty_data()
            sensex_data = self.stock_scraper.fetch_sensex_data()
            
            market_data = self.stock_scraper.fetch_top_gainers_losers()
            gainers = market_data.get('gainers', [])
            losers = market_data.get('losers', [])
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            nifty_data = sensex_data = None
            gainers = losers = []
        
        # Get NLP-based sentiment analysis
        nlp_summary = self.nlp_analyzer.generate_market_summary()
        
        # Combine the data
        summary = "Market Summary\n"
        summary += "=" * 50 + "\n\n"
        
        if nifty_data and nifty_data['price'] != 'N/A':
            summary += f"NIFTY 50: {nifty_data['price']} ({nifty_data['change']}, {nifty_data['percent_change']}%)\n"
        
        if sensex_data and sensex_data['price'] != 'N/A':
            summary += f"SENSEX: {sensex_data['price']} ({sensex_data['change']}, {sensex_data['percent_change']}%)\n"
        
        summary += "\n" + "=" * 50 + "\n\n"
        summary += nlp_summary
        
        summary += "\n" + "=" * 50 + "\n\n"
        
        if gainers:
            summary += "Top Gainers:\n"
            for i, gainer in enumerate(gainers[:5], 1):
                summary += f"{i}. {gainer['name']} ({gainer['symbol']}): {gainer['price']} ({gainer['percent_change']}%)\n"
            summary += "\n"
        
        if losers:
            summary += "Top Losers:\n"
            for i, loser in enumerate(losers[:5], 1):
                summary += f"{i}. {loser['name']} ({loser['symbol']}): {loser['price']} ({loser['percent_change']}%)\n"
        
        return summary
    
    def start_interactive_mode(self):
        """Start an interactive command-line interface"""
        print("\n" + "=" * 60)
        print("               NewsSense - \"Why Is My Nifty Down?\"")
        print("=" * 60)
        print("Type your questions about stocks, market movements, or news.")
        print("Type 'summary' for a market summary, or 'exit' to quit.")
        print("-" * 60 + "\n")
        
        # Initial data refresh
        print("Initializing and gathering market data...")
        self.refresh_data(force=True)
        print("Ready for questions!")
        
        while True:
            # Get user input
            try:
                user_input = input("\nAsk a question (or type 'summary', 'refresh', 'exit'): ")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting NewsSense. Goodbye!")
                break
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Exiting NewsSense. Goodbye!")
                break
            
            # Check for summary command
            if user_input.lower() == 'summary':
                print("\nGenerating market summary...")
                summary = self.get_market_summary()
                print("\n" + summary)
                continue
            
            # Check for refresh command
            if user_input.lower() == 'refresh':
                print("\nRefreshing data from sources...")
                self.refresh_data(force=True)
                print("Data refresh complete!")
                continue
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Process the question
            print("\nAnalyzing your question...")
            answer = self.answer_question(user_input)
            print("\nAnswer:")
            print(answer)
    
    def start_scraping_daemon(self, interval=3600):
        """Start a background scraping daemon that refreshes data periodically"""
        logger.info(f"Starting scraping daemon with interval {interval} seconds")
        
        while True:
            try:
                self.refresh_data(force=True)
                logger.info(f"Sleeping for {interval} seconds before next refresh")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Scraping daemon stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in scraping daemon: {str(e)}")
                # Sleep a bit before retrying
                time.sleep(60)

def main():
    """Main function to parse arguments and run the application"""
    parser = argparse.ArgumentParser(description='NewsSense - "Why Is My Nifty Down?" application')
    
    # Define command-line arguments
    parser.add_argument('--refresh', action='store_true', help='Force refresh of data')
    parser.add_argument('--daemon', action='store_true', help='Run as a background scraping daemon')
    parser.add_argument('--interval', type=int, default=3600, help='Refresh interval in seconds (default: 3600)')
    parser.add_argument('--question', type=str, help='Ask a question and exit')
    parser.add_argument('--summary', action='store_true', help='Print market summary and exit')
    
    args = parser.parse_args()
    
    # Initialize the application
    app = NewsSense(refresh_interval=args.interval)
    
    # Handle different modes
    if args.daemon:
        app.start_scraping_daemon(interval=args.interval)
    elif args.question:
        if args.refresh:
            app.refresh_data(force=True)
        answer = app.answer_question(args.question)
        print(answer)
    elif args.summary:
        if args.refresh:
            app.refresh_data(force=True)
        summary = app.get_market_summary()
        print(summary)
    else:
        app.start_interactive_mode()

if __name__ == "__main__":
    main() 