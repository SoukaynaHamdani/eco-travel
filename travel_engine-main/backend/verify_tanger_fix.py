
import sys
import os

# Add path
sys.path.append(os.getcwd())

from logic.engine import LogicEngine

def verify_fix():
    print("Initializing LogicEngine...")
    engine = LogicEngine()
    
    # Check if PROLOG data loaded
    transports, destinations = engine._load_prolog_data()
    print(f"Prolog Transports Loaded: {len(transports)}")
    print(f"Prolog Destinations Loaded: {len(destinations)}")
    
    tanger_dest = next((d for d in destinations if d['city'] == 'tanger'), None)
    if tanger_dest:
        print("PASS: 'tanger' found in Prolog destinations.")
    else:
        print("FAIL: 'tanger' NOT found in Prolog destinations.")

    print("\nTesting Recommendation: Tanger -> Marrakech")
    results = engine.recommend(
        origin="tanger",
        max_budget=20000,
        days=5,
        dest_filter="marrakech",
        num_people=1
    )
    
    print(f"Found {len(results)} results:")
    for r in results:
        print(f" - {r['transport']} | Cost: {r['explanation']}")
        
    if len(results) > 0:
        print("SUCCESS: Fix verified.")
    else:
        print("FAILURE: No results found.")

if __name__ == "__main__":
    verify_fix()
