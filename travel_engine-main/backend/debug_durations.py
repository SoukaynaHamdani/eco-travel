
import sys
import os

# Add path
sys.path.append(os.getcwd())

from logic.engine import LogicEngine

def debug_durations():
    print("Initializing LogicEngine...")
    engine = LogicEngine()
    
    routes = [
        ("casablanca", "rabat"), # Short trip (1h)
        ("tanger", "marrakech"), # Long trip
        ("casablanca", "marrakech")
    ]
    
    for origin, dest in routes:
        print(f"\nTesting: {origin} -> {dest}")
        results = engine.recommend(
            origin=origin,
            max_budget=20000,
            days=5,
            dest_filter=dest,
            num_people=1
        )
        
        for r in results:
            print(f" - {r['transport']}")
            print(f"   Explanation: '{r['explanation']}'")
            parts = r['explanation'].split(',')
            if len(parts) > 2:
                # Simulate JS regex
                import re
                dur_part = parts[2]
                match = re.search(r"([\d.]+)h", dur_part)
                if match:
                    print(f"   Parsed Duration: {match.group(1)}h")
                else:
                    print(f"   FAILED TO PARSE DURATION from: '{dur_part}'")
            else:
                print("   FAILED: Explanation has fewer than 3 parts")

if __name__ == "__main__":
    debug_durations()
