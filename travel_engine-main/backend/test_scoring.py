import sys
import os

# Add parent directory to path to import logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic.engine import LogicEngine

def test_scoring():
    engine = LogicEngine()
    
    # Test Case 1: Eco Priority (100% Eco)
    print("\n--- Test Case 1: High Eco Priority (Eco=100, Budget=0, Time=0) ---")
    # Trip: Low CO2 (Train), Medium Cost, Medium Time
    # Cost: 200, CO2: 10, Duration: 3h
    # Max Budget: 1000, People: 1
    score_1 = engine._calculate_score(
        total_cost=200, total_co2=10, duration=3.0,
        max_budget=1000, num_people=1,
        eco_p=100, budget_p=0, duration_p=0
    )
    print(f"Trip (Train): Cost=200, CO2=10, Time=3h -> Score: {score_1:.2f}")
    
    # Trip: High CO2 (Plane/Car), High Cost, Low Time
    # Cost: 800, CO2: 100, Duration: 1h
    score_2 = engine._calculate_score(
        total_cost=800, total_co2=100, duration=1.0,
        max_budget=1000, num_people=1,
        eco_p=100, budget_p=0, duration_p=0
    )
    print(f"Trip (Plane): Cost=800, CO2=100, Time=1h -> Score: {score_2:.2f}")

    # Test Case 2: Budget Priority (100% Budget)
    print("\n--- Test Case 2: High Budget Priority (Eco=0, Budget=100, Time=0) ---")
    score_3 = engine._calculate_score(
        total_cost=200, total_co2=10, duration=3.0,
        max_budget=1000, num_people=1,
        eco_p=0, budget_p=100, duration_p=0
    )
    print(f"Trip (Train): Cost=200 -> Score: {score_3:.2f}")
    
    score_4 = engine._calculate_score(
        total_cost=800, total_co2=100, duration=1.0,
        max_budget=1000, num_people=1,
        eco_p=0, budget_p=100, duration_p=0
    )
    print(f"Trip (Plane): Cost=800 -> Score: {score_4:.2f}")

    # Test Case 3: Balanced (33% each)
    print("\n--- Test Case 3: Balanced Profile (Eco=33, Budget=33, Time=33) ---")
    score_5 = engine._calculate_score(
        total_cost=200, total_co2=10, duration=3.0,
        max_budget=1000, num_people=1,
        eco_p=33, budget_p=33, duration_p=33
    )
    print(f"Trip (Train): Cost=200, CO2=10, Time=3h -> Score: {score_5:.2f}")

if __name__ == "__main__":
    test_scoring()
