import os
from nlp_processor import NLPProcessor
from qa_system import QASystem

def verify_environment():
    """Verify that the environment is set up correctly."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set!")
        print("\nTo set it in Windows PowerShell, run:")
        print('$env:GEMINI_API_KEY="your-api-key"')
        print("\nOr to set it directly in Python (this session only):")
        print('import os')
        print('os.environ["GEMINI_API_KEY"] = "your-api-key"')
        return False
    
    print("Environment verification successful!")
    print(f"GEMINI_API_KEY is set to: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else ''}")
    return True

def test_qa_system():
    """Test the QA system with a sample question."""
    # Try to get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        # Set a temporary API key for testing
        try:
            api_key = input("Enter your Gemini API key for testing: ")
            os.environ['GEMINI_API_KEY'] = api_key
        except Exception as e:
            print(f"Error setting API key: {e}")
            return
    
    try:
        print("Initializing NLP processor...")
        nlp_processor = NLPProcessor(api_key)
        print("Initializing QA system...")
        qa_system = QASystem(nlp_processor)
        
        # Sample articles
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
            }
        ]
        
        # Test question
        question = "Why is HDFC Bank's stock down today?"
        print(f"\nTesting with question: {question}")
        
        print("Processing question... (this may take a moment)")
        result = qa_system.process_question(question, articles)
        
        print("\nAnswer:")
        print(result['answer'])
        print(f"\nConfidence Score: {result['confidence_score']:.2f}")
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("\nCheck the error message above for details.")

if __name__ == "__main__":
    if verify_environment():
        test_qa_system()
    else:
        print("\nEnvironment verification failed. Set the GEMINI_API_KEY environment variable before running the test.")
        print("You can still run the test by entering your API key when prompted.") 