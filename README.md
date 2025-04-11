# FundWise - Stock Analysis Chatbot

FundWise is a comprehensive stock analysis application that provides real-time stock data, financial metrics, and market insights through an intuitive chatbot interface with both Flask API and React frontend.

## Project Overview

The system consists of two main components:

- **Flask API Backend**: Provides endpoints for the chatbot functionality and stock data
- **React Frontend**: User interface for interacting with the chatbot

## Project Structure

```
fundwise/
├── api/                   # API functionality
│   ├── __init__.py
│   ├── routes.py          # API route definitions
│   ├── stock_api.py       # Stock data API functions
│   └── chatbot_api.py     # Chatbot API functions
│
├── react/                 # React frontend
│   ├── src/               # React source code
│   ├── public/            # Public assets
│   └── package.json       # React dependencies
│
├── scraper/               # Web scraping functionality
│   ├── __init__.py
│   └── news_parser.py     # Financial news scraper
│
├── stock_api/             # Stock data processing
│   ├── __init__.py
│   ├── api.py             # Stock API functions
│   └── stock_details.py   # Stock information
│
├── summarizer/            # NLP & Text summarization
│   ├── __init__.py
│   ├── gemini_summarizer.py # AI text summarization
│   ├── news_processor.py    # News NLP processing
│   └── chatbot_nlp.py       # Chatbot NLP component
│
├── templates/             # HTML templates for Flask
│
├── chatbot_ui/            # Original UI components
│
├── app.py                 # Main Flask application
├── run_flask_api.py       # Flask API server runner
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (create from .env.example)
```

## Features

- Real-time stock quotes and financial metrics
- Company profiles and fundamental data
- Interactive chat interface for stock queries
- Financial news scraping and summarization
- React-based modern UI for the chatbot
- Flask API backend with multiple endpoints
- NLP-powered news analysis and question answering

## NLP Component

The NLP component of FundWise is responsible for:

1. **News Article Processing**
   - Summarizing financial news articles
   - Analyzing sentiment (positive/negative/neutral)
   - Extracting stock symbols mentioned in articles
   - Categorizing news by relevance to specific stocks

2. **Stock Movement Explanation**
   - Analyzing recent news to explain price movements
   - Correlating news sentiment with stock performance
   - Providing concise explanations for "Why is [stock] up/down?"

3. **Natural Language Understanding**
   - Processing user questions about stocks and markets
   - Identifying intent and extracting relevant entities
   - Matching questions with appropriate news and data
   - Generating natural language answers

4. **Chatbot Intelligence**
   - Understanding financial terminology and context
   - Maintaining conversation history for context
   - Providing relevant, accurate financial information
   - Handling different types of financial queries

## Setup and Installation

### Prerequisites

- Python 3.7+ installed
- Node.js and npm installed
- Google Gemini API key
- Required Python packages (see requirements.txt)

### Step 1: Install Dependencies

First, set up the Python virtual environment and install dependencies:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

Then install the React dependencies:

```bash
# Navigate to the React directory
cd react

# Install dependencies
npm install
```

### Step 2: Set up API keys

- Copy `.env.example` to `.env`
- Add your API keys:
  - `GEMINI_API_KEY` for the Google Gemini model
  - Other financial API keys as needed

## Running the Application

Start the Flask API server:

```bash
# From the project root directory
python run_flask_api.py
```

This will start the Flask server on http://localhost:5000.

In a separate terminal, start the React development server:

```bash
# Navigate to the React directory
cd react

# Start the development server
npm run dev
```

This will start the React development server on http://localhost:8080.

Access the chatbot through your web browser at http://localhost:8080

## API Endpoints

### NLP-Related Endpoints

#### Chat Endpoint
`POST /api/chat`

Request Body:
```json
{
  "message": "Why is AAPL stock down today?"
}
```

Response:
```json
{
  "response": "Apple (AAPL) is down 2.3% today following reports of supply chain issues affecting iPhone production...",
  "timestamp": "2023-11-01T12:34:56.789Z",
  "request_processed": true,
  "detected_symbol": "AAPL"
}
```

#### Stock News Endpoint
`GET /api/news/AAPL`

Response:
```json
{
  "symbol": "AAPL",
  "news_count": 3,
  "news": [
    {
      "title": "Apple faces supply chain challenges",
      "source": "Market News",
      "url": "https://example.com/news/apple-supply-chain",
      "date": "2023-11-01",
      "summary": "Apple is facing challenges in its supply chain...",
      "sentiment": "Negative"
    },
    ...
  ],
  "timestamp": "2023-11-01T12:34:56.789Z"
}
```

#### Stock Explanation Endpoint
`GET /api/explain/AAPL`

Response:
```json
{
  "symbol": "AAPL",
  "explanation": "Apple's stock is down 2.3% today primarily due to supply chain issues reported in recent news...",
  "timestamp": "2023-11-01T12:34:56.789Z"
}
```

## Troubleshooting

### API Connection Issues
- Ensure both the Flask API server and React development server are running
- Check that the Vite proxy configuration is correctly set up in react/vite.config.ts
- Verify network requests in your browser's developer tools

### NLP Issues
- Ensure your Gemini API key is valid and set in the environment
- Check for rate limiting issues with the Gemini API
- Verify that the news processing system is working correctly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Alpha Vantage for financial data
- Finnhub for stock information
- Google Gemini for NLP capabilities
- Flask for the web framework
- React for the frontend framework