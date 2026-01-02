
import sys
import os

# Add path
sys.path.append(os.getcwd())

from logic.engine import LogicEngine

def test_destinations():
    engine = LogicEngine()
    transports, destinations = engine._load_prolog_data()
    
    print(f"Loaded {len(destinations)} destinations from Prolog.")
    for d in destinations:
        print(f" - {d['city']} ({d['country']})")
        
    print(f"\nLoaded {len(transports)} transports from Prolog.")
    
    # Check if 'london' is absent
    london = next((d for d in destinations if d['city'] == 'london'), None)
    if london:
        print("FAIL: London found in destinations!")
    else:
        print("PASS: London successfully removed.")

    # Check if 'tanger' is present
    tanger = next((d for d in destinations if d['city'] == 'tanger'), None)
    if tanger:
        print("PASS: Tanger found in destinations.")
    else:
        print("FAIL: Tanger NOT found.")

if __name__ == "__main__":
    test_destinations()
