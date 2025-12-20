import requests
import json
import sys

def test_api():
    url = "http://localhost:8000/search"
    payload = {
        "url": "http://suspicious-link.com/login",
        "top_k": 3
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("\n=== API Response ===")
        print(json.dumps(data, indent=2))
        print("====================")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure uvicorn is running!")
        print("Run: uvicorn src.api.main:app --reload")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
