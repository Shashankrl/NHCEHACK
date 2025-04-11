"""
Web scraper for Indian financial news websites
This module scrapes financial news from Indian sources like Economic Times,
Moneycontrol, and others without using any commercial news APIs.
"""
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime, timedelta
import logging
from urllib.parse import urljoin
import pandas as pd
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()]
)
logger = logging.getLogger("NewsScraperIndia")

# Common Indian stock symbols for demo/testing
COMMON_INDIAN_STOCKS = {
    "RELIANCE": "Reliance Industries Ltd.",
    "TCS": "Tata Consultancy Services Ltd.",
    "HDFCBANK": "HDFC Bank Ltd.",
    "INFY": "Infosys Ltd.",
    "ICICIBANK": "ICICI Bank Ltd.",
    "HINDUNILVR": "Hindustan Unilever Ltd.",
    "SBIN": "State Bank of India",
    "BAJFINANCE": "Bajaj Finance Ltd.",
    "BHARTIARTL": "Bharti Airtel Ltd.",
    "KOTAKBANK": "Kotak Mahindra Bank Ltd.",
    "WIPRO": "Wipro Ltd.",
    "AXISBANK": "Axis Bank Ltd.",
    "ASIANPAINT": "Asian Paints Ltd.",
    "MARUTI": "Maruti Suzuki India Ltd.",
    "TITAN": "Titan Company Ltd."
}

class NewsScraperIndia:
    """Scraper for Indian financial news websites"""
    
    def __init__(self):
        """Initialize the scraper with common headers and settings"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.session = requests.Session()
        self.timeout = 30
        self.news_cache = []
    
    def _make_request(self, url):
        """Make a request with error handling and rate limiting"""
        try:
            # Add random delay to avoid rate limits
            time.sleep(random.uniform(1, 3))
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def _extract_date(self, date_text):
        """Extract a datetime object from various date text formats"""
        try:
            # Try to parse various date formats
            date_text = date_text.strip().lower()
            
            # Current date for relative dates
            now = datetime.now()
            
            # Handle relative dates
            if 'ago' in date_text:
                if 'minute' in date_text:
                    minutes = int(re.search(r'(\d+)', date_text).group(1))
                    return (now - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
                elif 'hour' in date_text:
                    hours = int(re.search(r'(\d+)', date_text).group(1))
                    return (now - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
                elif 'day' in date_text:
                    days = int(re.search(r'(\d+)', date_text).group(1))
                    return (now - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
                elif 'week' in date_text:
                    weeks = int(re.search(r'(\d+)', date_text).group(1))
                    return (now - timedelta(weeks=weeks)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return now.strftime('%Y-%m-%d %H:%M:%S')
            
            # Handle "today" and "yesterday"
            if 'today' in date_text:
                return now.strftime('%Y-%m-%d %H:%M:%S')
            if 'yesterday' in date_text:
                return (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Try common date formats
            # This is a simplified approach - in production, you'd want more robust date parsing
            date_formats = [
                '%d %b %Y',       # 15 Aug 2023
                '%d-%b-%Y',       # 15-Aug-2023
                '%d %B %Y',       # 15 August 2023
                '%B %d, %Y',      # August 15, 2023
                '%d/%m/%Y',       # 15/08/2023
                '%Y-%m-%d',       # 2023-08-15
                '%d.%m.%Y'        # 15.08.2023
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_text, fmt).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
            
            # If we can't parse the date, return current date
            return now.strftime('%Y-%m-%d %H:%M:%S')
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def scrape_economic_times(self, limit=20):
        """Scrape financial news from Economic Times"""
        articles = []
        
        urls = [
            "https://economictimes.indiatimes.com/markets/stocks",
            "https://economictimes.indiatimes.com/markets/stocks/news"
        ]
        
        for url in urls:
            logger.info(f"Scraping Economic Times: {url}")
            html = self._make_request(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract news articles
            news_items = soup.select('.eachStory, .story-box')
            
            for item in news_items[:limit]:
                try:
                    # Extract headline
                    headline_elem = item.select_one('h3, .story_title')
                    if not headline_elem:
                        continue
                    
                    headline = headline_elem.text.strip()
                    
                    # Extract link
                    link_elem = item.select_one('a')
                    if not link_elem or not link_elem.get('href'):
                        continue
                        
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = urljoin("https://economictimes.indiatimes.com", link)
                    
                    # Extract date
                    date_elem = item.select_one('.date-format, .publish_date')
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if date_elem:
                        date = self._extract_date(date_elem.text)
                    
                    # Extract summary if available
                    summary_elem = item.select_one('.content, .story_synopsis')
                    summary = ""
                    if summary_elem:
                        summary = summary_elem.text.strip()
                    
                    # Extract content
                    content = summary
                    if not content and link:
                        # Fetch the full article if we don't have a summary
                        article_html = self._make_request(link)
                        if article_html:
                            article_soup = BeautifulSoup(article_html, 'html.parser')
                            content_elems = article_soup.select('.normal, .artText, .article_content p')
                            if content_elems:
                                content = ' '.join([p.text.strip() for p in content_elems])
                    
                    articles.append({
                        'title': headline,
                        'url': link,
                        'date': date,
                        'summary': summary,
                        'content': content,
                        'source': 'Economic Times'
                    })
                    
                except Exception as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
        
        logger.info(f"Scraped {len(articles)} articles from Economic Times")
        return articles
    
    def scrape_moneycontrol(self, limit=20):
        """Scrape financial news from Moneycontrol"""
        articles = []
        
        urls = [
            "https://www.moneycontrol.com/news/business/markets/",
            "https://www.moneycontrol.com/news/business/stocks/"
        ]
        
        for url in urls:
            logger.info(f"Scraping Moneycontrol: {url}")
            html = self._make_request(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract news articles
            news_items = soup.select('.clearfix, .article_box, li.clearfix')
            
            for item in news_items[:limit]:
                try:
                    # Extract headline
                    headline_elem = item.select_one('h2, .article_title')
                    if not headline_elem:
                        continue
                    
                    headline = headline_elem.text.strip()
                    
                    # Extract link
                    link_elem = item.select_one('a')
                    if not link_elem or not link_elem.get('href'):
                        continue
                        
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = urljoin("https://www.moneycontrol.com", link)
                    
                    # Extract date
                    date_elem = item.select_one('.article_schedule, .publish_date')
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if date_elem:
                        date = self._extract_date(date_elem.text)
                    
                    # Extract summary if available
                    summary_elem = item.select_one('.article_desc, .desc')
                    summary = ""
                    if summary_elem:
                        summary = summary_elem.text.strip()
                    
                    # Extract content
                    content = summary
                    if not content and link:
                        # Fetch the full article if we don't have a summary
                        article_html = self._make_request(link)
                        if article_html:
                            article_soup = BeautifulSoup(article_html, 'html.parser')
                            content_elems = article_soup.select('.content_wrapper p, .article-desc')
                            if content_elems:
                                content = ' '.join([p.text.strip() for p in content_elems])
                    
                    articles.append({
                        'title': headline,
                        'url': link,
                        'date': date,
                        'summary': summary,
                        'content': content,
                        'source': 'Moneycontrol'
                    })
                    
                except Exception as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
        
        logger.info(f"Scraped {len(articles)} articles from Moneycontrol")
        return articles
    
    def scrape_financial_express(self, limit=20):
        """Scrape financial news from Financial Express"""
        articles = []
        
        urls = [
            "https://www.financialexpress.com/market/",
            "https://www.financialexpress.com/market/stock-market/"
        ]
        
        for url in urls:
            logger.info(f"Scraping Financial Express: {url}")
            html = self._make_request(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract news articles
            news_items = soup.select('.list-item, .story-article')
            
            for item in news_items[:limit]:
                try:
                    # Extract headline
                    headline_elem = item.select_one('h3, .story-title')
                    if not headline_elem:
                        continue
                    
                    headline = headline_elem.text.strip()
                    
                    # Extract link
                    link_elem = item.select_one('a')
                    if not link_elem or not link_elem.get('href'):
                        continue
                        
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = urljoin("https://www.financialexpress.com", link)
                    
                    # Extract date
                    date_elem = item.select_one('.date-stamp, .story-date')
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if date_elem:
                        date = self._extract_date(date_elem.text)
                    
                    # Extract summary if available
                    summary_elem = item.select_one('.desc, .story-desc')
                    summary = ""
                    if summary_elem:
                        summary = summary_elem.text.strip()
                    
                    # Extract content
                    content = summary
                    if not content and link:
                        # Fetch the full article if we don't have a summary
                        article_html = self._make_request(link)
                        if article_html:
                            article_soup = BeautifulSoup(article_html, 'html.parser')
                            content_elems = article_soup.select('.story-details p, .article-content')
                            if content_elems:
                                content = ' '.join([p.text.strip() for p in content_elems])
                    
                    articles.append({
                        'title': headline,
                        'url': link,
                        'date': date,
                        'summary': summary,
                        'content': content,
                        'source': 'Financial Express'
                    })
                    
                except Exception as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
        
        logger.info(f"Scraped {len(articles)} articles from Financial Express")
        return articles
    
    def scrape_all_sources(self, limit_per_source=10):
        """Scrape news from all sources"""
        all_articles = []
        
        # Scrape each source
        et_articles = self.scrape_economic_times(limit=limit_per_source)
        all_articles.extend(et_articles)
        
        mc_articles = self.scrape_moneycontrol(limit=limit_per_source)
        all_articles.extend(mc_articles)
        
        fe_articles = self.scrape_financial_express(limit=limit_per_source)
        all_articles.extend(fe_articles)
        
        # Sort by date (newest first)
        all_articles.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # Update the news cache
        self.news_cache = all_articles
        
        logger.info(f"Scraped a total of {len(all_articles)} articles from all sources")
        return all_articles

class IndianStockNewsScraper:
    """Scraper for Indian stock news and data"""
    
    def __init__(self, use_mock_data=True):
        self.use_mock_data = use_mock_data
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Cache to avoid duplicate requests
        self.news_cache = {}
        self.price_cache = {}
    
    def get_stock_data(self, symbol, days=30):
        """
        Get historical stock price data for the given symbol
        
        Args:
            symbol (str): NSE stock symbol (e.g., 'TCS', 'RELIANCE')
            days (int): Number of days of historical data to retrieve
            
        Returns:
            pandas.DataFrame: DataFrame with date and price data
        """
        if self.use_mock_data:
            return self._get_mock_stock_data(symbol, days)
        
        # If not using mock data, implement real API calls here
        try:
            # For real implementation, would use NSE/BSE API
            # Example with Alpha Vantage (requires API key)
            # API_KEY = "YOUR_API_KEY"
            # url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}.NS&outputsize=compact&apikey={API_KEY}"
            # response = requests.get(url, headers=self.headers)
            # data = response.json()
            
            # Using mock data instead for demonstration
            return self._get_mock_stock_data(symbol, days)
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return self._get_mock_stock_data(symbol, days)
    
    def _get_mock_stock_data(self, symbol, days=30):
        """Generate mock stock data for demo purposes"""
        if symbol in self.price_cache:
            return self.price_cache[symbol]
            
        # Generate realistic price points based on the stock
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        dates.reverse()  # Oldest first
        
        # Base price based on the stock (semi-realistic)
        base_prices = {
            "RELIANCE": 2400,
            "TCS": 3500,
            "HDFCBANK": 1600,
            "INFY": 1400,
            "ICICIBANK": 950,
            "HINDUNILVR": 2800,
            "SBIN": 650,
            "BAJFINANCE": 6800,
            "BHARTIARTL": 850,
            "KOTAKBANK": 1850,
            "WIPRO": 450,
            "AXISBANK": 950,
            "ASIANPAINT": 3200,
            "MARUTI": 9500,
            "TITAN": 2900
        }
        
        base_price = base_prices.get(symbol, 1000)  # Default to 1000 if not in the list
        
        # Generate semi-realistic price movements
        prices = []
        current_price = base_price
        
        for _ in dates:
            # Random daily change between -2% and 2%
            change_pct = random.uniform(-0.02, 0.02)
            current_price = current_price * (1 + change_pct)
            prices.append(round(current_price, 2))
        
        # Create a pandas DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        
        # Cache the result
        self.price_cache[symbol] = df
        return df
    
    def get_news_articles(self, symbol, days=14):
        """
        Get news articles for the given stock symbol
        
        Args:
            symbol (str): NSE stock symbol (e.g., 'TCS', 'RELIANCE')
            days (int): Number of days to look back for news
            
        Returns:
            list: List of news article dictionaries with title, date, summary, url, and sentiment
        """
        if symbol in self.news_cache:
            return self.news_cache[symbol]
            
        if self.use_mock_data:
            articles = self._get_mock_news(symbol, days)
            self.news_cache[symbol] = articles
            return articles
            
        # If not using mock data, implement web scraping here
        try:
            # Implement scraping from moneycontrol or economic times
            # This is a placeholder for actual implementation
            articles = []
            
            # Example scraping from moneycontrol
            company_name = COMMON_INDIAN_STOCKS.get(symbol, symbol)
            search_term = company_name.replace(" Ltd.", "").replace(" Limited", "")
            
            # For real implementation, we would scrape news sites
            # Example (simplified):
            # url = f"https://www.moneycontrol.com/news/business/stocks/searchresult.php?q={search_term}"
            # response = requests.get(url, headers=self.headers)
            # soup = BeautifulSoup(response.text, 'html.parser')
            # news_items = soup.select('.common-article')
            
            # For now, return mock data
            articles = self._get_mock_news(symbol, days)
            self.news_cache[symbol] = articles
            return articles
        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")
            return self._get_mock_news(symbol, days)
    
    def _get_mock_news(self, symbol, days=14):
        """Generate mock news articles for demo purposes"""
        # Company name
        company_name = COMMON_INDIAN_STOCKS.get(symbol, symbol)
        short_name = company_name.replace(" Ltd.", "").replace(" Limited", "")
        
        # Base template news with some real links
        news_templates = {
            "RELIANCE": [
                {"title": "Reliance Industries Reports Strong Q4 Results", "sentiment": "positive", "url": "https://economictimes.indiatimes.com/markets/stocks/earnings/reliance-industries-q4-results-net-profit-falls-1-8-qoq-to-rs-16779-crore/articleshow/99694339.cms"},
                {"title": "RIL Expands Retail Footprint with New Acquisitions", "sentiment": "positive", "url": "https://www.moneycontrol.com/news/business/rils-reliance-retail-acquires-ed-a-mamma-clothing-brand-valuing-it-at-rs-150-crore-10633301.html"},
                {"title": "Reliance Jio Launches New 5G Plans", "sentiment": "positive", "url": "https://indianexpress.com/article/technology/tech-news-technology/reliance-jio-launches-new-prepaid-plans-with-netflix-subscription-8639187/"},
            ],
            "TCS": [
                {"title": "TCS Reports Mixed Q4 Results as US Banking Client Spending Slows", "sentiment": "negative", "url": "https://economictimes.indiatimes.com/tech/information-tech/tcs-q4-results-preview-profit-may-rise-3-5-6-revenue-growth-seen-at-3-5-all-eyes-on-fy25-guidance/articleshow/109055959.cms"},
                {"title": "TCS Shares Fall After Analysts Cut IT Sector Outlook", "sentiment": "negative", "url": "https://www.livemint.com/market/stock-market-news/tcs-share-price-tanks-over-2-post-q4-results-should-you-buy-sell-or-hold-the-it-stock-check-what-brokerages-recommend-11712831213146.html"},
                {"title": "TCS Announces New AI Services Partnership", "sentiment": "positive", "url": "https://www.business-standard.com/companies/news/tcs-unveils-new-ai-powered-platform-for-retail-vertical-to-boost-customer-growth-124060300297_1.html"},
            ],
            "INFY": [
                {"title": "Infosys Wins Major Digital Transformation Deal", "sentiment": "positive", "url": "https://economictimes.indiatimes.com/tech/information-tech/infosys-tata-communications-partner-to-accelerate-enterprise-digital-transformation/articleshow/109288635.cms"},
                {"title": "Infosys Faces Challenges in European Market", "sentiment": "negative", "url": "https://www.moneycontrol.com/news/business/markets/tech-view-nifty-forms-hanging-man-pattern-signals-impending-weakness-12451272.html"},
                {"title": "Infosys Revises Growth Outlook for FY25", "sentiment": "neutral", "url": "https://www.business-standard.com/companies/news/infosys-leads-it-pack-in-fy24-growth-on-q4-estimate-beat-and-upbeat-outlook-124041700951_1.html"},
            ],
        }
        
        # Default news templates for stocks not in our list
        default_news = [
            {"title": f"{short_name} Reports Quarterly Earnings", "sentiment": "neutral", "url": "https://economictimes.indiatimes.com/markets/stocks"},
            {"title": f"{short_name} Announces Expansion Plans", "sentiment": "positive", "url": "https://www.moneycontrol.com/stocksmarketsindia/"},
            {"title": f"{short_name} Faces Regulatory Scrutiny", "sentiment": "negative", "url": "https://www.livemint.com/market/stock-market-news"},
            {"title": f"{short_name} Appoints New CEO", "sentiment": "neutral", "url": "https://www.business-standard.com/markets/news"},
        ]
        
        # Get the templates for this symbol, or use default
        templates = news_templates.get(symbol, default_news)
        articles = []
        
        # Generate dates
        today = datetime.now()
        random_dates = []
        for i in range(min(len(templates) + 2, days)):
            random_dates.append(today - timedelta(days=random.randint(0, days-1)))
        random_dates.sort(reverse=True)
        
        # Create articles from templates
        for i, template in enumerate(templates):
            if i < len(random_dates):
                date = random_dates[i].strftime("%Y-%m-%d")
            else:
                date = (today - timedelta(days=random.randint(0, days-1))).strftime("%Y-%m-%d")
                
            # Generate summary based on title and sentiment
            title = template["title"]
            sentiment = template["sentiment"]
            
            if sentiment == "positive":
                summary = f"{short_name} showed strong performance with positive market reception. {title.replace(short_name, 'The company').lower()}."
            elif sentiment == "negative":
                summary = f"{short_name} faced challenges as {title.lower()}. The market reacted cautiously to this development."
            else:
                summary = f"{short_name} announced new developments. {title.replace(short_name, 'The company').lower()}."
            
            article = {
                "date": date,
                "title": title,
                "summary": summary,
                "url": template["url"],
                "sentiment": sentiment
            }
            articles.append(article)
        
        # Add a few more random articles if needed
        while len(articles) < min(7, days):
            sentiment = random.choice(["positive", "negative", "neutral"])
            if sentiment == "positive":
                title = f"{short_name} Announces Positive Growth Outlook"
                summary = f"{short_name} released a positive growth outlook for the upcoming quarter, indicating strong market position."
            elif sentiment == "negative":
                title = f"{short_name} Shares Down on Market Concerns"
                summary = f"{short_name} shares declined as market concerns about the sector impacted investor sentiment."
            else:
                title = f"{short_name} Maintains Stable Position in Market"
                summary = f"{short_name} continued to maintain its market position with stable performance indicators."
            
            date = (today - timedelta(days=random.randint(0, days-1))).strftime("%Y-%m-%d")
            
            article = {
                "date": date,
                "title": title,
                "summary": summary,
                "url": "https://www.moneycontrol.com/stocksmarketsindia/",
                "sentiment": sentiment
            }
            articles.append(article)
        
        # Sort by date, newest first
        articles.sort(key=lambda x: x["date"], reverse=True)
        return articles

    def get_nifty_data(self, days=30):
        """Get Nifty 50 index data for the specified number of days"""
        if "NIFTY50" in self.price_cache:
            return self.price_cache["NIFTY50"]
            
        # Generate mock Nifty 50 data for demonstration
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        dates.reverse()  # Oldest first
        
        # Starting value for Nifty
        base_price = 22500
        
        # Generate semi-realistic price movements
        prices = []
        current_price = base_price
        
        for _ in dates:
            # Random daily change between -1% and 1%
            change_pct = random.uniform(-0.01, 0.01)
            current_price = current_price * (1 + change_pct)
            prices.append(round(current_price, 2))
        
        # Create a pandas DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        
        # Cache the result
        self.price_cache["NIFTY50"] = df
        return df
    
    def get_nifty_news(self, days=14):
        """Get news articles related to Nifty 50 index"""
        if "NIFTY50" in self.news_cache:
            return self.news_cache["NIFTY50"]
            
        # Mock news articles for Nifty
        news_templates = [
            {"title": "Nifty Hits All-Time High on Strong Global Cues", "sentiment": "positive", "url": "https://economictimes.indiatimes.com/markets/stocks/news/10-factors-that-are-likely-to-guide-market-on-wednesday/articleshow/109387649.cms"},
            {"title": "Nifty Plunges 2% as Global Tariff Concerns Weigh on Markets", "sentiment": "negative", "url": "https://economictimes.indiatimes.com/markets/stocks/news/sensex-nifty-end-over-1-5-lower-as-fii-selling-persists-small-midcaps-underperform/articleshow/109369232.cms"},
            {"title": "Fiscal Deficit Concerns Weigh on Nifty; Defensive Sectors Outperform", "sentiment": "negative", "url": "https://www.livemint.com/market/stock-market-news/sensex-today-live-updates-nifty-may-start-on-flat-note-amid-negative-global-cues-11722747126457.html"},
            {"title": "RBI Policy Decision Boosts Banking Stocks, Nifty Begins Recovery", "sentiment": "positive", "url": "https://www.business-standard.com/markets/news/nifty-rebounds-57-points-from-day-s-low-six-factors-behind-market-recovery-124060700486_1.html"},
            {"title": "IT Stocks Drag Nifty Lower as US Tech Earnings Disappoint", "sentiment": "negative", "url": "https://www.moneycontrol.com/news/business/markets/share-market-live-updates-stock-market-today-june-17-latest-news-bse-nse-sensex-nifty-covid-coronavirus-hdfc-bank-hero-moto-corp-timken-devyani-12475311.html"},
            {"title": "Nifty Consolidates as Investors Await Quarterly Results", "sentiment": "neutral", "url": "https://www.business-standard.com/markets/news/nifty-consolidates-near-23-000-level-it-shares-advance-metal-stocks-decline-124061300363_1.html"},
        ]
        
        today = datetime.now()
        articles = []
        
        # Generate random dates
        random_dates = []
        for i in range(min(len(news_templates), days)):
            random_dates.append(today - timedelta(days=random.randint(0, days-1)))
        random_dates.sort(reverse=True)
        
        # Create articles from templates
        for i, template in enumerate(news_templates):
            if i < len(random_dates):
                date = random_dates[i].strftime("%Y-%m-%d")
            else:
                date = (today - timedelta(days=random.randint(0, days-1))).strftime("%Y-%m-%d")
                
            # Generate summary based on title and sentiment
            title = template["title"]
            sentiment = template["sentiment"]
            
            if sentiment == "positive":
                summary = f"The Nifty 50 index showed strong performance as {title.lower()}. Investors responded positively to these developments."
            elif sentiment == "negative":
                summary = f"The Nifty 50 index faced pressure as {title.lower()}. This led to cautious trading in the market."
            else:
                summary = f"The Nifty 50 index remained stable as {title.lower()}. Market participants are watching for further cues."
            
            article = {
                "date": date,
                "title": title,
                "summary": summary,
                "url": template["url"],
                "sentiment": sentiment
            }
            articles.append(article)
        
        # Sort by date, newest first
        articles.sort(key=lambda x: x["date"], reverse=True)
        
        # Cache the result
        self.news_cache["NIFTY50"] = articles
        return articles

    def get_all_stocks_list(self):
        """Get list of all available Indian stocks"""
        # For demonstration, return the common stocks we have
        return COMMON_INDIAN_STOCKS

# Helper functions

def analyze_market_movement(symbol, data, news):
    """
    Analyze market movement for a stock based on price data and news
    
    Args:
        symbol (str): Stock symbol
        data (pandas.DataFrame): Price data
        news (list): News articles
        
    Returns:
        dict: Analysis result with summary and factors
    """
    # Get company name
    company_name = COMMON_INDIAN_STOCKS.get(symbol, symbol)
    
    # Calculate overall change
    if len(data) >= 2:
        start_price = data.iloc[0]['Price']
        end_price = data.iloc[-1]['Price']
        change_pct = ((end_price - start_price) / start_price) * 100
    else:
        change_pct = 0
    
    # Count positive and negative news
    pos_news = [n for n in news if n['sentiment'] == 'positive']
    neg_news = [n for n in news if n['sentiment'] == 'negative']
    
    # Generate summary
    if change_pct > 0:
        direction = "up"
        sentiment = "positive"
    elif change_pct < 0:
        direction = "down"
        sentiment = "negative"
    else:
        direction = "flat"
        sentiment = "neutral"
    
    # Find key factors
    factors = []
    if len(neg_news) > 0 and sentiment == "negative":
        factors.extend([n['title'] for n in neg_news[:2]])
    elif len(pos_news) > 0 and sentiment == "positive":
        factors.extend([n['title'] for n in pos_news[:2]])
    
    # Create analysis result
    result = {
        "symbol": symbol,
        "company_name": company_name,
        "change_percent": round(change_pct, 2),
        "direction": direction,
        "sentiment": sentiment,
        "summary": f"{company_name} is {direction} {abs(round(change_pct, 2))}% over the analyzed period.",
        "factors": factors,
        "recent_news": news[:3]  # Most recent 3 news articles
    }
    
    return result

# Example usage
if __name__ == "__main__":
    # Demo usage of the scraper
    scraper = IndianStockNewsScraper(use_mock_data=True)
    
    # Get data for TCS
    tcs_data = scraper.get_stock_data("TCS", days=30)
    tcs_news = scraper.get_news_articles("TCS", days=14)
    
    print("TCS Stock Data Sample:")
    print(tcs_data.head())
    
    print("\nTCS News Sample:")
    for article in tcs_news[:3]:
        print(f"- {article['date']}: {article['title']} ({article['sentiment']})")
    
    # Get Nifty data
    nifty_data = scraper.get_nifty_data(days=30)
    nifty_news = scraper.get_nifty_news(days=14)
    
    print("\nNifty 50 Data Sample:")
    print(nifty_data.head())
    
    print("\nNifty 50 News Sample:")
    for article in nifty_news[:3]:
        print(f"- {article['date']}: {article['title']} ({article['sentiment']})")
    
    # Get list of all stocks
    all_stocks = scraper.get_all_stocks_list()
    print(f"\nAvailable stocks: {len(all_stocks)}")
    print(list(all_stocks.keys())[:5])
    
    # Analyze market movement
    tcs_analysis = analyze_market_movement("TCS", tcs_data, tcs_news)
    print(f"\nTCS Analysis: {tcs_analysis['summary']}")
    if tcs_analysis['factors']:
        print("Key factors:")
        for factor in tcs_analysis['factors']:
            print(f"- {factor}") 