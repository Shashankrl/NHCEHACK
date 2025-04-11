from summarizer.gemini_summarizer import GeminiSummarizer

print("Testing GeminiSummarizer initialization...")

try:
    # Attempt to initialize without API key
    summarizer = GeminiSummarizer()
    print("Success! GeminiSummarizer initialized.")
except ValueError as e:
    print(f"Error: {e}")
    print("Providing an API key is required to use GeminiSummarizer.")
except Exception as e:
    print(f"Unexpected error: {e}")

print("\nTesting with empty API key...")
try:
    # Test with empty API key
    summarizer = GeminiSummarizer(api_key="")
    print("Success! GeminiSummarizer initialized with empty key.")
except ValueError as e:
    print(f"Error: {e}")
    print("An API key must be provided to use GeminiSummarizer.")
except Exception as e:
    print(f"Unexpected error: {e}")
    
print("\nTo use the GeminiSummarizer in production:")
print("1. Get a Gemini API key from Google AI Studio")
print("2. Set it as an environment variable GEMINI_API_KEY")
print("3. Or pass it directly to the GeminiSummarizer constructor") 