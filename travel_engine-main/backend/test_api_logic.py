import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000/recommend"
    headers = {"Content-Type": "application/json"}
    
    # Payload for 1 person
    payload_1 = {
        "origin": "paris",
        "destination_filter": "marrakech",
        "max_budget": 5000,
        "duration_days": 5,
        "num_people": 1
    }
    
    # Payload for 2 people
    payload_2 = {
        "origin": "paris",
        "destination_filter": "marrakech",
        "max_budget": 5000, # Same total budget, allow more room
        "duration_days": 5,
        "num_people": 2
    }
    
    try:
        print("Sending Request 1 (1 person)...")
        r1 = requests.post(base_url, json=payload_1)
        r1.raise_for_status()
        res1 = r1.json()
        
        print("Sending Request 2 (2 people)...")
        r2 = requests.post(base_url, json=payload_2)
        r2.raise_for_status()
        res2 = r2.json()
        
        explanation1 = res1[0]['explanation'] if res1 else "No Data"
        explanation2 = res2[0]['explanation'] if res2 else "No Data"
        
        print(f"\nResult 1 (1 person): {explanation1}")
        print(f"Result 2 (2 people): {explanation2}")
        
        # Parse costs roughly
        cost1 = float(explanation1.split(':')[1].split('EUR')[0].strip())
        cost2 = float(explanation2.split(':')[1].split('EUR')[0].strip())
        
        if cost2 > cost1:
            print(f"\nSUCCESS: Cost increased from {cost1} to {cost2}")
        else:
            print(f"\nFAILURE: Cost did not increase ({cost1} -> {cost2})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
