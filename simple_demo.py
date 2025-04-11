"""
MyFi NewsSense Simple Demo
A simplified demonstration with basic visualizations
"""

import tempfile
import webbrowser
import time
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

def main():
    print("\n" + "=" * 70)
    print("                MyFi NewsSense Simple Demo")
    print("           'Why is my Nifty down?' - NHCEHACK")
    print("=" * 70)
    
    # Generate some simple sample data
    print("\nGenerating sample data...")
    
    # Create dates for the last 15 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Generate mock Nifty prices with a decline in the middle
    nifty_prices = [22500]
    for i in range(1, len(dates)):
        if i < 5:
            # Slight uptrend
            change = random.uniform(0.1, 0.3)
        elif 5 <= i < 8:
            # Significant drop (tariff news)
            change = random.uniform(-1.0, -0.5)
        else:
            # Recovery
            change = random.uniform(0.05, 0.4)
        
        new_price = nifty_prices[-1] * (1 + change/100)
        nifty_prices.append(round(new_price, 2))
    
    # Generate mock sentiment scores
    sentiments = []
    news_days = [2, 5, 7, 10, 13]  # Days with news
    for i in range(len(dates)):
        if i in news_days:
            if i == 5:
                # Bad news day
                sentiments.append(-0.7)
            elif i == 10:
                # Good news day
                sentiments.append(0.6)
            else:
                # Mixed news
                sentiments.append(random.uniform(-0.3, 0.3))
        else:
            sentiments.append(None)
    
    # Mock news articles
    news_articles = [
        {"date": dates[2], "title": "Market anticipates strong quarterly results", "sentiment": "positive"},
        {"date": dates[5], "title": "Nifty Plunges 2% as Global Tariff Concerns Weigh on Markets", "sentiment": "negative"},
        {"date": dates[7], "title": "Fiscal Deficit Concerns Weigh on Nifty; Defensive Sectors Outperform", "sentiment": "negative"},
        {"date": dates[10], "title": "RBI Policy Decision Boosts Banking Stocks, Nifty Up 1.5%", "sentiment": "positive"},
        {"date": dates[13], "title": "Foreign investors return to Indian markets", "sentiment": "positive"}
    ]
    
    # Create a very simple graph
    print("Creating simple visualization...")
    plt.figure(figsize=(10, 6))
    
    # Plot price line
    plt.plot(dates, nifty_prices, 'b-', label='Nifty Price')
    
    # Mark news events with different colors based on sentiment
    for i, day in enumerate(news_days):
        if sentiments[day] > 0:
            plt.plot(dates[day], nifty_prices[day], 'go', markersize=10)  # Green for positive
        else:
            plt.plot(dates[day], nifty_prices[day], 'ro', markersize=10)  # Red for negative
    
    # Add annotations for key news
    plt.annotate("📉 Tariff concerns", 
                xy=(dates[5], nifty_prices[5]),
                xytext=(dates[5], nifty_prices[5]-300),
                arrowprops=dict(facecolor='red', shrink=0.05))
    
    plt.annotate("📈 RBI policy boost", 
                xy=(dates[10], nifty_prices[10]),
                xytext=(dates[10], nifty_prices[10]+300),
                arrowprops=dict(facecolor='green', shrink=0.05))
    
    plt.title("📊 Nifty Price with News Sentiment")
    plt.xlabel("Date")
    plt.ylabel("Nifty Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save to temp file and display
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
        plt.savefig(f.name)
        img_path = f.name
    
    plt.close()
    
    # Create a simple HTML file with the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        html_path = f.name
    
    # Create simple HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MyFi NewsSense - Simple Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            .news-item {{ border-left: 4px solid #28a745; padding-left: 10px; margin: 10px 0; text-align: left; }}
            .negative {{ border-left-color: #dc3545; }}
            .answer {{ background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 20px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 MyFi NewsSense - "Why is my Nifty down?"</h1>
            
            <div style="margin: 20px 0;">
                <img src="file://{img_path}" alt="Nifty Price Chart with News Sentiment" width="100%">
            </div>
            
            <h2>📰 Key News Events</h2>
            <div class="news-container">
    """
    
    # Add news items to HTML
    for article in news_articles:
        css_class = "news-item negative" if article["sentiment"] == "negative" else "news-item"
        emoji = "📉" if article["sentiment"] == "negative" else "📈"
        html_content += f"""
                <div class="{css_class}">
                    <h3>{emoji} {article["title"]}</h3>
                    <p>Date: {article["date"]}</p>
                </div>
        """
    
    # Add answer to "Why is my Nifty down?"
    html_content += f"""
            </div>
            
            <h2>❓ Why is my Nifty down?</h2>
            <div class="answer">
                <p>📉 💹 📰 Nifty is down primarily due to global tariff concerns. The index dropped over 2% on {dates[5]}, marking its worst session in three months as global markets reacted to news of potential tariff increases between major economies.</p>
                <p>Foreign institutional investors were net sellers, offloading shares worth ₹3,200 crore. Additionally, fiscal deficit concerns have added pressure to the market.</p>
                <p>However, there has been some recovery following the RBI policy decision that boosted banking stocks.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write to the temp file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open in browser
    print(f"Opening simple visualization in your browser...")
    webbrowser.open('file://' + html_path)
    
    # Display summary
    print("\n" + "-" * 70)
    print("KEY FEATURES DEMONSTRATED:")
    print("1. 📊 Simple visualization with price chart")
    print("2. 📌 Contextual annotations for key events")
    print("3. 📉 Visual indicators for negative news")
    print("4. 📈 Visual indicators for positive news")
    print("5. 🔍 Clear answer to 'Why is my Nifty down?'")
    print("-" * 70)
    
    print("\nDemonstration Complete!")
    print("=" * 70)
    
    time.sleep(3)  # Give time to read the output

if __name__ == "__main__":
    main() 