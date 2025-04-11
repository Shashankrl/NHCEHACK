"""
Flask Web Application for MyFi NewsSense
This module provides a web interface for the enhanced NLP system with interactive
charts, sentiment analysis, and Nifty market data visualization.
"""
import os
import json
import time
from flask import Flask, request, jsonify, render_template, session

# Import data and NLP modules
from fundwise.nlp.enhanced_nlp import EnhancedNLPProcessor
from market_data import get_market_articles
from nifty_data import get_nifty_news_articles, get_nifty_price_data
from nifty_chat import generate_answer

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'my-secret-key-for-newssense')

# Initialize NLP processor and load data (only once at startup)
nlp_processor = EnhancedNLPProcessor()
articles = get_market_articles() + get_nifty_news_articles()
price_data = get_nifty_price_data()

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to ask a question and get a response with potential graph data"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Process the question
        response = generate_answer(nlp_processor, question, articles, price_data)
        
        return jsonify({
            'text': response['text'],
            'has_graph': 'graph_data' in response,
            'entity': response.get('entity', 'Market')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/graph', methods=['GET'])
def get_graph_data():
    """API endpoint to get the graph data for the last question"""
    question = request.args.get('question', '')
    entity = request.args.get('entity', None)
    
    try:
        # Generate response with graph data
        response = generate_answer(nlp_processor, question, articles, price_data)
        
        if 'graph_data' in response and 'graph_json' in response['graph_data']:
            graph_json = response['graph_data']['graph_json']
            return jsonify({
                'graph_data': json.loads(graph_json),
                'entity': response.get('entity', 'Market')
            })
        else:
            return jsonify({'error': 'No graph data available for this query'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entities', methods=['GET'])
def get_entities():
    """API endpoint to get the list of available entities (funds/indices)"""
    entities = ["NIFTY", "SBI", "HDFC", "ICICI", "BANKNIFTY"]
    
    # Add descriptions
    entity_descriptions = {
        "NIFTY": "Nifty 50 - India's benchmark stock market index",
        "SBI": "SBI Mutual Fund - India's largest asset management company",
        "HDFC": "HDFC AMC - One of India's leading fund houses",
        "ICICI": "ICICI Prudential - Major financial services provider",
        "BANKNIFTY": "Bank Nifty - Index tracking banking sector stocks"
    }
    
    result = []
    for entity in entities:
        # Get performance data if available
        performance = "N/A"
        if price_data and entity in price_data:
            start_price = price_data[entity][0]
            end_price = price_data[entity][-1]
            percent_change = ((end_price - start_price) / start_price) * 100
            performance = f"{percent_change:.2f}%"
        
        result.append({
            'symbol': entity,
            'description': entity_descriptions.get(entity, ""),
            'performance': performance
        })
    
    return jsonify({'entities': result})

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """API endpoint to get the list of news articles"""
    entity_filter = request.args.get('entity', None)
    
    filtered_articles = []
    for article in articles:
        # Include basic article data
        article_data = {
            'title': article['title'],
            'source': article['source'],
            'date': article['date'],
            'snippet': article['content'][:150] + "..."
        }
        
        # Add to results if no filter or matches filter
        if not entity_filter:
            filtered_articles.append(article_data)
        elif entity_filter.upper() in article['title'].upper() or entity_filter.upper() in article['content'].upper():
            filtered_articles.append(article_data)
    
    return jsonify({'articles': filtered_articles})

# Create templates directory and basic HTML template
def create_templates():
    """Create the templates directory and basic HTML template if they don't exist"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    index_html_path = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(index_html_path):
        with open(index_html_path, 'w', encoding='utf-8') as f:
            f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyFi NewsSense - Why is my Nifty down?</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #dee2e6;
            border-radius: 0.375rem;
            padding: 1rem;
            background-color: white;
        }
        .user-message {
            background-color: #f1f8ff;
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            margin-bottom: 0.5rem;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
        }
        .assistant-message {
            background-color: #efffef;
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            margin-bottom: 0.5rem;
            max-width: 80%;
        }
        .chart-container {
            height: 400px;
            border: 1px solid #dee2e6;
            border-radius: 0.375rem;
            background-color: white;
        }
        .entity-card {
            cursor: pointer;
            transition: transform 0.2s;
        }
        .entity-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .news-item {
            border-left: 4px solid #28a745;
            padding-left: 1rem;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">
                📊 MyFi NewsSense
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="showHelp">Help</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-8">
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Chat with MyFi NewsSense 💬</h5>
                    </div>
                    <div class="card-body">
                        <div class="chat-container d-flex flex-column" id="chatContainer">
                            <div class="assistant-message">
                                👋 Hello! I'm MyFi NewsSense. Ask me about Nifty, mutual funds, or market trends. Try asking "Why is Nifty down today?" or "How is SBI Mutual Fund performing?"
                            </div>
                        </div>
                        <div class="mt-3">
                            <div class="input-group">
                                <input type="text" class="form-control" id="questionInput" 
                                    placeholder="Ask a question (e.g., Why is my Nifty down?)" 
                                    aria-label="Question" aria-describedby="button-addon2">
                                <button class="btn btn-primary" type="button" id="sendButton">
                                    Send
                                </button>
                            </div>
                            <div class="mt-2">
                                <button class="btn btn-sm btn-outline-secondary me-1" onclick="askSampleQuestion('Why is Nifty down today?')">Why is Nifty down? 📉</button>
                                <button class="btn btn-sm btn-outline-secondary me-1" onclick="askSampleQuestion('How is SBI Mutual Fund performing?')">SBI MF performance? 💰</button>
                                <button class="btn btn-sm btn-outline-secondary" onclick="askSampleQuestion('Compare Nifty with HDFC AMC')">Compare Nifty & HDFC 📊</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Interactive Visualization 📈</h5>
                    </div>
                    <div class="card-body">
                        <div class="chart-container" id="chartContainer">
                            <div class="d-flex justify-content-center align-items-center h-100 text-muted">
                                Ask a question about market trends to see data visualizations
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Indices & Funds 💹</h5>
                    </div>
                    <div class="card-body">
                        <div id="entitiesContainer">
                            <div class="d-flex justify-content-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Latest News 📰</h5>
                    </div>
                    <div class="card-body">
                        <div id="newsContainer">
                            <div class="d-flex justify-content-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal for help -->
        <div class="modal fade" id="helpModal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="helpModalLabel">MyFi NewsSense Help</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <h6>Example Questions:</h6>
                        <ul>
                            <li>📉 Why is Nifty down today?</li>
                            <li>💰 How is SBI Mutual Fund performing?</li>
                            <li>📊 Compare Nifty with HDFC AMC</li>
                            <li>🏦 What's happening with Bank Nifty?</li>
                            <li>📰 Tell me about market sentiment</li>
                            <li>💻 How did IT stocks affect Nifty recently?</li>
                            <li>💸 What's the latest on interest rates?</li>
                        </ul>
                        <h6>Features:</h6>
                        <ul>
                            <li>Click on any entity card to quickly ask about it</li>
                            <li>Interactive graphs - hover for details, zoom in/out</li>
                            <li>Sentiment analysis with emoji indicators</li>
                            <li>Dual-axis visualization comparing price and sentiment</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light py-3 mt-4">
        <div class="container text-center">
            <small>MyFi NewsSense - "Why is my Nifty down?" - NHCEHACK</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // DOM elements
        const questionInput = document.getElementById('questionInput');
        const sendButton = document.getElementById('sendButton');
        const chatContainer = document.getElementById('chatContainer');
        const chartContainer = document.getElementById('chartContainer');
        const entitiesContainer = document.getElementById('entitiesContainer');
        const newsContainer = document.getElementById('newsContainer');
        const showHelpButton = document.getElementById('showHelp');
        
        // Event listeners
        document.addEventListener('DOMContentLoaded', function() {
            loadEntities();
            loadNews();

            questionInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendQuestion();
                }
            });

            sendButton.addEventListener('click', sendQuestion);
            
            showHelpButton.addEventListener('click', function() {
                const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
                helpModal.show();
            });
        });

        // Function to send question to API
        async function sendQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;

            // Add user message to chat
            addMessageToChat(question, 'user');
            questionInput.value = '';

            // Show loading message
            const loadingId = 'loading-' + Date.now();
            addLoadingMessage(loadingId);

            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ question })
                });

                const data = await response.json();
                
                // Remove loading message
                removeMessage(loadingId);

                // Add assistant response
                addMessageToChat(data.text, 'assistant');

                // Update chart if available
                if (data.has_graph) {
                    loadGraph(question, data.entity);
                }

            } catch (error) {
                // Remove loading message
                removeMessage(loadingId);
                addMessageToChat('Sorry, I encountered an error. Please try again.', 'assistant');
                console.error('Error:', error);
            }
        }

        // Function to add message to chat
        function addMessageToChat(message, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = sender + '-message';
            messageDiv.innerHTML = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Function to add loading message
        function addLoadingMessage(id) {
            const loadingDiv = document.createElement('div');
            loadingDiv.id = id;
            loadingDiv.className = 'assistant-message';
            loadingDiv.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"><span class="visually-hidden">Loading...</span></div> Analyzing...';
            chatContainer.appendChild(loadingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Function to remove message
        function removeMessage(id) {
            const messageToRemove = document.getElementById(id);
            if (messageToRemove) {
                messageToRemove.remove();
            }
        }

        // Function to load graph
        async function loadGraph(question, entity) {
            try {
                chartContainer.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
                
                const response = await fetch(`/api/graph?question=${encodeURIComponent(question)}&entity=${encodeURIComponent(entity)}`);
                const data = await response.json();
                
                if (data.error) {
                    chartContainer.innerHTML = `<div class="d-flex justify-content-center align-items-center h-100 text-muted">${data.error}</div>`;
                    return;
                }
                
                chartContainer.innerHTML = '';
                Plotly.newPlot(chartContainer, data.graph_data.data, data.graph_data.layout);
                
            } catch (error) {
                chartContainer.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100 text-muted">Error loading chart</div>';
                console.error('Error loading graph:', error);
            }
        }

        // Function to load entities
        async function loadEntities() {
            try {
                const response = await fetch('/api/entities');
                const data = await response.json();
                
                entitiesContainer.innerHTML = '';
                
                data.entities.forEach(entity => {
                    const performanceClass = entity.performance.includes('-') ? 'text-danger' : 'text-success';
                    const performanceIcon = entity.performance.includes('-') ? '📉' : '📈';
                    
                    const entityCard = document.createElement('div');
                    entityCard.className = 'card entity-card mb-2';
                    entityCard.innerHTML = `
                        <div class="card-body p-2">
                            <h6 class="card-title">${entity.symbol} ${performanceIcon}</h6>
                            <p class="card-text small mb-1">${entity.description}</p>
                            <p class="card-text ${performanceClass} fw-bold mb-0">${entity.performance}</p>
                        </div>
                    `;
                    
                    entityCard.addEventListener('click', () => {
                        askSampleQuestion(`Tell me about ${entity.symbol}`);
                    });
                    
                    entitiesContainer.appendChild(entityCard);
                });
                
            } catch (error) {
                entitiesContainer.innerHTML = '<div class="alert alert-danger">Error loading entities</div>';
                console.error('Error loading entities:', error);
            }
        }

        // Function to load news
        async function loadNews() {
            try {
                const response = await fetch('/api/articles');
                const data = await response.json();
                
                newsContainer.innerHTML = '';
                
                // Show just the first few articles
                const articlesToShow = data.articles.slice(0, 5);
                
                articlesToShow.forEach(article => {
                    const newsItem = document.createElement('div');
                    newsItem.className = 'news-item';
                    
                    // Determine sentiment icon
                    let sentimentIcon = '📊';
                    if (article.title.toLowerCase().includes('down') || 
                        article.title.toLowerCase().includes('fall') || 
                        article.title.toLowerCase().includes('drop')) {
                        sentimentIcon = '📉';
                        newsItem.style.borderLeftColor = '#dc3545';
                    } else if (article.title.toLowerCase().includes('up') || 
                             article.title.toLowerCase().includes('rise') || 
                             article.title.toLowerCase().includes('gain')) {
                        sentimentIcon = '📈';
                        newsItem.style.borderLeftColor = '#28a745';
                    }
                    
                    newsItem.innerHTML = `
                        <h6>${sentimentIcon} ${article.title}</h6>
                        <p class="small text-muted mb-1">${article.source} · ${article.date}</p>
                        <p class="small">${article.snippet}</p>
                    `;
                    
                    newsContainer.appendChild(newsItem);
                });
                
            } catch (error) {
                newsContainer.innerHTML = '<div class="alert alert-danger">Error loading news</div>';
                console.error('Error loading news:', error);
            }
        }

        // Function to ask sample question
        function askSampleQuestion(question) {
            questionInput.value = question;
            sendQuestion();
        }
    </script>
</body>
</html>
            ''')

if __name__ == '__main__':
    # Create templates before running the app
    create_templates()
    
    # Run the app
    app.run(debug=True, port=5000) 