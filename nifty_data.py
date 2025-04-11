"""
Nifty and Fund Market Data for FundWise NLP
This module provides price data for Nifty, SBI AMC, and other funds
for visualization and analysis purposes.
"""
from datetime import datetime, timedelta
import random

def get_nifty_price_data():
    """
    Get mock price data for Nifty index and related funds.
    
    Returns:
        Dictionary with dates and price data for various funds/indices
    """
    # Generate date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Generate dates list
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Price data function - creates realistic price movements with some correlation
    def generate_price_series(base_price, volatility, trend=0, correlation_factor=0.7, correlation_series=None):
        """Generate a realistic price series with optional correlation to another series"""
        prices = [base_price]
        for i in range(1, len(date_list)):
            # Random daily change with trend
            daily_change_pct = random.gauss(trend, volatility)
            
            # Add some correlation to previous price series if provided
            if correlation_series and i > 0 and len(correlation_series) > i:
                corr_change = (correlation_series[i] - correlation_series[i-1]) / correlation_series[i-1]
                daily_change_pct = daily_change_pct * (1 - correlation_factor) + corr_change * correlation_factor
                
            # Calculate new price
            new_price = prices[-1] * (1 + daily_change_pct)
            prices.append(round(new_price, 2))
        
        return prices
    
    # Generate NIFTY price data - base series
    nifty_prices = generate_price_series(
        base_price=22500,  # Starting price
        volatility=0.008,  # Daily volatility
        trend=0.0005,      # Slight upward trend
        correlation_factor=0
    )
    correlation_series = nifty_prices  # Use Nifty as correlation base for other series
    
    # Generate SBI AMC fund data - correlated with Nifty but different volatility
    sbi_amc_prices = generate_price_series(
        base_price=450.75,
        volatility=0.006,
        trend=0.0003,
        correlation_factor=0.8,
        correlation_series=correlation_series
    )
    
    # Generate HDFC AMC fund data
    hdfc_amc_prices = generate_price_series(
        base_price=3200.25,
        volatility=0.007,
        trend=0.0002,
        correlation_factor=0.75,
        correlation_series=correlation_series
    )
    
    # Generate ICICI Prudential fund data
    icici_pru_prices = generate_price_series(
        base_price=950.50,
        volatility=0.0055,
        trend=0.0004,
        correlation_factor=0.7,
        correlation_series=correlation_series
    )
    
    # Bank Nifty prices - correlated with Nifty but different volatility
    bank_nifty_prices = generate_price_series(
        base_price=48200,
        volatility=0.01,
        trend=0.0003,
        correlation_factor=0.85,
        correlation_series=correlation_series
    )
    
    # Return the data
    return {
        "dates": date_list,
        "NIFTY": nifty_prices,
        "SBI": sbi_amc_prices,
        "HDFC": hdfc_amc_prices,
        "ICICI": icici_pru_prices,
        "BANKNIFTY": bank_nifty_prices
    }

def get_nifty_news_articles():
    """Return a collection of Nifty related news articles"""
    
    # Calculate dates for relative timestamps
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    two_days_ago = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    three_days_ago = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    last_week = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    
    return [
        # Nifty News
        {
            'title': 'Nifty Plunges 2% as Global Tariff Concerns Weigh on Markets',
            'content': 'The Nifty 50 index dropped over 2% today, marking its worst session in three months as global markets reacted to news of potential tariff increases between major economies. Information technology and metal stocks were the worst hit, with the sectoral indices falling 3.1% and 2.8% respectively. Foreign institutional investors were net sellers, offloading shares worth ₹3,200 crore. Analysts suggest the market may remain volatile in the near term as investors assess the potential impact of tariff policies on corporate earnings.',
            'source': 'Economic Times',
            'date': yesterday,
            'url': 'https://economictimes.com/nifty-plunges-tariff-concerns'
        },
        {
            'title': 'SBI Mutual Fund Reports Strong AUM Growth Despite Market Volatility',
            'content': 'SBI Mutual Fund, India\'s largest asset management company, reported a 15% year-on-year growth in assets under management despite recent market volatility. The fund house saw particularly strong inflows into its equity schemes, with systematic investment plans (SIPs) reaching an all-time high. The company\'s Managing Director attributed the growth to increasing retail participation and the fund\'s consistent performance across various market cycles. Industry experts view this as a sign of maturing investor behavior in India, with focus shifting from short-term market movements to long-term wealth creation.',
            'source': 'Mint',
            'date': two_days_ago,
            'url': 'https://livemint.com/sbi-mutual-fund-aum-growth'
        },
        {
            'title': 'RBI Policy Decision Boosts Banking Stocks, Nifty Bank Index Up 1.5%',
            'content': 'The Nifty Bank index rose 1.5% following the Reserve Bank of India\'s monetary policy announcement maintaining status quo on interest rates while adopting a less hawkish tone on inflation. Banking stocks rallied on expectations of improving credit growth and potential interest rate cuts later in the year. SBI led the gains with a 2.8% increase, followed by ICICI Bank and Axis Bank. Analysts suggest that improving asset quality and the possibility of a rate easing cycle beginning in the second half of the year could further boost banking sector performance.',
            'source': 'BusinessLine',
            'date': three_days_ago,
            'url': 'https://www.thehindubusinessline.com/rbi-policy-banking-stocks'
        },
        {
            'title': 'IT Stocks Drag Nifty Lower Amid Global Tech Slowdown Concerns',
            'content': 'Information technology stocks pulled the Nifty lower today amid growing concerns about a slowdown in global tech spending. The Nifty IT index fell 3.2%, with all constituents trading in the red. Industry majors cited delays in decision-making by clients in the US and European markets as businesses reassess their technology investments. The sector, which derives a significant portion of revenue from overseas markets, also faced pressure from a strengthening rupee. Analysts have downgraded their earnings forecasts for the sector, expecting growth moderation in the coming quarters.',
            'source': 'LiveMint',
            'date': yesterday,
            'url': 'https://www.livemint.com/it-stocks-drag-nifty'
        },
        {
            'title': 'Nifty Crosses 23,000 Mark for First Time as FII Buying Surges',
            'content': 'The Nifty 50 index breached the 23,000 level for the first time, powered by strong foreign institutional investor (FII) buying and positive global cues. FIIs pumped in over ₹10,000 crore in the past week, their highest weekly purchase in ten months. The rally was broad-based with banking, auto and consumer goods stocks leading the gains. Market experts attribute the surge to improving economic indicators, expectations of strong corporate earnings growth, and India\'s resilient economic outlook compared to other emerging markets. The index has gained over 12% year-to-date, outperforming most global peers.',
            'source': 'Financial Express',
            'date': last_week,
            'url': 'https://www.financialexpress.com/nifty-crosses-23000'
        },
        {
            'title': 'HDFC AMC Launches New Fund Targeting Nifty Next 50 Companies',
            'content': 'HDFC Asset Management Company has launched a new fund focusing on companies in the Nifty Next 50 index, targeting businesses poised to enter the benchmark Nifty 50 index. The fund aims to capitalize on the growth potential of established companies that are on the cusp of becoming market leaders. The AMC\'s Chief Investment Officer highlighted that historically, the Nifty Next 50 has outperformed the Nifty 50 over longer time frames, offering better risk-adjusted returns for investors with a long-term horizon. The new fund offering (NFO) has garnered significant interest from both retail and high net-worth investors.',
            'source': 'Economic Times',
            'date': three_days_ago,
            'url': 'https://economictimes.com/hdfc-amc-nifty-next-50-fund'
        },
        {
            'title': 'Fiscal Deficit Concerns Weigh on Nifty; Defensive Sectors Outperform',
            'content': 'The Nifty closed lower today as concerns about the government\'s fiscal deficit targets weighed on market sentiment. The selling pressure was particularly acute in infrastructure and capital goods stocks following reports of potential spending cuts in the upcoming budget. Defensive sectors like FMCG and pharmaceuticals outperformed the broader market as investors rotated into less cyclical stocks. Economists have raised concerns about the government\'s ability to meet its fiscal consolidation roadmap while maintaining capital expenditure growth, creating uncertainty that has prompted some foreign investors to adopt a cautious stance on Indian equities.',
            'source': 'Mint',
            'date': two_days_ago,
            'url': 'https://www.livemint.com/fiscal-deficit-nifty'
        }
    ]

# Create a demo function to show the price data
def demo_price_data():
    """Display the price data for demonstration purposes"""
    price_data = get_nifty_price_data()
    
    print("Generated price data for the last 30 days:")
    print(f"Start date: {price_data['dates'][0]}")
    print(f"End date: {price_data['dates'][-1]}")
    print("\nLast price for each index/fund:")
    
    for entity in ['NIFTY', 'SBI', 'HDFC', 'ICICI', 'BANKNIFTY']:
        start_price = price_data[entity][0]
        end_price = price_data[entity][-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        direction = "up" if percent_change > 0 else "down"
        
        print(f"{entity}: {end_price} ({direction} {abs(percent_change):.2f}% over 30 days)")

# Run the demo if the script is executed directly
if __name__ == "__main__":
    demo_price_data() 