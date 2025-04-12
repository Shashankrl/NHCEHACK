"""
Test script to verify unlisted stocks integration
"""
import json
import requests

# List of unlisted companies to test
UNLISTED_STOCKS = [
    "SWIGGY", "OLA", "BYJU", "ZERODHA", "CRED", "MEESHO"
]

def test_unlisted_stocks():
    print("Testing integration of unlisted stocks...")
    
    # Base URL for the API
    base_url = "http://localhost:5000"
    
    # Test each unlisted company
    for stock in UNLISTED_STOCKS:
        print(f"\nTesting {stock}...")
        
        # Test chat endpoint
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": f"How is {stock} performing today?"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat API response: Status {response.status_code}")
                print(f"Entity detected: {data.get('entity')}")
                print(f"Price: ₹{data.get('live_data', {}).get('price')}")
                print(f"Change: {data.get('live_data', {}).get('pChange')}%")
                
                # Check if content contains the stock name
                if stock in data.get('content', ''):
                    print(f"✅ Content includes {stock}")
                else:
                    print(f"❌ Content doesn't mention {stock}")
                
                # Check if chart data exists
                if data.get('chart_data'):
                    print("✅ Chart data provided")
                else:
                    print("❌ No chart data")
            else:
                print(f"❌ API returned status code: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"❌ Error testing {stock}: {str(e)}")
    
    print("\nTesting descriptions...")
    try:
        response = requests.get(f"{base_url}/api/entities")
        if response.status_code == 200:
            data = response.json()
            entities = data.get('entities', [])
            
            # Look for unlisted companies in the entities list
            found = []
            for entity in entities:
                if entity.get('symbol') in UNLISTED_STOCKS:
                    found.append(entity.get('symbol'))
                    print(f"Found {entity.get('symbol')}: {entity.get('description')}")
            
            if found:
                print(f"✅ Found {len(found)} unlisted companies in entities list")
            else:
                print("❌ No unlisted companies found in entities list")
        else:
            print(f"❌ Entities API returned status code: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error testing entities: {str(e)}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_unlisted_stocks() 