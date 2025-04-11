# NewsSense - "Why Is My Nifty Down?"

NewsSense is an AI-powered financial news analyzer that connects real-world news and events to stock market performance. It helps answer the common question investors have: "Why is my stock, mutual fund, or ETF down today?"

## Features

- Web scraping of financial news from Indian sources without using commercial APIs
- Real-time stock market data for Nifty, Sensex, and individual stocks
- Natural Language Processing (NLP) to analyze market sentiment and trends
- Question-answering system for natural language queries about market movements
- CLI interface for interactive market analysis

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/newssense.git
cd newssense
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Download NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Usage

### Interactive Mode

To start the interactive CLI interface:

```
python -m scraper.main
```

This will allow you to ask questions about stocks and market movements.

### Command Line Options

- Get a market summary:
```
python -m scraper.main --summary
```

- Ask a specific question:
```
python -m scraper.main --question "Why is Jyothy Labs up today?"
```

- Force refresh of data:
```
python -m scraper.main --refresh
```

- Run as a background scraping daemon:
```
python -m scraper.main --daemon --interval 1800
```

## Sample Queries

- "Why did Jyothy Labs up today?"
- "What happened to Nifty this week?"
- "Any macro news impacting tech-focused funds?"
- "What does the last quarter say for the Swiggy?"
- "Why is HDFC Bank down today?"
- "What's happening with Reliance stock?"

## Project Structure

- `scraper/news_scraper.py` - Web scraper for financial news websites
- `scraper/stock_data.py` - Scraper for stock market data
- `scraper/nlp_analyzer.py` - NLP pipeline for analyzing news articles
- `scraper/main.py` - Main application integrating all components
- `data/` - Directory for cached data and processed articles

## Limitations

- Web scraping is dependent on the structure of the target websites, which may change over time
- The system works with publicly available information only
- Analysis is based on correlation between news and market movements, not causation
- Market movements are often influenced by factors not covered in news articles

## License

MIT