from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from nlp_processor import NLPProcessor

class QASystem:
    def __init__(self, nlp_processor: NLPProcessor):
        self.nlp_processor = nlp_processor
    
    def process_question(self, question: str, articles: List[Dict]) -> Dict:
        """
        Process a user question about fund performance and return relevant information.
        
        Args:
            question (str): User's question (e.g., "Why is HDFC fund down today?")
            articles (List[Dict]): List of processed articles from the database
            
        Returns:
            Dict containing:
            - answer: Generated answer
            - relevant_articles: List of articles used to generate the answer
            - confidence_score: How confident the system is in the answer
        """
        try:
            # Extract fund name from question
            fund_name = self._extract_fund_name(question)
            
            # Get today's date and last 7 days for recent articles
            today = datetime.now().strftime('%Y-%m-%d')
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # Check if we're looking for price drop or general information
            is_price_drop = any(word in question.lower() for word in ['down', 'fall', 'drop', 'decline', 'decrease'])
            
            # Set sentiment filter based on question type
            sentiment_filter = "Negative" if is_price_drop else None
            
            # Find relevant articles
            relevant_articles = self.nlp_processor.find_relevant_articles(
                query=fund_name,
                articles=articles,
                sentiment_filter=sentiment_filter,
                date_range=(week_ago, today)  # Only recent articles
            )
            
            if not relevant_articles:
                return {
                    'answer': f"Sorry, I couldn't find any recent news about {fund_name}.",
                    'relevant_articles': [],
                    'confidence_score': 0.0
                }
            
            # Combine relevant articles for context
            context = "\n\n".join([article['original_text'] for article in relevant_articles])
            
            # Generate answer using Gemini
            answer = self.nlp_processor.answer_question(question, context)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(relevant_articles)
            
            return {
                'answer': answer,
                'relevant_articles': relevant_articles,
                'confidence_score': confidence_score
            }
        except Exception as e:
            print(f"Error processing question: {e}")
            return {
                'answer': "I'm sorry, I couldn't process that question at the moment.",
                'relevant_articles': [],
                'confidence_score': 0.0
            }
    
    def _extract_fund_name(self, question: str) -> str:
        """Extract fund name from the question."""
        try:
            # Try to use Gemini for extraction
            prompt = f"""
            Extract the fund or company name from this question. Return only the name.
            
            Question: {question}
            """
            fund_name = self.nlp_processor.get_gemini_response(prompt).strip()
            
            # Simple fallback if Gemini returns too much text
            if len(fund_name.split()) > 3:
                # Simple extraction based on common patterns
                for keyword in ["HDFC", "SBI", "Nifty", "Sensex", "ICICI", "Axis", "Kotak"]:
                    if keyword in question:
                        return keyword
                return "Unknown"
                
            return fund_name
        except Exception as e:
            print(f"Error extracting fund name: {e}")
            # Fallback to simple keyword extraction
            for keyword in ["HDFC", "SBI", "Nifty", "Sensex", "ICICI", "Axis", "Kotak"]:
                if keyword in question:
                    return keyword
            return "Unknown"
    
    def _calculate_confidence(self, articles: List[Dict]) -> float:
        """Calculate confidence score based on article properties."""
        if not articles:
            return 0.0
        
        try:
            # Factors affecting confidence:
            # 1. Number of articles (more articles = higher confidence)
            # 2. Recency (newer articles = higher confidence)
            # 3. Sentiment strength (stronger sentiment = higher confidence)
            
            num_articles_score = min(len(articles) / 5, 1.0)  # Cap at 1.0
            
            # Calculate recency score
            today = datetime.now()
            recency_scores = []
            for article in articles:
                try:
                    article_date = datetime.strptime(article['date'], '%Y-%m-%d')
                    days_old = (today - article_date).days
                    recency_score = max(0, 1 - (days_old / 7))  # Linear decay over 7 days
                    recency_scores.append(recency_score)
                except Exception:
                    recency_scores.append(0.5)  # Default middle value
            
            recency_score = sum(recency_scores) / len(recency_scores) if recency_scores else 0.5
            
            # Calculate sentiment score
            sentiment_scores = []
            for article in articles:
                try:
                    sentiment_scores.append(article['sentiment']['score'])
                except (KeyError, TypeError):
                    sentiment_scores.append(0.5)  # Default middle value
            
            sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5
            
            # Combine scores with weights
            confidence = (
                0.4 * num_articles_score +  # Number of articles
                0.3 * recency_score +       # Recency
                0.3 * sentiment_score       # Sentiment strength
            )
            
            return min(confidence, 1.0)  # Cap at 1.0
        except Exception as e:
            print(f"Error calculating confidence: {e}")
            return 0.5  # Default middle value 