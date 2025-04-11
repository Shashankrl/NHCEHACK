"""
NLP analyzer for financial news articles
This module processes scraped news content to generate market insights,
identify sentiment, extract entities, and answer queries.
"""
import re
import os
import json
import logging
import string
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter, defaultdict

# Import our NLP model
from fundwise.nlp.mock_nlp import MockNLPProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("nlp_analyzer.log"), logging.StreamHandler()]
)
logger = logging.getLogger("NLPAnalyzer")

# Download NLTK resources if needed
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
    except Exception as e:
        logger.error(f"Error downloading NLTK resources: {str(e)}")

class NLPAnalyzer:
    """NLP analyzer for financial news articles"""
    
    def __init__(self):
        """Initialize the NLP analyzer"""
        logger.info("Initializing NLP Analyzer")
        self.mock_processor = MockNLPProcessor()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.article_cache = []
        self.processed_cache = {}
        
        # Dictionary mapping company names to stock symbols
        self.company_to_symbol = {
            'reliance': 'RELIANCE',
            'tcs': 'TCS',
            'infosys': 'INFY',
            'hdfc': 'HDFC',
            'hdfc bank': 'HDFCBANK',
            'icici': 'ICICIBANK',
            'itc': 'ITC',
            'kotak': 'KOTAKBANK',
            'hindustan unilever': 'HINDUNILVR',
            'sbi': 'SBIN',
            'bajaj finance': 'BAJFINANCE',
            'bharti airtel': 'BHARTIARTL',
            'asian paints': 'ASIANPAINT',
            'hcl': 'HCLTECH',
            'maruti': 'MARUTI',
            'wipro': 'WIPRO',
            'axis bank': 'AXISBANK',
            'ultratech cement': 'ULTRACEMCO',
            'adani': 'ADANIPORTS',
            'sun pharma': 'SUNPHARMA',
            'jyothy labs': 'JYOTHYLAB',
            'swiggy': 'SWIGGY'
        }
        
        # Keywords related to market downturns and their categories
        self.downturn_keywords = {
            'economic': [
                'recession', 'inflation', 'deflation', 'economic slowdown', 'economic downturn',
                'interest rate', 'rate hike', 'monetary policy', 'fed', 'rbi', 'reserve bank',
                'cpi', 'wpi', 'gdp', 'economic growth', 'slowdown'
            ],
            'company_specific': [
                'profit warning', 'earnings miss', 'revenue decline', 'lower guidance',
                'missed estimates', 'downgrade', 'rating cut', 'debt', 'layoffs', 'restructuring',
                'ceo exit', 'management change', 'accounting issues', 'delay in results'
            ],
            'regulatory': [
                'regulation', 'compliance', 'investigation', 'legal', 'lawsuit', 'penalty',
                'fine', 'tax', 'sebi', 'competition commission', 'antitrust'
            ],
            'global_markets': [
                'global selloff', 'asian markets', 'european markets', 'us markets',
                'foreign investors', 'fii', 'dii', 'foreign outflow', 'foreign selling'
            ],
            'sectoral': [
                'sector rotation', 'sectoral', 'industry downturn', 'pharma', 'it', 'banking',
                'auto', 'metal', 'fmcg', 'energy', 'oil', 'gas'
            ],
            'technical': [
                'technical breakdown', 'support broken', 'resistance', 'bearish pattern',
                'death cross', 'head and shoulders', 'overbought', 'oversold'
            ]
        }
        
        # Initialize all sector-related keywords
        self.sector_keywords = {
            'it': ['information technology', 'software', 'digital', 'tech', 'infotech', 'it services'],
            'banking': ['bank', 'finance', 'financial', 'loan', 'credit', 'deposit', 'lending'],
            'pharma': ['pharmaceutical', 'medicine', 'drug', 'healthcare', 'api', 'clinical'],
            'auto': ['automobile', 'car', 'vehicle', 'auto', 'ev', 'electric vehicle'],
            'fmcg': ['consumer goods', 'fmcg', 'retail', 'household', 'packaged goods'],
            'energy': ['power', 'energy', 'electricity', 'renewable', 'solar', 'wind'],
            'telecom': ['telecom', 'telecommunications', 'mobile', '5g', 'network'],
            'manufacturing': ['manufacturing', 'industrial', 'production', 'factory'],
            'metal': ['steel', 'aluminum', 'copper', 'zinc', 'metal', 'mining'],
            'oil_gas': ['oil', 'gas', 'petroleum', 'refinery', 'crude']
        }
    
    def preprocess_text(self, text):
        """Preprocess text for NLP tasks"""
        if not text:
            return []
            
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Tokenize into words
        words = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words and len(word) > 2]
        
        return words
    
    def extract_entities(self, text):
        """Extract companies, sectors, and other financial entities from text"""
        entities = {
            'companies': [],
            'symbols': [],
            'sectors': [],
            'indices': [],
            'economic_terms': []
        }
        
        # Simple extraction based on keyword dictionaries
        text_lower = text.lower()
        
        # Extract company names and symbols
        for company, symbol in self.company_to_symbol.items():
            if company in text_lower:
                entities['companies'].append(company)
                entities['symbols'].append(symbol)
                
        # Look for stock symbols directly (like RELIANCE, TCS, etc.)
        symbol_pattern = r'\b[A-Z]{2,10}\b'
        potential_symbols = re.findall(symbol_pattern, text)
        for symbol in potential_symbols:
            if symbol in self.company_to_symbol.values() and symbol not in entities['symbols']:
                entities['symbols'].append(symbol)
                
        # Extract sectors
        for sector, keywords in self.sector_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities['sectors'].append(sector)
                    break
        
        # Look for indices
        indices = ['nifty', 'sensex', 'nifty50', 'nifty 50', 'bank nifty', 'nifty bank']
        for index in indices:
            if index in text_lower:
                entities['indices'].append(index)
        
        # Look for economic terms
        economic_terms = [
            'gdp', 'inflation', 'cpi', 'wpi', 'iip', 'fiscal deficit', 'current account',
            'interest rate', 'repo rate', 'monetary policy', 'rbi', 'sebi', 'budget'
        ]
        for term in economic_terms:
            if term in text_lower:
                entities['economic_terms'].append(term)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
            
        return entities
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        return self.mock_processor.analyze_sentiment(text)
    
    def process_article(self, article):
        """Process a single news article"""
        # Check if we've already processed this article (by URL)
        if article.get('url') in self.processed_cache:
            return self.processed_cache[article.get('url')]
            
        # Combine title and content for analysis
        title = article.get('title', '')
        content = article.get('content', '')
        full_text = f"{title}\n\n{content}"
        
        # Extract entities
        entities = self.extract_entities(full_text)
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(full_text)
        
        # Identify market downturn factors if sentiment is negative
        downturn_factors = {}
        if sentiment.get('label') == 'Negative':
            for category, keywords in self.downturn_keywords.items():
                matched_keywords = []
                for keyword in keywords:
                    if keyword in full_text.lower():
                        matched_keywords.append(keyword)
                
                if matched_keywords:
                    downturn_factors[category] = matched_keywords
        
        # Create processed article
        processed = {
            'title': title,
            'url': article.get('url', ''),
            'date': article.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'source': article.get('source', 'Unknown'),
            'entities': entities,
            'sentiment': sentiment,
            'summary': article.get('summary', ''),
            'downturn_factors': downturn_factors,
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Cache the processed article
        self.processed_cache[article.get('url')] = processed
        
        return processed
    
    def process_articles(self, articles):
        """Process multiple articles and build an analysis database"""
        processed_articles = []
        
        for article in articles:
            processed = self.process_article(article)
            processed_articles.append(processed)
            
            # Add to our cache for building the knowledge base
            self.article_cache.append(processed)
        
        # Update our knowledge base with the new articles
        self._update_knowledge_base()
        
        return processed_articles
    
    def _update_knowledge_base(self):
        """Update the knowledge base with processed articles"""
        logger.info("Updating knowledge base")
        
        # This is a simplified approach - in a real system, you might use a database
        # or vector store for more sophisticated retrieval
        
        # Save processed articles to a JSON file
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/processed_articles.json', 'w') as f:
                json.dump(self.article_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {str(e)}")
    
    def find_articles_by_symbol(self, symbol, days=7):
        """Find articles related to a specific stock symbol"""
        symbol = symbol.upper()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        matching_articles = []
        for article in self.article_cache:
            # Check if the article is recent enough
            try:
                article_date = datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                if article_date < cutoff_date:
                    continue
            except:
                # If we can't parse the date, include it anyway
                pass
                
            # Check if the symbol is in the article's entities
            if symbol in article.get('entities', {}).get('symbols', []):
                matching_articles.append(article)
                
        return matching_articles
    
    def find_articles_by_sentiment(self, sentiment_label, days=7):
        """Find articles with a specific sentiment"""
        sentiment_label = sentiment_label.capitalize()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        matching_articles = []
        for article in self.article_cache:
            # Check if the article is recent enough
            try:
                article_date = datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                if article_date < cutoff_date:
                    continue
            except:
                # If we can't parse the date, include it anyway
                pass
                
            # Check if the sentiment matches
            if article.get('sentiment', {}).get('label') == sentiment_label:
                matching_articles.append(article)
                
        return matching_articles
    
    def explain_stock_movement(self, symbol):
        """Explain why a stock might be up or down based on recent news"""
        # Get recent articles about this stock
        symbol = symbol.upper()
        articles = self.find_articles_by_symbol(symbol, days=3)
        
        if not articles:
            return f"No recent news found about {symbol}."
            
        # Count positive vs negative articles
        pos_count = sum(1 for a in articles if a.get('sentiment', {}).get('label') == 'Positive')
        neg_count = sum(1 for a in articles if a.get('sentiment', {}).get('label') == 'Negative')
        
        # Determine overall sentiment
        if pos_count > neg_count:
            direction = "up"
            articles_to_use = [a for a in articles if a.get('sentiment', {}).get('label') == 'Positive']
        else:
            direction = "down"
            articles_to_use = [a for a in articles if a.get('sentiment', {}).get('label') == 'Negative']
            
        if not articles_to_use:
            articles_to_use = articles  # Use all articles if we don't have any with matching sentiment
        
        # Collect reasons
        reasons = []
        
        for article in articles_to_use:
            # For downward movement, look for downturn factors
            if direction == "down" and article.get('downturn_factors'):
                for category, factors in article.get('downturn_factors').items():
                    reason = f"{category.replace('_', ' ').title()} factors: {', '.join(factors)}"
                    reasons.append(reason)
            
            # Add the article title as a reason
            if article.get('title'):
                reasons.append(f"News: {article['title']}")
        
        # Make reasons unique
        unique_reasons = list(set(reasons))
        
        # Construct explanation
        if unique_reasons:
            explanation = f"{symbol} appears to be {direction} due to these factors:\n\n"
            explanation += "\n".join(f"• {reason}" for reason in unique_reasons[:5])
            return explanation
        else:
            return f"{symbol} appears to be {direction}, but the specific reasons are unclear from recent news."
    
    def answer_market_question(self, question):
        """Answer a natural language question about the market"""
        question_lower = question.lower()
        
        # Extract entities from the question
        entities = self.extract_entities(question)
        symbols = entities.get('symbols', [])
        indices = entities.get('indices', [])
        sectors = entities.get('sectors', [])
        
        # Check if this is a "why is X down/up" question
        if "why" in question_lower and symbols:
            symbol = symbols[0]
            if "down" in question_lower or "fall" in question_lower or "decrease" in question_lower:
                return self.explain_stock_movement(symbol)
            elif "up" in question_lower or "rise" in question_lower or "increase" in question_lower:
                return self.explain_stock_movement(symbol)
        
        # If asking about a specific stock
        if symbols:
            symbol = symbols[0]
            articles = self.find_articles_by_symbol(symbol, days=7)
            
            if articles:
                summary = f"Recent news about {symbol}:\n\n"
                for i, article in enumerate(articles[:3], 1):
                    summary += f"{i}. {article['title']} ({article['source']})\n"
                    if article.get('sentiment', {}).get('label'):
                        summary += f"   Sentiment: {article['sentiment']['label']} (score: {article['sentiment'].get('score', 'N/A')})\n"
                return summary
            else:
                return f"No recent news found about {symbol}."
        
        # If asking about indices
        if indices:
            index = indices[0].upper()
            # In a real implementation, we would check our database of index movements
            # For now, we'll just give a generic response
            return f"The {index} index has been affected by recent market volatility. Please check the latest data for specific movements."
        
        # If asking about a sector
        if sectors:
            sector = sectors[0]
            sector_name = sector.replace('_', ' ').upper()
            return f"The {sector_name} sector has been influenced by recent market trends. For detailed analysis, please check the latest sectoral reports."
        
        # Default response
        return "I don't have enough information to answer that question specifically. Please ask about a particular stock, index, or sector."
        
    def generate_market_summary(self):
        """Generate a summary of current market conditions"""
        # Get recent articles (last 2 days)
        cutoff_date = datetime.now() - timedelta(days=2)
        recent_articles = [a for a in self.article_cache if datetime.strptime(a['date'], '%Y-%m-%d %H:%M:%S') >= cutoff_date]
        
        if not recent_articles:
            return "No recent market data available."
        
        # Count sentiment distribution
        sentiment_counts = Counter([a.get('sentiment', {}).get('label') for a in recent_articles])
        
        # Determine overall market sentiment
        total = sum(sentiment_counts.values())
        if total == 0:
            overall_sentiment = "neutral"
        else:
            pos_ratio = sentiment_counts.get('Positive', 0) / total
            neg_ratio = sentiment_counts.get('Negative', 0) / total
            
            if pos_ratio > 0.6:
                overall_sentiment = "very positive"
            elif pos_ratio > 0.4:
                overall_sentiment = "somewhat positive"
            elif neg_ratio > 0.6:
                overall_sentiment = "very negative"
            elif neg_ratio > 0.4:
                overall_sentiment = "somewhat negative"
            else:
                overall_sentiment = "mixed"
        
        # Count mentions of different sectors
        sector_mentions = defaultdict(int)
        for article in recent_articles:
            for sector in article.get('entities', {}).get('sectors', []):
                sector_mentions[sector] += 1
        
        # Identify most discussed sectors
        top_sectors = [s[0].replace('_', ' ').upper() for s in sorted(sector_mentions.items(), key=lambda x: x[1], reverse=True)[:3]]
        
        # Get positive and negative highlights
        positive_articles = [a for a in recent_articles if a.get('sentiment', {}).get('label') == 'Positive']
        negative_articles = [a for a in recent_articles if a.get('sentiment', {}).get('label') == 'Negative']
        
        # Construct summary
        summary = f"Market Sentiment: {overall_sentiment.title()}\n\n"
        
        if top_sectors:
            summary += f"Most discussed sectors: {', '.join(top_sectors)}\n\n"
        
        if positive_articles:
            summary += "Positive highlights:\n"
            for i, article in enumerate(positive_articles[:3], 1):
                summary += f"{i}. {article['title']}\n"
            summary += "\n"
        
        if negative_articles:
            summary += "Concerning developments:\n"
            for i, article in enumerate(negative_articles[:3], 1):
                summary += f"{i}. {article['title']}\n"
        
        return summary

if __name__ == "__main__":
    # Simple test when run directly
    analyzer = NLPAnalyzer()
    
    # Test with a sample article
    test_article = {
        'title': 'Nifty falls 2% as global markets tumble on recession fears',
        'content': 'The Nifty 50 index closed 2% lower on Wednesday as fears of a global recession intensified. Banking stocks were the worst hit, with HDFC Bank and ICICI Bank falling over 3%. The selloff was triggered by weak US economic data and an inverted yield curve, which is often seen as a precursor to recession. Foreign investors pulled out over Rs 3,000 crore from Indian equities. The volatility index, India VIX, surged 15% indicating heightened market anxiety.',
        'source': 'Financial Express',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': 'https://example.com/nifty-falls'
    }
    
    # Process the article
    processed = analyzer.process_article(test_article)
    
    # Print results
    print("Processed Article:")
    print(f"Title: {processed['title']}")
    print(f"Sentiment: {processed['sentiment']['label']} (score: {processed['sentiment']['score']})")
    print(f"Entities:")
    for entity_type, entities in processed['entities'].items():
        if entities:
            print(f"  {entity_type}: {', '.join(entities)}")
    
    if processed['downturn_factors']:
        print("\nDownturn Factors:")
        for category, factors in processed['downturn_factors'].items():
            print(f"  {category}: {', '.join(factors)}")
    
    # Test question answering
    test_question = "Why is HDFC Bank down today?"
    answer = analyzer.answer_market_question(test_question)
    print(f"\nQuestion: {test_question}")
    print(f"Answer: {answer}") 