#!/usr/bin/env python
"""
Tesla-focused Financial Chat Interface for FundWise NLP
This script provides a command-line interface specifically for asking questions
about Tesla (TSLA) using an enhanced dataset of Tesla news articles.
"""
import sys
import os
import time
from datetime import datetime
import traceback

# Add parent directory to path so we can import the fundwise package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FundWise components
from fundwise.nlp.mock_nlp import MockNLPProcessor
from tesla_data import get_tesla_articles

def print_banner():
    """Print a welcome banner"""
    print("\n" + "=" * 70)
    print("                   Tesla Financial Analyst")
    print("         Ask questions about Tesla stock and company news")
    print("=" * 70)
    print("Type 'exit', 'quit', or 'q' to end the session")
    print("Type 'help' for sample questions")
    print("Type 'list' to see available news articles")
    print("-" * 70 + "\n")

def print_help():
    """Print sample questions that users can ask about Tesla"""
    print("\nSample questions you can ask about Tesla:")
    print("  - Why is TSLA up today?")
    print("  - What's happening with Tesla stock?")
    print("  - Is Tesla facing any recalls?")
    print("  - Tell me about Tesla's recent deliveries")
    print("  - What's new with Tesla Energy?")
    print("  - Is Tesla expanding its charging network?")
    print("  - What are Tesla's profit margins like?")
    print("  - Any news about the Cybertruck?")
    print("-" * 70 + "\n")

def print_article_list(articles):
    """Print a list of available Tesla news articles"""
    print("\nAvailable Tesla News Articles:")
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

def get_article_by_index(articles, index):
    """Get a specific article by its index"""
    try:
        index = int(index)
        if 1 <= index <= len(articles):
            return articles[index-1]
    except:
        pass
    return None

def generate_detailed_answer(question, articles):
    """Generate a more detailed answer based on the question and relevant articles"""
    question_lower = question.lower()
    
    # Extract keywords from question
    keywords = []
    if "up" in question_lower or "rise" in question_lower or "increase" in question_lower or "growth" in question_lower:
        keywords.extend(["record", "exceed", "growth", "increase", "beat", "strong", "positive"])
    if "down" in question_lower or "fall" in question_lower or "decrease" in question_lower or "drop" in question_lower:
        keywords.extend(["recall", "delay", "drops", "fell", "declining", "pressure", "weaker"])
    
    # Add specific topics
    topic_keywords = {
        "delivery": ["delivery", "deliveries", "quarter", "q2", "numbers"],
        "recall": ["recall", "safety", "concern", "issue"],
        "cybertruck": ["cybertruck", "production", "delays"],
        "margin": ["margin", "profit", "revenue", "financial"],
        "energy": ["energy", "solar", "powerwall", "megapack"],
        "charging": ["charging", "supercharger", "network"],
        "fsd": ["fsd", "full self-driving", "autopilot"],
        "model 3": ["model 3", "highland", "refresh"],
    }
    
    for topic, topic_kw in topic_keywords.items():
        if any(kw in question_lower for kw in topic_kw):
            keywords.extend(topic_kw)
    
    # Find relevant articles
    relevant_articles = search_articles_by_keywords(articles, keywords)
    
    if not relevant_articles:
        # If no specific match, return general articles about Tesla
        relevant_articles = articles[:3]
    
    # Construct answer
    if "up" in question_lower or "rise" in question_lower or "increase" in question_lower:
        # Find positive news to explain upward movement
        positive_content = []
        for article in relevant_articles:
            if any(kw in article['title'].lower() + article['content'].lower() for kw in 
                  ["record", "exceed", "beat", "strong", "growth", "increase", "positive", "up"]):
                positive_content.append(f"• {article['title']}: {article['content'][:100]}...")
        
        if positive_content:
            return f"TSLA stock appears to be up due to several positive developments:\n\n" + "\n\n".join(positive_content[:3])
        
    elif "down" in question_lower or "fall" in question_lower or "decrease" in question_lower:
        # Find negative news to explain downward movement
        negative_content = []
        for article in relevant_articles:
            if any(kw in article['title'].lower() + article['content'].lower() for kw in 
                  ["recall", "delay", "drop", "fall", "concern", "risk", "issue", "pressure", "weaker"]):
                negative_content.append(f"• {article['title']}: {article['content'][:100]}...")
        
        if negative_content:
            return f"TSLA stock appears to be down due to several concerning developments:\n\n" + "\n\n".join(negative_content[:3])
    
    # For specific topics
    for topic, topic_kw in topic_keywords.items():
        if any(kw in question_lower for kw in topic_kw):
            topic_content = []
            for article in relevant_articles:
                if any(kw in article['title'].lower() + article['content'].lower() for kw in topic_kw):
                    topic_content.append(f"• {article['title']}: {article['content'][:100]}...")
            
            if topic_content:
                return f"Recent news about Tesla's {topic}:\n\n" + "\n\n".join(topic_content[:3])
    
    # General answer with relevant articles
    summaries = [f"• {article['title']}" for article in relevant_articles[:3]]
    return f"Here's the latest information about Tesla:\n\n" + "\n".join(summaries)

def main():
    """Run the Tesla-focused interactive chat interface"""
    # Initialize the NLP processor
    print("Initializing Tesla financial analysis system...")
    processor = MockNLPProcessor()
    
    # Load Tesla articles
    print("Loading Tesla news articles...")
    tesla_articles = get_tesla_articles()
    for article in tesla_articles:
        processor.process_article(article)
    print(f"Loaded {len(tesla_articles)} Tesla news articles")
    
    # Print welcome banner
    print_banner()
    
    # Main chat loop
    while True:
        # Get user input
        try:
            user_input = input("\nAsk a question about Tesla or TSLA stock: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Tesla Analyst. Goodbye!")
            break
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Exiting Tesla Analyst. Goodbye!")
            break
        
        # Check for help command
        if user_input.lower() == 'help':
            print_help()
            continue
            
        # Check for list command
        if user_input.lower() == 'list':
            print_article_list(tesla_articles)
            continue
            
        # Check for 'read N' command to read a specific article
        if user_input.lower().startswith('read '):
            try:
                article_index = int(user_input.lower().replace('read ', '').strip())
                article = get_article_by_index(tesla_articles, article_index)
                if article:
                    print(f"\n{'-' * 70}")
                    print(f"Title: {article['title']}")
                    print(f"Source: {article['source']} ({article['date']})")
                    print(f"{'-' * 70}")
                    print(f"{article['content']}")
                    print(f"{'-' * 70}")
                    continue
                else:
                    print(f"Article not found. Please enter a number between 1 and {len(tesla_articles)}")
                    continue
            except:
                pass
        
        # Skip empty input
        if not user_input.strip():
            continue
        
        # Process the user's question
        print("\nAnalyzing your question about Tesla...")
        
        try:
            # Extract symbols from the question
            symbols = processor.extract_symbols(user_input)
            if symbols:
                print(f"Detected stock symbols: {', '.join(symbols)}")
            
            # Generate detailed answer using our enhanced Tesla dataset
            answer = generate_detailed_answer(user_input, tesla_articles)
            
            # Display the answer
            print(f"\nAnswer: {answer}\n")
            print("-" * 70)
            
        except Exception as e:
            print(f"Error processing question: {e}")
            traceback.print_exc()
            print("Please try again with a different question")

if __name__ == "__main__":
    main() 