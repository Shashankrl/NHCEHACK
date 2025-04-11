"""
MyFi NewsSense Ultra Simple Demo
A very simple demonstration with clear visuals and linked news articles
"""

import tempfile
import webbrowser
import time
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import re

def main():
    print("\n" + "=" * 70)
    print("                MyFi NewsSense Ultra Simple Demo")
    print("              'Why is my Nifty down?' - NHCEHACK")
    print("=" * 70)
    
    # Add user input to simulate a real chatbot interaction
    print("\n📱 Welcome to MyFi NewsSense! What would you like to know about the markets?")
    print("   (Try asking: 'Why is my Nifty down?' or 'What happened to TCS?')")
    print("   (Type 'exit' to quit)")
    
    while True:
        user_question = input("\n> ")
        
        # Exit condition
        if user_question.lower() == 'exit':
            print("Thank you for using MyFi NewsSense. Goodbye!")
            break
            
        # Check if question is about Nifty or markets
        nifty_pattern = re.compile(r'nifty|market|index', re.IGNORECASE)
        # Check if question is about specific stocks
        tcs_pattern = re.compile(r'tcs', re.IGNORECASE)
        
        if nifty_pattern.search(user_question):
            print("\n⏳ Analyzing market data and news articles to answer your question...")
            time.sleep(1.5)  # Simulate processing time
            
            # Generate the visualization and answer for Nifty
            generate_nifty_analysis()
            break
        elif tcs_pattern.search(user_question):
            print("\n⏳ Analyzing TCS stock data and related news articles...")
            time.sleep(1.5)  # Simulate processing time
            
            # Generate the visualization and answer for TCS
            generate_tcs_analysis()
            break
        else:
            print("\nℹ️ I can help with questions about the Nifty index and specific stocks like TCS.")
            print("   Try asking something like 'Why did the Nifty drop?' or 'What happened to TCS?'")

def generate_nifty_analysis():
    # Generate simple sample data
    print("Gathering relevant market data...")
    time.sleep(0.8)  # Simulate data gathering
    
    # Create 5 key dates for our demo
    dates = ["May 1", "May 5", "May 10", "May 15", "May 20"]
    
    # Simple Nifty prices - clear pattern: up, big drop, small drop, recovery
    nifty_prices = [22500, 22650, 22000, 21900, 22200]
    
    print("Finding related news articles...")
    time.sleep(1.2)  # Simulate search process
    
    # Key news events - just 3 events for clarity
    news_articles = [
        {
            "date": "May 5",
            "title": "Nifty Plunges 2% as Global Tariff Concerns Weigh on Markets",
            "summary": "The Nifty 50 index dropped over 2% today as global markets reacted to news of potential tariff increases between major economies.",
            "sentiment": "negative",
            "url": "https://economictimes.indiatimes.com/markets/stocks/news/10-factors-that-are-likely-to-guide-market-on-wednesday/articleshow/109387649.cms"
        },
        {
            "date": "May 10",
            "title": "Fiscal Deficit Concerns Weigh on Nifty; Defensive Sectors Outperform",
            "summary": "The Nifty closed lower today as concerns about the government's fiscal deficit targets weighed on market sentiment.",
            "sentiment": "negative",
            "url": "https://www.livemint.com/market/stock-market-news/sensex-today-live-updates-nifty-may-start-on-flat-note-amid-negative-global-cues-11722747126457.html"
        },
        {
            "date": "May 15",
            "title": "RBI Policy Decision Boosts Banking Stocks, Nifty Begins Recovery",
            "summary": "The Nifty Bank index rose 1.5% following the Reserve Bank of India's monetary policy announcement maintaining status quo on interest rates.",
            "sentiment": "positive",
            "url": "https://www.business-standard.com/markets/news/nifty-rebounds-57-points-from-day-s-low-six-factors-behind-market-recovery-124060700486_1.html"
        }
    ]
    
    print("Analyzing sentiment in news articles...")
    time.sleep(0.8)  # Simulate analysis
    
    print("Generating visualization with insights...")
    
    # Set a more attractive style for the plot
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Create a very simple graph with improved aesthetics
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Define more attractive colors
    up_color = '#27ae60'    # Nice green
    down_color = '#e74c3c'  # Nice red
    neutral_color = '#3498db'  # Nice blue
    
    # Use a gradient of colors for better visualization
    colors = [up_color, up_color, down_color, down_color, up_color]
    
    # Add background shading for easier reading
    ax.axvspan(1.5, 3.5, alpha=0.1, color='#e74c3c')  # Shade the drop period
    
    # Use bars for the prices with clear colors
    bars = ax.bar(dates, nifty_prices, color=colors, alpha=0.7, 
                 width=0.6, edgecolor='black', linewidth=1)
    
    # Make the current bar stand out
    for i in range(len(bars)):
        if i == 2:  # Highlight the biggest drop
            bars[i].set_alpha(1.0)
            bars[i].set_edgecolor('black')
            bars[i].set_linewidth(2)
    
    # Add value labels on top of bars with better formatting
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 30,
                f'{height:,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold',
                color='black')
    
    # Add a clear title and labels with improved formatting
    ax.set_title("Nifty Price Changes - May 2024", fontsize=18, pad=20, fontweight='bold')
    ax.set_xlabel("Date", fontsize=14, labelpad=10)
    ax.set_ylabel("Nifty Index Value", fontsize=14, labelpad=10)
    
    # Add a horizontal line for the starting value with annotation
    ax.axhline(y=22500, color=neutral_color, linestyle='--', linewidth=2, label='Starting Value')
    ax.text(0, 22400, "Starting Value", fontsize=10, color=neutral_color)
    
    # Improve tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Add eye-catching annotations with custom boxes
    # Function to create annotation box with custom style
    def create_annotation(x, y, text, xytext, color, arrow_color):
        return ax.annotate(
            text, 
            xy=(x, y),
            xytext=xytext,
            arrowprops=dict(
                facecolor=arrow_color, 
                shrink=0.05, 
                width=2, 
                alpha=0.8,
                connectionstyle="arc3,rad=.2"
            ),
            fontsize=12, 
            fontweight='bold',
            bbox=dict(
                boxstyle="round,pad=0.5", 
                fc=color, 
                ec="black", 
                alpha=0.7
            )
        )
    
    # Add clear annotations for key events with improved styling
    create_annotation(
        1, 22650,
        "MAJOR DROP: Global Tariff News", 
        (1, 23100),
        'mistyrose',
        down_color
    )
    
    create_annotation(
        2, 22000,
        "CONTINUED DROP: Fiscal Deficit", 
        (2.5, 21700),
        'mistyrose',
        down_color
    )
    
    create_annotation(
        3, 21900,
        "RECOVERY: RBI Policy Boost", 
        (3.5, 21500),
        'palegreen',
        up_color
    )
    
    # Add emoji indicators
    ax.text(0.95, 22700, "📈", fontsize=24)
    ax.text(1.95, 21800, "📉", fontsize=24)
    ax.text(3.95, 22300, "📈", fontsize=24)
    
    # Add "WHY DID NIFTY DROP?" text in a prominent box
    props = dict(boxstyle='round', facecolor='#f9e79f', alpha=0.5)
    ax.text(0.5, 0.05, 'WHY DID NIFTY DROP?', transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='center',
            bbox=props, fontweight='bold')
    
    plt.tight_layout()
    
    # Save to temp file with higher DPI for better quality
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
        plt.savefig(f.name, dpi=300, bbox_inches='tight')
        img_path = f.name
    
    plt.close()
    
    # Create a simple HTML file with the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        html_path = f.name
    
    # Create simple HTML content with improved styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MyFi NewsSense - Ultra Simple Demo</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f9f9f9; }}
            .container {{ max-width: 1000px; margin: 0 auto; background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #2c3e50; text-align: center; }}
            h1 {{ background: linear-gradient(135deg, #3498db, #2c3e50); color: white; padding: 15px; border-radius: 10px; margin-top: 0; }}
            .chart-container {{ text-align: center; margin: 30px 0; }}
            .news-item {{ border-left: 4px solid #27ae60; padding: 15px; margin: 15px 0; background-color: #f8f9fa; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: transform 0.2s; }}
            .news-item:hover {{ transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .negative {{ border-left-color: #e74c3c; }}
            .answer {{ background: linear-gradient(135deg, #e9f7fe, #d6eaf8); padding: 25px; border-radius: 10px; margin: 30px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            .answer h2 {{ color: #2980b9; text-align: left; }}
            .answer p {{ font-size: 16px; line-height: 1.6; }}
            .answer li {{ margin-bottom: 8px; }}
            .emoji {{ font-size: 24px; margin-right: 10px; }}
            .user-question {{ background-color: #f1f1f1; padding: 15px; border-radius: 20px 20px 20px 0; display: inline-block; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            img {{ border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            a {{ color: #3498db; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MyFi NewsSense - Market Analysis</h1>
            
            <div class="chart-container">
                <img src="file://{img_path}" alt="Nifty Price Chart" width="100%">
                <p><em>Fig 1: Nifty price changes over time with major events highlighted</em></p>
            </div>
            
            <div class="answer">
                <div class="user-question">
                    <p><strong>You asked:</strong> Why is my Nifty down?</p>
                </div>
                <h2>📊 Analysis Results</h2>
                <p><span class="emoji">📉</span> <strong>The Nifty dropped primarily because of two key events:</strong></p>
                <ol>
                    <li><strong>Global Tariff Concerns (May 5):</strong> The index dropped over 2% as markets reacted to news of potential tariff increases.</li>
                    <li><strong>Fiscal Deficit Concerns (May 10):</strong> Continued pressure as investors worried about government spending.</li>
                </ol>
                <p><span class="emoji">📈</span> <strong>Recovery began on May 15</strong> after the RBI's positive policy announcement that boosted banking stocks.</p>
            </div>
            
            <h2>Key News Articles That Impacted Nifty</h2>
    """
    
    # Add news items to HTML with links
    for article in news_articles:
        css_class = "news-item negative" if article["sentiment"] == "negative" else "news-item"
        emoji = "📉" if article["sentiment"] == "negative" else "📈"
        html_content += f"""
            <div class="{css_class}">
                <h3>{emoji} {article["title"]}</h3>
                <p><strong>Date:</strong> {article["date"]}</p>
                <p>{article["summary"]}</p>
                <p><a href="{article["url"]}" target="_blank">Read full article</a></p>
            </div>
        """
    
    html_content += f"""
        </div>
    </body>
    </html>
    """
    
    # Write to the temp file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open in browser
    print(f"Opening visualization with your answer in browser...")
    webbrowser.open('file://' + html_path)
    
    # Display summary in console too
    print("\n" + "-" * 70)
    print("📊 ANALYSIS RESULTS: WHY IS NIFTY DOWN?")
    print("-" * 70)
    print("1️⃣ Global Tariff Concerns (May 5): 2% drop")
    print("2️⃣ Fiscal Deficit Concerns (May 10): Further decline")
    print("3️⃣ Recovery began May 15 with positive RBI policy announcement")
    print("-" * 70)
    
    print("\nDemonstration Complete!")
    print("=" * 70)

# Add a new function for TCS analysis
def generate_tcs_analysis():
    # Generate simple sample data for TCS
    print("Gathering TCS stock data...")
    time.sleep(0.8)  # Simulate data gathering
    
    # Create 5 key dates for our demo
    dates = ["May 1", "May 5", "May 10", "May 15", "May 20"]
    
    # TCS prices - different pattern from Nifty
    tcs_prices = [3500, 3450, 3200, 3180, 3250]
    
    print("Finding related TCS news articles...")
    time.sleep(1.2)  # Simulate search process
    
    # Key news events specific to TCS
    news_articles = [
        {
            "date": "May 5",
            "title": "TCS Reports Mixed Q4 Results as US Banking Client Spending Slows",
            "summary": "Tata Consultancy Services reported lower than expected revenue growth as spending from its US banking and financial services clients remained cautious.",
            "sentiment": "negative",
            "url": "https://economictimes.indiatimes.com/tech/information-tech/tcs-q4-results-preview-profit-may-rise-3-5-6-revenue-growth-seen-at-3-5-all-eyes-on-fy25-guidance/articleshow/109055959.cms"
        },
        {
            "date": "May 10",
            "title": "TCS Shares Fall After Analysts Cut IT Sector Outlook",
            "summary": "TCS shares dropped nearly 4% today after several analysts downgraded the IT sector outlook citing continued weakness in discretionary spending.",
            "sentiment": "negative",
            "url": "https://www.livemint.com/market/stock-market-news/tcs-share-price-tanks-over-2-post-q4-results-should-you-buy-sell-or-hold-the-it-stock-check-what-brokerages-recommend-11712831213146.html"
        },
        {
            "date": "May 15",
            "title": "TCS Announces New AI Services Partnership, Stock Stabilizes",
            "summary": "TCS announced a new strategic partnership focused on AI services implementation, helping the stock stabilize after recent declines.",
            "sentiment": "positive",
            "url": "https://www.business-standard.com/companies/news/tcs-unveils-new-ai-powered-platform-for-retail-vertical-to-boost-customer-growth-124060300297_1.html"
        }
    ]
    
    print("Analyzing sentiment in TCS news articles...")
    time.sleep(0.8)  # Simulate analysis
    
    print("Generating visualization with insights...")
    
    # Set a more attractive style for the plot
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Create a very simple graph with improved aesthetics
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Define more attractive colors
    up_color = '#27ae60'    # Nice green
    down_color = '#e74c3c'  # Nice red
    neutral_color = '#3498db'  # Nice blue
    
    # Use a gradient of colors for better visualization
    colors = [up_color, down_color, down_color, down_color, up_color]
    
    # Add background shading for easier reading
    ax.axvspan(1.5, 3.5, alpha=0.1, color='#e74c3c')  # Shade the drop period
    
    # Use bars for the prices with clear colors
    bars = ax.bar(dates, tcs_prices, color=colors, alpha=0.7, 
                 width=0.6, edgecolor='black', linewidth=1)
    
    # Make the current bar stand out
    for i in range(len(bars)):
        if i == 2:  # Highlight the biggest drop
            bars[i].set_alpha(1.0)
            bars[i].set_edgecolor('black')
            bars[i].set_linewidth(2)
    
    # Add value labels on top of bars with better formatting
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 30,
                f'{height:,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold',
                color='black')
    
    # Add a clear title and labels with improved formatting
    ax.set_title("TCS Share Price Changes - May 2024", fontsize=18, pad=20, fontweight='bold')
    ax.set_xlabel("Date", fontsize=14, labelpad=10)
    ax.set_ylabel("TCS Share Price (₹)", fontsize=14, labelpad=10)
    
    # Add a horizontal line for the starting value with annotation
    ax.axhline(y=3500, color=neutral_color, linestyle='--', linewidth=2, label='Starting Value')
    ax.text(0, 3480, "Starting Value", fontsize=10, color=neutral_color)
    
    # Improve tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Function to create annotation box with custom style
    def create_annotation(x, y, text, xytext, color, arrow_color):
        return ax.annotate(
            text, 
            xy=(x, y),
            xytext=xytext,
            arrowprops=dict(
                facecolor=arrow_color, 
                shrink=0.05, 
                width=2, 
                alpha=0.8,
                connectionstyle="arc3,rad=.2"
            ),
            fontsize=12, 
            fontweight='bold',
            bbox=dict(
                boxstyle="round,pad=0.5", 
                fc=color, 
                ec="black", 
                alpha=0.7
            )
        )
    
    # Add clear annotations for key events with improved styling
    create_annotation(
        1, 3450,
        "DROP: Mixed Q4 Results", 
        (1, 3650),
        'mistyrose',
        down_color
    )
    
    create_annotation(
        2, 3200,
        "CONTINUED DROP: Analyst Downgrades", 
        (2.5, 3100),
        'mistyrose',
        down_color
    )
    
    create_annotation(
        3, 3180,
        "RECOVERY: New AI Partnership", 
        (3.5, 3050),
        'palegreen',
        up_color
    )
    
    # Add emoji indicators
    ax.text(0.95, 3400, "📉", fontsize=24)
    ax.text(1.95, 3150, "📉", fontsize=24)
    ax.text(3.95, 3300, "📈", fontsize=24)
    
    # Add "WHY DID TCS DROP?" text in a prominent box
    props = dict(boxstyle='round', facecolor='#f9e79f', alpha=0.5)
    ax.text(0.5, 0.05, 'WHY DID TCS DROP?', transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='center',
            bbox=props, fontweight='bold')
    
    plt.tight_layout()
    
    # Save to temp file with higher DPI for better quality
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
        plt.savefig(f.name, dpi=300, bbox_inches='tight')
        img_path = f.name
    
    plt.close()
    
    # Create a simple HTML file with the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        html_path = f.name
    
    # Create simple HTML content with improved styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MyFi NewsSense - TCS Analysis</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f9f9f9; }}
            .container {{ max-width: 1000px; margin: 0 auto; background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #2c3e50; text-align: center; }}
            h1 {{ background: linear-gradient(135deg, #3498db, #2c3e50); color: white; padding: 15px; border-radius: 10px; margin-top: 0; }}
            .chart-container {{ text-align: center; margin: 30px 0; }}
            .news-item {{ border-left: 4px solid #27ae60; padding: 15px; margin: 15px 0; background-color: #f8f9fa; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: transform 0.2s; }}
            .news-item:hover {{ transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .negative {{ border-left-color: #e74c3c; }}
            .answer {{ background: linear-gradient(135deg, #e9f7fe, #d6eaf8); padding: 25px; border-radius: 10px; margin: 30px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            .answer h2 {{ color: #2980b9; text-align: left; }}
            .answer p {{ font-size: 16px; line-height: 1.6; }}
            .answer li {{ margin-bottom: 8px; }}
            .emoji {{ font-size: 24px; margin-right: 10px; }}
            .user-question {{ background-color: #f1f1f1; padding: 15px; border-radius: 20px 20px 20px 0; display: inline-block; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            img {{ border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            a {{ color: #3498db; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MyFi NewsSense - TCS Stock Analysis</h1>
            
            <div class="chart-container">
                <img src="file://{img_path}" alt="TCS Price Chart" width="100%">
                <p><em>Fig 1: TCS share price changes over time with major events highlighted</em></p>
            </div>
            
            <div class="answer">
                <div class="user-question">
                    <p><strong>You asked:</strong> Why is TCS down?</p>
                </div>
                <h2>📊 Analysis Results</h2>
                <p><span class="emoji">📉</span> <strong>TCS shares dropped primarily because of two key factors:</strong></p>
                <ol>
                    <li><strong>Q4 Results Below Expectations (May 5):</strong> TCS reported mixed quarterly results with lower than expected revenue growth due to cautious spending from US banking clients.</li>
                    <li><strong>Analyst Downgrades (May 10):</strong> Several analysts downgraded the outlook for the IT sector citing continued weakness in discretionary spending.</li>
                </ol>
                <p><span class="emoji">📈</span> <strong>Recovery began on May 15</strong> after TCS announced a new strategic partnership focused on AI services implementation.</p>
            </div>
            
            <h2>Key News Articles That Impacted TCS</h2>
    """
    
    # Add news items to HTML with links
    for article in news_articles:
        css_class = "news-item negative" if article["sentiment"] == "negative" else "news-item"
        emoji = "📉" if article["sentiment"] == "negative" else "📈"
        html_content += f"""
            <div class="{css_class}">
                <h3>{emoji} {article["title"]}</h3>
                <p><strong>Date:</strong> {article["date"]}</p>
                <p>{article["summary"]}</p>
                <p><a href="{article["url"]}" target="_blank">Read full article</a></p>
            </div>
        """
    
    html_content += f"""
        </div>
    </body>
    </html>
    """
    
    # Write to the temp file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open in browser
    print(f"Opening visualization with your answer in browser...")
    webbrowser.open('file://' + html_path)
    
    # Display summary in console too
    print("\n" + "-" * 70)
    print("📊 ANALYSIS RESULTS: WHY IS TCS DOWN?")
    print("-" * 70)
    print("1️⃣ Q4 Results Below Expectations (May 5): Share price initially dropped")
    print("2️⃣ Analyst Downgrades (May 10): Further decline due to sector outlook")
    print("3️⃣ Recovery began May 15 with announcement of new AI services partnership")
    print("-" * 70)
    
    print("\nDemonstration Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main() 