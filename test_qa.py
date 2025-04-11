from nlp_processor import NLPProcessor
from qa_system import QASystem
import os

def main():
    # Initialize NLP processor with Gemini API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    nlp_processor = NLPProcessor(api_key)
    qa_system = QASystem(nlp_processor)
    
    # Sample articles (in a real system, these would come from your database)
    articles = [
        {
            'date': '2024-04-10',
            'original_text': """
            HDFC Bank's shares fell 3% today after the RBI imposed restrictions on its digital banking operations.
            The central bank cited concerns over technical glitches and customer complaints.
            Analysts at Morgan Stanley have revised their target price for HDFC Bank from ₹1,800 to ₹1,650.
            This comes amid growing regulatory scrutiny of digital banking services in India.
            """,
            'summary': "RBI imposes restrictions on HDFC Bank's digital operations, causing 3% stock drop.",
            'sentiment': {
                'label': 'Negative',
                'score': 0.85,
                'factors': ['regulatory restrictions', 'technical issues', 'price target reduction']
            }
        },
        {
            'date': '2024-04-09',
            'original_text': """
            HDFC Bank reported strong Q4 earnings with a 25% increase in net profit.
            The bank's digital initiatives have shown promising growth, with mobile banking users up 40%.
            However, concerns remain about the bank's asset quality in the retail segment.
            """,
            'summary': "HDFC Bank reports strong Q4 earnings but faces retail segment concerns.",
            'sentiment': {
                'label': 'Mixed',
                'score': 0.6,
                'factors': ['strong earnings', 'digital growth', 'retail concerns']
            }
        }
    ]
    
    # Test questions
    questions = [
        "Why is HDFC Bank's stock down today?",
        "What's happening with HDFC Bank?",
        "Why did HDFC Bank's price drop?"
    ]
    
    # Process each question
    for question in questions:
        print(f"\nQuestion: {question}")
        result = qa_system.process_question(question, articles)
        
        print(f"\nAnswer (Confidence: {result['confidence_score']:.2f}):")
        print(result['answer'])
        
        if result['relevant_articles']:
            print("\nSource Articles:")
            for article in result['relevant_articles']:
                print(f"\nDate: {article['date']}")
                print(f"Summary: {article['summary']}")
                print(f"Sentiment: {article['sentiment']['label']} (Score: {article['sentiment']['score']})")
                print(f"Key Factors: {', '.join(article['sentiment']['factors'])}")

if __name__ == "__main__":
    main() 