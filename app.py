from flask import Flask
from api.routes import api_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Root route
@app.route('/')
def index():
    return {
        "message": "FundWise API is running",
        "api_docs": "/api-docs",
        "api_base": "/api",
        "status": "online"
    }

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    # Run app
    app.run(host='0.0.0.0', port=port, debug=True) 