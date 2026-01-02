
import requests
import json

def test_result_count():
    url = "http://127.0.0.1:8010/recommend"
    payload = {
        "origin": "casablanca",
        "destination_filter": "marrakech",
        "max_budget": 20000,
        "num_people": 1,
        "duration_days": 7,
        "eco_priority": 50,
        "budget_priority": 50,
        "duration_priority": 50
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Number of results: {len(data)}")
        for i, res in enumerate(data):
            print(f"{i+1}. {res['destination']} via {res['transport']} - Score: {res['score']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_result_count()
