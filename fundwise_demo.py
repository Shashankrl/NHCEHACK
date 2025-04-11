"""
FundWise Demo Application
A demonstration of the financial news analysis system
"""
import os
import sys
import time
from datetime import datetime

# Import our NLP processors
try:
    from summarizer.gemini_summarizer import GeminiSummarizer
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

from summarizer.mock_nlp import MockNLPProcessor

class FundWiseDemo:
    def __init__(self):
        """Initialize the FundWise demo application"""
        self.nlp = None
        self.sample_articles = self._load_sample_articles()
        self.setup_nlp()
        
    def setup_nlp(self):
        """Set up the NLP processor, trying Gemini first, then falling back to MockNLP"""
        if HAS_GEMINI:
            try:
                api_key = os.environ.get("GEMINI_API_KEY")
                if api_key:
                    print("Using Gemini NLP processor...")
                    self.nlp = GeminiSummarizer(api_key=api_key)
                    return
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
        
        # Fall back to mock processor
        print("Using Mock NLP processor (no API key required)...")
        self.nlp = MockNLPProcessor()
        
    def _load_sample_articles(self):
        """Load sample financial news articles"""
        return [
            {
                'title': 'Tesla Reports Strong Q2 Earnings',
                'content': 'Tesla Inc. announced better than expected earnings for Q2 2023. Revenue increased by 47% year-over-year, beating analyst expectations. The company cited strong demand for Model Y and production improvements.',
                'source': 'Financial Times',
                'date': '2023-07-20'
            },
            {
                'title': 'Apple Faces Supply Chain Issues',
                'content': 'Apple is experiencing supply chain constraints for its iPhone production. The company warned that this could impact Q3 revenue. Analysts have lowered their expectations due to these concerns.',
                'source': 'Wall Street Journal',
                'date': '2023-07-15'
            },
            {
                'title': 'Microsoft Cloud Business Growth Slows',
                'content': 'Microsoft reported its Q2 results with Azure growth declining to 26% from 31% in the previous quarter. The slowdown in cloud growth has raised concerns among investors about the broader tech sector.',
                'source': 'Bloomberg',
                'date': '2023-07-18'
            },
            {
                'title': 'Amazon Prime Day Sets New Sales Record',
                'content': 'Amazon announced that its Prime Day event set new sales records with over 375 million items purchased worldwide. The company reported that this was the largest Prime Day event in its history.',
                'source': 'CNBC',
                'date': '2023-07-14'
            },
            {
                'title': 'Nvidia Stock Surges on AI Chip Demand',
                'content': 'Nvidia shares jumped 8% today as demand for AI chips continues to surge. The company has been a key beneficiary of the artificial intelligence boom, with its GPUs being essential for training large language models.',
                'source': 'Reuters',
                'date': '2023-07-21'
            }
        ]
    
    def process_all_news(self):
        """Process all news articles in the database"""
        print("\nProcessing news articles...")
        processed = []
        for article in self.sample_articles:
            print(f"Processing: {article['title']}")
            
            # If using the actual Gemini model, we would perform actual API calls
            if isinstance(self.nlp, MockNLPProcessor):
                result = self.nlp.process_article(article)
            else:
                # For GeminiSummarizer, we need to adapt the methods
                summary = self.nlp.summarize_article(article['content'])
                sentiment = self.nlp.analyze_sentiment(article['content'])
                symbols = self.nlp.extract_stock_symbols(article['content'])
                
                result = {
                    'title': article['title'],
                    'source': article['source'],
                    'date': article['date'],
                    'summary': summary,
                    'sentiment': sentiment,
                    'related_symbols': symbols,
                    'original_text': article['content']
                }
            
            processed.append(result)
            time.sleep(0.5)  # Add a small delay for demo purposes
        
        return processed
    
    def display_processed_news(self, articles):
        """Display processed news in a readable format"""
        print("\n" + "=" * 60)
        print("FUNDWISE FINANCIAL NEWS ANALYSIS".center(60))
        print("=" * 60)
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']} | Date: {article['date']}")
            print(f"   Summary: {article['summary']}")
            
            sentiment = article['sentiment']
            if isinstance(sentiment, dict) and 'label' in sentiment:
                print(f"   Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
                if 'factors' in sentiment and sentiment['factors']:
                    print(f"   Key factors: {', '.join(sentiment['factors'])}")
            else:
                print(f"   Sentiment: {sentiment}")
                
            symbols = article['related_symbols']
            if symbols:
                print(f"   Related stocks: {', '.join(symbols)}")
            print("-" * 60)
    
    def chat_interface(self, articles):
        """Simple chat interface for asking questions about stocks"""
        print("\n" + "=" * 60)
        print("FUNDWISE CHAT ASSISTANT".center(60))
        print("=" * 60)
        print("Ask me questions about stocks or type 'exit' to quit.\n")
        
        # Map of company names/keywords to symbols for better matching
        symbol_mapping = {
            "tesla": ["TSLA", "tesla", "musk", "model y", "electric vehicle"],
            "apple": ["AAPL", "apple", "iphone", "mac", "ios", "cupertino"],
            "microsoft": ["MSFT", "microsoft", "azure", "windows", "satya"],
            "amazon": ["AMZN", "amazon", "prime", "bezos", "aws", "e-commerce"],
            "nvidia": ["NVDA", "nvidia", "graphics", "gpu", "ai chips", "jensen"]
        }
        
        while True:
            question = input("You: ").strip()
            if question.lower() in ('exit', 'quit', 'bye'):
                print("Thank you for using FundWise!")
                break
                
            if not question:
                continue
            
            # Convert question to lowercase for easier matching
            question_lower = question.lower()
            
            # Find matching articles based on company names and stock symbols
            matching_articles = []
            
            # Check for company names and keywords
            for company, keywords in symbol_mapping.items():
                for keyword in keywords:
                    if keyword.lower() in question_lower:
                        # Find symbol for this company
                        symbol = keywords[0]  # First item is always the symbol
                        
                        # Search for articles with this symbol
                        for article in articles:
                            if symbol in article.get('related_symbols', []) and article not in matching_articles:
                                matching_articles.append((article, company, symbol))
            
            # Display results if matches found
            if matching_articles:
                print(f"FundWise: Here's what I found based on your query:")
                for i, (article, company, symbol) in enumerate(matching_articles, 1):
                    print(f"\n{i}. {article['title']} ({symbol})")
                    print(f"   Summary: {article['summary']}")
                    
                    sentiment = article['sentiment']
                    if isinstance(sentiment, dict) and 'label' in sentiment:
                        print(f"   Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
                        if 'factors' in sentiment and sentiment['factors']:
                            factors = ', '.join(sentiment['factors'])
                            print(f"   Key factors: {factors}")
                    else:
                        print(f"   Sentiment: {sentiment}")
                    
                    print(f"   Source: {article['source']} | Date: {article['date']}")
                    
                # If asking about why a stock is up/down, provide a specific response
                if "why" in question_lower and any(term in question_lower for term in ["up", "down", "rising", "falling", "increase", "decrease"]):
                    # Use the first article's sentiment to explain
                    first_article = matching_articles[0][0]
                    sentiment = first_article['sentiment']
                    company_name = matching_articles[0][1].title()
                    
                    if isinstance(sentiment, dict) and sentiment['label'] == 'Positive':
                        print(f"\nFundWise: {company_name} is performing well because of positive factors like: {', '.join(sentiment['factors'])}")
                        print(f"   This has led to positive market sentiment as reported in '{first_article['title']}'")
                    elif isinstance(sentiment, dict) and sentiment['label'] == 'Negative':
                        print(f"\nFundWise: {company_name} is facing challenges due to: {', '.join(sentiment['factors'])}")
                        print(f"   This has led to negative market sentiment as reported in '{first_article['title']}'")
                    else:
                        print(f"\nFundWise: {company_name}'s stock movement is being influenced by recent news as detailed above.")
            else:
                # No specific match found, use default question answering
                if isinstance(self.nlp, MockNLPProcessor):
                    answer = self.nlp.answer_question(question)
                    print(f"FundWise: {answer}")
                else:
                    # Use the most relevant article as context
                    context = self.sample_articles[0]['content'] if self.sample_articles else ""
                    answer = self.nlp.answer_stock_question(question, context)
                    print(f"FundWise: {answer}")
            
            print()  # Add a blank line for readability
    
    def run_demo(self):
        """Run the complete demo"""
        print("\n" + "*" * 70)
        print("WELCOME TO FUNDWISE FINANCIAL NEWS ANALYSIS SYSTEM".center(70))
        print("*" * 70)
        
        print("\nSystem Information:")
        print(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"- NLP Processor: {self.nlp.__class__.__name__}")
        print(f"- Available Articles: {len(self.sample_articles)}")
        
        # Process news once and store for reuse
        processed_articles = self.process_all_news()
        
        # Display results
        self.display_processed_news(processed_articles)
        
        # Chat interface - pass the processed articles to avoid reprocessing
        self.chat_interface(processed_articles)

if __name__ == "__main__":
    demo = FundWiseDemo()
    demo.run_demo() 