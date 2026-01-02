from logic.engine import LogicEngine
import os

def test_filtering():
    engine = LogicEngine()
    # Mocking behaviors or using fallback
    
    print("Testing Fallback Logic Filtering...")
    
    # 1. No filter
    results_all = engine.recommend("paris", 5000, 5)
    print(f"No filter count: {len(results_all)}")
    
    # 2. Filter for Marrakech
    results_marrakech = engine.recommend("paris", 5000, 5, dest_filter="marrakech")
    print(f"Filter 'marrakech' count: {len(results_marrakech)}")
    
    for r in results_marrakech:
        if r['destination'].lower() != 'marrakech':
            print(f"FAILED: Found {r['destination']} when filtering for marrakech")
            return

    if len(results_marrakech) > 0 and len(results_marrakech) < len(results_all):
         print("SUCCESS: Filtering reduced result set correctly.")
    else:
         print(f"WARNING: Filtered count {len(results_marrakech)} vs All count {len(results_all)}")

    # 3. Filter for non-existent
    results_none = engine.recommend("paris", 5000, 5, dest_filter="mars")
    print(f"Filter 'mars' count: {len(results_none)}")
    if len(results_none) == 0:
        print("SUCCESS: Non-existent destination returned 0 results.")
    else:
        print("FAILED: Found results for non-existent destination")

if __name__ == "__main__":
    test_filtering()
