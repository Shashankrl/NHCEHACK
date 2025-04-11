"""
FundWise NLP components
Provides text summarization, sentiment analysis, and question answering
for financial news and stock information.
"""

# Import main components for easier access
from fundwise.nlp.mock_nlp import MockNLPProcessor
from fundwise.nlp.news_processor import NewsProcessor
from fundwise.nlp.chatbot_nlp import ChatbotNLP

try:
    from fundwise.nlp.gemini_summarizer import GeminiSummarizer
except ImportError:
    # Gemini might not be available if dependencies are missing
    pass

__all__ = ["MockNLPProcessor", "GeminiSummarizer", "NewsProcessor", "ChatbotNLP"] 