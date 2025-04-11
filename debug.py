"""
Debug script to test imports
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath("."))
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print(f"Files in fundwise directory: {os.listdir('./fundwise')}")
print(f"Files in fundwise/nlp directory: {os.listdir('./fundwise/nlp')}")

try:
    print("\nTrying to import MockNLPProcessor directly...")
    from fundwise.nlp.mock_nlp import MockNLPProcessor
    print("Import successful!")
except Exception as e:
    print(f"Import error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()

print("\nDebug complete.") 