#!/usr/bin/env python
"""
Comprehensive Market Chat Interface for FundWise NLP
This script provides a command-line interface for asking questions about
multiple companies, sectors, and market trends using an enhanced dataset.
"""
import sys
import os
import time
from datetime import datetime
import traceback
from typing import Dict, List, Any

# Add parent directory to path so we can import the fundwise package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FundWise components and data
from fundwise.nlp.mock_nlp import MockNLPProcessor
from market_data import get_market_articles
from tesla_data import get_tesla_articles

def print_banner():
    """Print a welcome banner"""
    print("\n" + "=" * 70)
    print("                FundWise Market Intelligence")
    print("         Ask questions about stocks, sectors, and market trends")
    print("=" * 70)
    print("Type 'exit', 'quit', or 'q' to end the session")
    print("Type 'help' for sample questions")
    print("Type 'companies' to see available companies")
    print("Type 'list' to see all available news articles")
    print("-" * 70 + "\n")

def print_help():
    """Print sample questions that users can ask"""
    print("\nSample questions you can ask:")
    print("  - Why is AAPL stock up today?")
    print("  - What's happening with MSFT?")
    print("  - Tell me about NVDA's new chip")
    print("  - How is Google's cloud business performing?")
    print("  - What are the recent developments in AI?")
    print("  - Tell me about the semiconductor sector")
    print("  - What's the latest on interest rates?")
    print("  - How is META's advertising business?")
    print("  - What's new with Amazon's delivery network?")
    print("  - What's going on with oil prices?")
    print("-" * 70 + "\n")

def print_companies():
    """Print a list of available companies in the dataset"""
    print("\nAvailable Companies in the Dataset:")
    print("-" * 70)
    companies = [
        "AAPL (Apple) - iPhone, App Store, consumer electronics",
        "MSFT (Microsoft) - Cloud, Azure, gaming, enterprise software",
        "AMZN (Amazon) - E-commerce, AWS, logistics, streaming",
        "GOOGL (Alphabet/Google) - Search, cloud, advertising, AI",
        "META (Meta Platforms) - Social media, advertising, AI, metaverse",
        "NVDA (NVIDIA) - GPUs, AI chips, data center, automotive",
        "TSLA (Tesla) - Electric vehicles, energy, autonomy"
    ]
    for company in companies:
        print(f"• {company}")
    print("-" * 70 + "\n")

def print_article_list(articles):
    """Print a list of available news articles"""
    print("\nAvailable News Articles:")
    print("-" * 70)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']} ({article['source']}, {article['date']})")
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

def search_articles_by_company(articles, company_symbol):
    """Search articles for a specific company symbol"""
    company_mappings = {
        "AAPL": ["apple", "iphone", "app store"],
        "MSFT": ["microsoft", "azure", "xbox", "windows"],
        "AMZN": ["amazon", "aws", "bezos"],
        "GOOGL": ["google", "alphabet", "youtube", "gemini"],
        "META": ["meta", "facebook", "instagram", "zuckerberg"],
        "NVDA": ["nvidia", "gpu", "blackwell"],
        "TSLA": ["tesla", "musk", "cybertruck", "electric vehicle"]
    }
    
    company_symbol = company_symbol.upper()
    if company_symbol not in company_mappings:
        return []
    
    search_terms = company_mappings[company_symbol]
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

def generate_answer(question, articles):
    """Generate an answer based on the question and relevant articles"""
    question_lower = question.lower()
    
    # Check for company-specific questions
    company_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "TSLA"]
    mentioned_companies = [symbol for symbol in company_symbols if symbol.lower() in question_lower]
    
    # Also check for company names
    company_names = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "amazon": "AMZN",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "meta": "META",
        "facebook": "META",
        "nvidia": "NVDA",
        "tesla": "TSLA"
    }
    
    for name, symbol in company_names.items():
        if name in question_lower and symbol not in mentioned_companies:
            mentioned_companies.append(symbol)
    
    # Extract topic keywords from question
    keywords = []
    
    # Stock movement keywords
    if "up" in question_lower or "rise" in question_lower or "increase" in question_lower:
        keywords.extend(["growth", "exceed", "record", "jump", "strong", "beat"])
    if "down" in question_lower or "fall" in question_lower or "decrease" in question_lower:
        keywords.extend(["drop", "decline", "fall", "challenge", "pressure", "concern"])
    
    # Specific topics
    topic_keywords = {
        "cloud": ["cloud", "azure", "aws", "infrastructure"],
        "ai": ["ai", "artificial intelligence", "machine learning", "model", "generative"],
        "semiconductor": ["chip", "semiconductor", "gpu", "processor", "taiwan"],
        "gaming": ["game", "gaming", "xbox", "studio"],
        "delivery": ["delivery", "logistics", "fulfillment", "shipping"],
        "advertising": ["ad", "advertising", "revenue", "marketing"],
        "privacy": ["privacy", "data", "regulation", "compliance"],
        "interest rates": ["fed", "federal reserve", "interest rate", "cut", "inflation"],
        "energy": ["energy", "oil", "price", "opec", "production"]
    }
    
    for topic, topic_kw in topic_keywords.items():
        if any(kw in question_lower for kw in topic_kw):
            keywords.extend(topic_kw)
    
    # Find relevant articles
    relevant_articles = []
    
    # First priority: company-specific articles if a company was mentioned
    if mentioned_companies:
        for company in mentioned_companies:
            company_articles = search_articles_by_company(articles, company)
            relevant_articles.extend(company_articles)
    
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
    
    # Construct answer based on question type
    # For stock movement questions
    if "why" in question_lower and ("up" in question_lower or "down" in question_lower or "moving" in question_lower):
        if not mentioned_companies:
            return "To answer why a stock is moving, I need to know which company you're asking about. Please specify a company symbol or name."
        
        company = mentioned_companies[0]
        movement_type = "up" if "up" in question_lower else "down"
        
        # Find articles explaining the movement
        movement_articles = []
        for article in relevant_articles:
            title_content = article['title'].lower() + ' ' + article['content'].lower()
            
            # For upward movement
            if movement_type == "up" and any(term in title_content for term in ["beat", "exceed", "record", "jump", "growth", "strong", "positive"]):
                movement_articles.append(article)
            
            # For downward movement
            elif movement_type == "down" and any(term in title_content for term in ["miss", "fall", "drop", "concern", "risk", "challenge", "pressure", "negative"]):
                movement_articles.append(article)
        
        if movement_articles:
            summaries = [f"• {article['title']}: {article['content'][:100]}..." for article in movement_articles]
            return f"{company} stock appears to be {movement_type} due to these factors:\n\n" + "\n\n".join(summaries)
        else:
            # Use the relevant articles even if they don't explicitly mention up/down
            summaries = [f"• {article['title']}" for article in relevant_articles]
            return f"Recent news about {company} that may be affecting the stock price:\n\n" + "\n".join(summaries)
    
    # For general company inquiries
    elif mentioned_companies:
        company = mentioned_companies[0]
        summaries = [f"• {article['title']}: {article['content'][:100]}..." for article in relevant_articles]
        return f"Here's the latest information about {company}:\n\n" + "\n\n".join(summaries)
    
    # For sector or topic inquiries
    else:
        # Try to identify the main topic
        main_topic = None
        for topic, topic_kw in topic_keywords.items():
            if any(kw in question_lower for kw in topic_kw):
                main_topic = topic
                break
        
        if main_topic:
            summaries = [f"• {article['title']}: {article['content'][:100]}..." for article in relevant_articles]
            return f"Here's the latest information about {main_topic}:\n\n" + "\n\n".join(summaries)
        else:
            summaries = [f"• {article['title']}: {article['content'][:100]}..." for article in relevant_articles]
            return f"Here's some relevant market information:\n\n" + "\n\n".join(summaries)

def main():
    """Run the comprehensive market chat interface"""
    # Initialize the NLP processor
    print("Initializing FundWise Market Intelligence system...")
    processor = MockNLPProcessor()
    
    # Load all articles
    print("Loading market news articles...")
    market_articles = get_market_articles()
    tesla_articles = get_tesla_articles()
    all_articles = market_articles + tesla_articles
    
    # Process articles with NLP processor
    for article in all_articles:
        processor.process_article(article)
    
    print(f"Loaded {len(all_articles)} financial news articles covering multiple companies and sectors")
    
    # Print welcome banner
    print_banner()
    
    # Main chat loop
    while True:
        # Get user input
        try:
            user_input = input("\nAsk a question about the market or specific companies: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting FundWise Market Intelligence. Goodbye!")
            break
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Exiting FundWise Market Intelligence. Goodbye!")
            break
        
        # Check for help command
        if user_input.lower() == 'help':
            print_help()
            continue
        
        # Check for companies command
        if user_input.lower() == 'companies':
            print_companies()
            continue
            
        # Check for list command
        if user_input.lower() == 'list':
            print_article_list(all_articles)
            continue
            
        # Check for 'read N' command to read a specific article
        if user_input.lower().startswith('read '):
            try:
                article_index = int(user_input.lower().replace('read ', '').strip())
                article = get_article_by_index(all_articles, article_index)
                if article:
                    print(f"\n{'-' * 70}")
                    print(f"Title: {article['title']}")
                    print(f"Source: {article['source']} ({article['date']})")
                    print(f"{'-' * 70}")
                    print(f"{article['content']}")
                    print(f"{'-' * 70}")
                    continue
                else:
                    print(f"Article not found. Please enter a number between 1 and {len(all_articles)}")
                    continue
            except:
                pass
        
        # Skip empty input
        if not user_input.strip():
            continue
        
        # Process the user's question
        print("\nAnalyzing your market question...")
        
        try:
            # Extract symbols from the question
            symbols = processor.extract_symbols(user_input)
            if symbols:
                print(f"Detected stock symbols: {', '.join(symbols)}")
            
            # Generate detailed answer using our enhanced dataset
            answer = generate_answer(user_input, all_articles)
            
            # Display the answer
            print(f"\nAnswer: {answer}\n")
            print("-" * 70)
            
        except Exception as e:
            print(f"Error processing question: {e}")
            traceback.print_exc()
            print("Please try again with a different question")

if __name__ == "__main__":
    main() 