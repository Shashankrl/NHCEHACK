"""
Tests for the MockNLPProcessor class
"""
import unittest
import sys
import os
# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fundwise.nlp import MockNLPProcessor

class TestMockNLPProcessor(unittest.TestCase):
    """Test cases for the MockNLPProcessor"""

    def setUp(self):
        """Set up the test case"""
        self.nlp = MockNLPProcessor()
        self.test_article = {
            'title': 'Tesla Reports Strong Q2 Earnings',
            'content': 'Tesla Inc. announced better than expected earnings for Q2 2023. Revenue increased by 47% year-over-year, beating analyst expectations.',
            'source': 'Financial Times',
            'date': '2023-07-20'
        }

    def test_summarize_text(self):
        """Test the summarize_text method"""
        text = "This is the first sentence. This is the second sentence."
        summary = self.nlp.summarize_text(text)
        self.assertEqual(summary, "This is the first sentence.")

    def test_analyze_sentiment_positive(self):
        """Test sentiment analysis with positive text"""
        text = "The company reported strong growth with increased profits."
        sentiment = self.nlp.analyze_sentiment(text)
        self.assertEqual(sentiment['label'], "Positive")
        self.assertGreater(sentiment['score'], 0.5)

    def test_analyze_sentiment_negative(self):
        """Test sentiment analysis with negative text"""
        text = "The market declined due to concerns about economic weakness."
        sentiment = self.nlp.analyze_sentiment(text)
        self.assertEqual(sentiment['label'], "Negative")
        self.assertGreater(sentiment['score'], 0.5)

    def test_extract_symbols(self):
        """Test stock symbol extraction"""
        text = "Apple (AAPL) and Tesla (TSLA) stocks were up today."
        symbols = self.nlp.extract_symbols(text)
        self.assertIn("AAPL", symbols)
        self.assertIn("TSLA", symbols)

    def test_process_article(self):
        """Test the process_article method"""
        result = self.nlp.process_article(self.test_article)
        self.assertIn('summary', result)
        self.assertIn('sentiment', result)
        self.assertIn('related_symbols', result)
        self.assertEqual(result['title'], self.test_article['title'])

    def test_find_articles_by_symbol(self):
        """Test finding articles by symbol"""
        # First add an article to the database
        self.nlp.process_article(self.test_article)
        articles = self.nlp.find_articles_by_symbol("TSLA")
        self.assertGreaterEqual(len(articles), 1)

    def test_answer_question(self):
        """Test the question answering function"""
        question = "Why is TSLA up today?"
        answer = self.nlp.answer_question(question)
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 10)

if __name__ == '__main__':
    unittest.main() 