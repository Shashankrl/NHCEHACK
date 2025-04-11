"""
Stock data scraper for Indian markets
This module fetches stock data for Sensex, Nifty, and individual stocks
from public sources without using commercial APIs.
"""
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import logging
from datetime import datetime, timedelta
import csv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("stock_scraper.log"), logging.StreamHandler()]
)
logger = logging.getLogger("StockScraperIndia")

class StockScraperIndia:
    """Scraper for Indian stock market data"""
    
    def __init__(self):
        """Initialize the scraper with common headers and settings"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.session = requests.Session()
        self.timeout = 30
        self.stock_cache = {}
        self.symbols_cache = []
    
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
    
    def fetch_nifty_data(self):
        """Fetch current Nifty index data"""
        url = "https://www.nseindia.com/api/market-data-pre-open?key=NIFTY"
        try:
            # NSE website has protections, so we need to visit the home page first
            home_page = "https://www.nseindia.com/get-quotes/equity?symbol=NIFTY%2050"
            self._make_request(home_page)
            
            # Now try to get the data
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return {
                    'index': 'NIFTY 50',
                    'price': data.get('data', [])[0].get('lastPrice', 'N/A'),
                    'change': data.get('data', [])[0].get('change', 'N/A'),
                    'percent_change': data.get('data', [])[0].get('pChange', 'N/A'),
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            logger.error(f"Error fetching Nifty data: {str(e)}")
        
        # Fallback to scraping from Money Control if NSE API fails
        try:
            url = "https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
            html = self._make_request(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                price_div = soup.select_one('.bseindex_card .inprice1')
                change_div = soup.select_one('.bseindex_card .inpcnt1')
                
                if price_div and change_div:
                    price = price_div.text.strip()
                    change_text = change_div.text.strip()
                    change_match = re.search(r'([+-]?\d+\.\d+)\s*\(([+-]?\d+\.\d+)%\)', change_text)
                    
                    if change_match:
                        change = change_match.group(1)
                        percent_change = change_match.group(2)
                        
                        return {
                            'index': 'NIFTY 50',
                            'price': price,
                            'change': change,
                            'percent_change': percent_change,
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
            
        except Exception as e:
            logger.error(f"Error in fallback Nifty scraper: {str(e)}")
        
        # Return empty data if all methods fail
        return {
            'index': 'NIFTY 50',
            'price': 'N/A',
            'change': 'N/A',
            'percent_change': 'N/A',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def fetch_sensex_data(self):
        """Fetch current Sensex index data"""
        try:
            url = "https://www.moneycontrol.com/indian-indices/sensex-4.html"
            html = self._make_request(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                price_div = soup.select_one('.bseindex_card .inprice1')
                change_div = soup.select_one('.bseindex_card .inpcnt1')
                
                if price_div and change_div:
                    price = price_div.text.strip()
                    change_text = change_div.text.strip()
                    change_match = re.search(r'([+-]?\d+\.\d+)\s*\(([+-]?\d+\.\d+)%\)', change_text)
                    
                    if change_match:
                        change = change_match.group(1)
                        percent_change = change_match.group(2)
                        
                        return {
                            'index': 'SENSEX',
                            'price': price,
                            'change': change,
                            'percent_change': percent_change,
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
            
        except Exception as e:
            logger.error(f"Error fetching Sensex data: {str(e)}")
        
        # Return empty data if all methods fail
        return {
            'index': 'SENSEX',
            'price': 'N/A',
            'change': 'N/A',
            'percent_change': 'N/A',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def fetch_stock_symbols(self):
        """Fetch list of stock symbols from NSE"""
        if self.symbols_cache:
            return self.symbols_cache
        
        try:
            # First, try to load from local CSV if available
            if os.path.exists('data/nse_symbols.csv'):
                with open('data/nse_symbols.csv', 'r') as f:
                    reader = csv.DictReader(f)
                    symbols = [row for row in reader]
                    if symbols:
                        self.symbols_cache = symbols
                        return symbols
            
            # If not available locally, scrape from Money Control
            url = "https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/nifty-50.html"
            html = self._make_request(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.select_one('table.tbldata14')
                
                if table:
                    symbols = []
                    rows = table.select('tr')[1:]  # Skip header row
                    
                    for row in rows:
                        cells = row.select('td')
                        if len(cells) >= 2:
                            stock_name = cells[0].text.strip()
                            stock_code = cells[1].text.strip()
                            
                            symbols.append({
                                'symbol': stock_code,
                                'name': stock_name,
                                'exchange': 'NSE'
                            })
                    
                    # Save to cache
                    self.symbols_cache = symbols
                    
                    # Save to local file
                    os.makedirs('data', exist_ok=True)
                    with open('data/nse_symbols.csv', 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['symbol', 'name', 'exchange'])
                        writer.writeheader()
                        writer.writerows(symbols)
                    
                    return symbols
        
        except Exception as e:
            logger.error(f"Error fetching stock symbols: {str(e)}")
        
        # Return empty list if all methods fail
        return []
    
    def fetch_stock_data(self, symbol):
        """Fetch data for a specific stock by symbol"""
        # Check cache first
        if symbol in self.stock_cache:
            # Only use cache if it's less than 15 minutes old
            cache_time = datetime.strptime(self.stock_cache[symbol]['date'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time < timedelta(minutes=15):
                return self.stock_cache[symbol]
        
        try:
            # Try Money Control first
            url = f"https://www.moneycontrol.com/india/stockpricequote/search/auto/{symbol}"
            html = self._make_request(url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                # Check if we have search results and need to click through
                search_results = soup.select('.srch_tbl a')
                if search_results:
                    stock_url = search_results[0]['href']
                    html = self._make_request(stock_url)
                    soup = BeautifulSoup(html, 'html.parser')
                
                # Now extract stock data
                price_div = soup.select_one('.pcstkspr span')
                change_div = soup.select_one('.bsedata .stk-sp-chg span')
                company_div = soup.select_one('h1.pcstname')
                
                if price_div and change_div and company_div:
                    price = price_div.text.strip()
                    change_text = change_div.text.strip()
                    company_name = company_div.text.strip()
                    
                    # Extract change amount and percentage
                    change_match = re.search(r'([+-]?\d+\.\d+)\s*\(([+-]?\d+\.\d+)%\)', change_text)
                    change = 'N/A'
                    percent_change = 'N/A'
                    
                    if change_match:
                        change = change_match.group(1)
                        percent_change = change_match.group(2)
                    
                    stock_data = {
                        'symbol': symbol,
                        'name': company_name,
                        'price': price,
                        'change': change,
                        'percent_change': percent_change,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Cache the result
                    self.stock_cache[symbol] = stock_data
                    return stock_data
        
        except Exception as e:
            logger.error(f"Error fetching data for stock {symbol}: {str(e)}")
        
        # Return empty data if all methods fail
        return {
            'symbol': symbol,
            'name': 'Unknown',
            'price': 'N/A',
            'change': 'N/A',
            'percent_change': 'N/A',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def fetch_top_gainers_losers(self):
        """Fetch top gainers and losers from NSE"""
        gainers = []
        losers = []
        
        try:
            # Try to scrape Money Control for gainers
            url = "https://www.moneycontrol.com/stocks/marketstats/nse-gainer/index.php"
            html = self._make_request(url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.select_one('table.tbldata14')
                
                if table:
                    rows = table.select('tr.bggry')[1:11]  # Get top 10 gainers
                    
                    for row in rows:
                        cells = row.select('td')
                        if len(cells) >= 5:
                            company = cells[0].text.strip()
                            price = cells[1].text.strip()
                            change = cells[2].text.strip()
                            percent_change = cells[3].text.strip()
                            
                            # Extract symbol from link
                            symbol_elem = cells[0].select_one('a')
                            symbol = symbol_elem.text.strip() if symbol_elem else 'Unknown'
                            
                            gainers.append({
                                'symbol': symbol,
                                'name': company,
                                'price': price,
                                'change': change,
                                'percent_change': percent_change,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
            
            # Try to scrape Money Control for losers
            url = "https://www.moneycontrol.com/stocks/marketstats/nse-loser/index.php"
            html = self._make_request(url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.select_one('table.tbldata14')
                
                if table:
                    rows = table.select('tr.bggry')[1:11]  # Get top 10 losers
                    
                    for row in rows:
                        cells = row.select('td')
                        if len(cells) >= 5:
                            company = cells[0].text.strip()
                            price = cells[1].text.strip()
                            change = cells[2].text.strip()
                            percent_change = cells[3].text.strip()
                            
                            # Extract symbol from link
                            symbol_elem = cells[0].select_one('a')
                            symbol = symbol_elem.text.strip() if symbol_elem else 'Unknown'
                            
                            losers.append({
                                'symbol': symbol,
                                'name': company,
                                'price': price,
                                'change': change,
                                'percent_change': percent_change,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
        
        except Exception as e:
            logger.error(f"Error fetching top gainers/losers: {str(e)}")
        
        return {
            'gainers': gainers,
            'losers': losers
        }
    
    def fetch_mutual_fund_data(self, fund_name=None):
        """Fetch mutual fund data (basic implementation)"""
        funds = []
        
        try:
            # Try to scrape Value Research for mutual fund data
            url = "https://www.valueresearchonline.com/funds/selector/category/1/equity-large-cap/?end-type=1&plan-type=direct&tab=overview"
            html = self._make_request(url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.select_one('table.grid')
                
                if table:
                    rows = table.select('tbody tr')
                    
                    for row in rows:
                        cells = row.select('td')
                        if len(cells) >= 7:
                            mf_name = cells[0].text.strip()
                            
                            # Skip if specific fund name is provided and doesn't match
                            if fund_name and fund_name.lower() not in mf_name.lower():
                                continue
                                
                            aum = cells[1].text.strip()
                            expense_ratio = cells[2].text.strip()
                            returns_1yr = cells[3].text.strip()
                            returns_3yr = cells[4].text.strip()
                            returns_5yr = cells[5].text.strip()
                            
                            funds.append({
                                'name': mf_name,
                                'aum': aum,
                                'expense_ratio': expense_ratio,
                                'returns_1yr': returns_1yr,
                                'returns_3yr': returns_3yr,
                                'returns_5yr': returns_5yr,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            
                            # If we found the specific fund, we can stop
                            if fund_name and len(funds) > 0:
                                break
        
        except Exception as e:
            logger.error(f"Error fetching mutual fund data: {str(e)}")
        
        return funds

if __name__ == "__main__":
    # Simple test when run directly
    scraper = StockScraperIndia()
    
    # Test Nifty data
    nifty_data = scraper.fetch_nifty_data()
    print("NIFTY 50 Data:")
    print(f"  Price: {nifty_data['price']}")
    print(f"  Change: {nifty_data['change']} ({nifty_data['percent_change']}%)")
    print(f"  Date: {nifty_data['date']}")
    
    # Test stock data
    print("\nTesting stock data for: RELIANCE")
    stock_data = scraper.fetch_stock_data("RELIANCE")
    print(f"  Symbol: {stock_data['symbol']}")
    print(f"  Name: {stock_data['name']}")
    print(f"  Price: {stock_data['price']}")
    print(f"  Change: {stock_data['change']} ({stock_data['percent_change']}%)")
    
    # Test top gainers/losers
    market_data = scraper.fetch_top_gainers_losers()
    print("\nTop Gainers:")
    for i, gainer in enumerate(market_data['gainers'][:3], 1):
        print(f"  {i}. {gainer['name']} ({gainer['symbol']}): {gainer['price']} ({gainer['percent_change']}%)")
    
    print("\nTop Losers:")
    for i, loser in enumerate(market_data['losers'][:3], 1):
        print(f"  {i}. {loser['name']} ({loser['symbol']}): {loser['price']} ({loser['percent_change']}%)") 