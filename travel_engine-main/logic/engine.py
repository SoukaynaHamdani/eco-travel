from typing import List, Dict, Any, Optional
import os 
import re 
try:
    from pyswip import Prolog
except Exception:
    Prolog = None

class LogicEngine:
    def __init__(self):
        self.prolog_available = False
        self.prolog = None
        self._check_prolog()
        
    def _check_prolog(self):
        # Even if pyswip is installed, we need swipl binary
        if Prolog:
            try:
                # Basic check if SWI-Prolog is in PATH to avoid hanging
                import subprocess
                # Check for swipl executable existence
                if subprocess.call("where swipl", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                   print("SWI-Prolog not found in PATH. Using fallback logic.")
                   self.prolog_available = False
                   return

                self.prolog = Prolog()
                # Try simple query
                list(self.prolog.query("true."))
                self.prolog_available = True
            except Exception as e:
                print(f"Prolog initialization failed: {e}")
                self.prolog_available = False
        
    def load_rules(self, rules_path: str):
        if self.prolog_available:
            try:
                rules_path = rules_path.replace("\\", "/")
                self.prolog.consult(rules_path)
            except Exception as e:
                print(f"Failed to consult prolog file: {e}")
                self.prolog_available = False
    
    def recommend(self, origin: str, max_budget: float, days: int, dest_filter: Optional[str] = None, num_people: int = 1, eco_priority: int = 50, budget_priority: int = 30, duration_priority: int = 20) -> List[Dict[str, Any]]:
        if self.prolog_available:
            return self._recommend_prolog(origin, max_budget, days, dest_filter, num_people, eco_priority, budget_priority, duration_priority)
        else:
            return self._recommend_python(origin, max_budget, days, dest_filter, num_people, eco_priority, budget_priority, duration_priority)
            
    def _calculate_score(self, total_cost, total_co2, duration, max_budget, num_people, eco_p, budget_p, duration_p):
        """
        Calculates the Global Score (0-100) based on weighted user priorities.
        Formula:
        - Score_Budget = max(0, 100 * (1 - Total_Cost / Max_Budget))
        - Score_CO2 = max(0, 100 * (1 - Total_CO2 / (Benchmark_CO2 * Num_People)))
        - Score_Time = max(0, 100 * (1 - Duration / Benchmark_Time))
        
        Final Score = Weighted Sum of Component Scores.
        """
        # 1. Benchmarks
        BENCHMARK_CO2_PER_PERSON = 300.0 # kg
        BENCHMARK_DURATION = 12.0 # hours

        # 2. Component Scores (0-100, higher is better)
        # Budget
        if max_budget > 0:
            budget_score = max(0.0, 100.0 * (1.0 - (total_cost / max_budget)))
        else:
            budget_score = 0.0

        # CO2
        benchmark_total_co2 = BENCHMARK_CO2_PER_PERSON * num_people
        if benchmark_total_co2 > 0:
            co2_score = max(0.0, 100.0 * (1.0 - (total_co2 / benchmark_total_co2)))
        else:
            co2_score = 0.0

        # Duration
        duration_score = max(0.0, 100.0 * (1.0 - (duration / BENCHMARK_DURATION)))

        # 3. Normalized Weights
        total_priority = eco_p + budget_p + duration_p
        if total_priority == 0:
            w_eco, w_budget, w_duration = 1/3, 1/3, 1/3
        else:
            w_eco = eco_p / total_priority
            w_budget = budget_p / total_priority
            w_duration = duration_p / total_priority

        # 4. Final Weighted Score
        final_score = (
            (co2_score * w_eco) +
            (budget_score * w_budget) +
            (duration_score * w_duration)
        )
        
        return min(100.0, final_score)

    def _recommend_prolog(self, origin: str, max_budget: float, days: int, dest_filter: Optional[str] = None, num_people: int = 1, eco_priority: int = 50, budget_priority: int = 30, duration_priority: int = 20) -> List[Dict[str, Any]]:
        # Prolog logic calculates per-person cost. So we check if (PerPersonCost * NumPeople) <= MaxBudget
        # Equivalent to PerPersonCost <= (MaxBudget / NumPeople)
        per_person_budget = max_budget / num_people
        
        dest_arg = dest_filter.lower() if dest_filter else "Dest"
        query = f"recommend({origin.lower()}, {per_person_budget}, {days}, {dest_arg}, Transport, Score, Explanation, Cost, CO2, Duration)"
        results = []
        try:
            for res in self.prolog.query(query):
                # Prolog returns per-person Cost and CO2 totals for the trip
                # We need Group Totals for scoring if our logic expects it, OR consistent units.
                # _calculate_score expects Group Total Cost and Group Total CO2.
                
                # Res['Cost'] is per-person total (Transport + Daily Living)
                # Res['CO2'] is per-person total
                
                cost_per_person = float(res['Cost'])
                co2_per_person = float(res['CO2'])
                duration = float(res['Duration'])
                
                total_cost = cost_per_person * num_people
                total_co2 = co2_per_person * num_people
                
                # Recalculate Score using Python Logic to ensure consistency with User Priorities
                final_score = self._calculate_score(
                    total_cost, total_co2, duration, 
                    max_budget, num_people, 
                    eco_priority, budget_priority, duration_priority
                )

                results.append({
                    "destination": str(res['Dest']),
                    "transport": str(res['Transport']),
                    "score": float(final_score), # Use recalculated score
                    "explanation": str(res['Explanation']) + f" (Group of {num_people})",
                    "cost": total_cost,
                    "co2": total_co2,
                    "duration": duration
                })
                
            # Sort by Score Descending
            results.sort(key=lambda x: x['score'], reverse=True)
            
        except Exception as e:
            print(f"Prolog query error: {e}")
            # Fallback if query fails
            return self._recommend_python(origin, max_budget, days, dest_filter, num_people, eco_priority, budget_priority, duration_priority)
        return results

    def _load_prolog_data(self):
        """
        Parses transport AND destination facts from logic/travel_rules.pl textually.
        Expected format: 
        - transport(Origin, Dest, Type, Cost, CO2, Duration).
        - destination(City, Country, Cost, CO2).
        """
        prolog_transports = []
        prolog_destinations = []
        
        try:
            # Construct absolute path to prolog file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            pl_path = os.path.join(base_dir, "travel_rules.pl")
            
            if os.path.exists(pl_path):
                with open(pl_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Regex for TRANSPORTS: transport(origin, dest, type, cost, co2, duration).
                t_pattern = re.compile(r"transport\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*,\s*([\d\.]+)\s*,\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\)")
                t_matches = t_pattern.findall(content)
                for m in t_matches:
                    origin, dest, t_type, cost, co2, duration = m
                    prolog_transports.append({
                        "origin": origin.lower(),
                        "dest": dest.lower(),
                        "type": t_type.lower(),
                        "cost": float(cost),
                        "co2": float(co2),
                        "duration": float(duration)
                    })
                    
                # Regex for DESTINATIONS: destination(City, Country, Cost, CO2).
                d_pattern = re.compile(r"destination\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*,\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\)")
                d_matches = d_pattern.findall(content)
                for m in d_matches:
                    city, country, cost, co2 = m
                    prolog_destinations.append({
                        "city": city.lower(),
                        "country": country.lower(),
                        "cost_per_day": float(cost),
                        "co2_per_day": float(co2)
                    })
            else:
                print(f"WARNING: Prolog file not found at {pl_path}")
                
        except Exception as e:
            print(f"ERROR: Failed to load Prolog data: {e}")
            
        return prolog_transports, prolog_destinations

    def _recommend_python(self, origin: str, max_budget: float, days: int, dest_filter: Optional[str] = None, num_people: int = 1, eco_priority: int = 50, budget_priority: int = 30, duration_priority: int = 20) -> List[Dict[str, Any]]:
        """Fallback Python logic simulating the Prolog rules"""
        # print(f"DEBUG: _recommend_python call: origin={origin}, filter={dest_filter}...")
        
        # Comprehensive Moroccan travel database with realistic values
        # Prices in MAD (Moroccan Dirham)
        destinations = [
            {"city": "marrakech", "country": "morocco", "cost_per_day": 550, "co2_per_day": 8},
            {"city": "fes", "country": "morocco", "cost_per_day": 500, "co2_per_day": 7},
            {"city": "casablanca", "country": "morocco", "cost_per_day": 650, "co2_per_day": 10},
            {"city": "tangier", "country": "morocco", "cost_per_day": 600, "co2_per_day": 8},
            {"city": "chefchaouen", "country": "morocco", "cost_per_day": 400, "co2_per_day": 5},
            {"city": "essaouira", "country": "morocco", "cost_per_day": 500, "co2_per_day": 6},
            {"city": "rabat", "country": "morocco", "cost_per_day": 600, "co2_per_day": 9},
            {"city": "ouarzazate", "country": "morocco", "cost_per_day": 450, "co2_per_day": 6},
            {"city": "agadir", "country": "morocco", "cost_per_day": 550, "co2_per_day": 7},
            {"city": "meknes", "country": "morocco", "cost_per_day": 450, "co2_per_day": 6},
        ]
        
        # ... (Car constants) ...
        CAR_RENTAL_DAY = 300 
        FUEL_PRICE = 13 
        CONSUMPTION = 0.07 
        TOLL_RATE = 0.35 
        CAR_KM_COST = (FUEL_PRICE * CONSUMPTION) + TOLL_RATE

        def estimate_car_cost(km, days):
             return (CAR_RENTAL_DAY * days) + (km * CAR_KM_COST)

        # 1. Load Hardcoded Python Transports (Advanced)
        python_transports = [
            # From Casablanca
            # Marrakech (~240km)
            {"origin": "casablanca", "dest": "marrakech", "type": "train_2nd", "cost": 130, "co2": 8, "duration": 2.6},
            {"origin": "casablanca", "dest": "marrakech", "type": "train_1st", "cost": 195, "co2": 9, "duration": 2.6}, # ~1.5x
            {"origin": "casablanca", "dest": "marrakech", "type": "bus_ctm", "cost": 100, "co2": 15, "duration": 3.5},
            {"origin": "casablanca", "dest": "marrakech", "type": "car_rental", "distance": 240, "co2": 40, "duration": 2.5}, # Shared
            
            # Fes (~300km)
            {"origin": "casablanca", "dest": "fes", "type": "train_2nd", "cost": 160, "co2": 10, "duration": 4.0},
            {"origin": "casablanca", "dest": "fes", "type": "train_1st", "cost": 240, "co2": 11, "duration": 4.0},
            {"origin": "casablanca", "dest": "fes", "type": "bus_ctm", "cost": 120, "co2": 18, "duration": 5.0},
            {"origin": "casablanca", "dest": "fes", "type": "car_rental", "distance": 300, "co2": 50, "duration": 3.5},

            # Tanger (~340km)
            {"origin": "casablanca", "dest": "tanger", "type": "train_highspeed", "cost": 290, "co2": 6, "duration": 2.2}, # Al Boraq
            {"origin": "casablanca", "dest": "tanger", "type": "bus_ctm", "cost": 160, "co2": 25, "duration": 5.5},
            {"origin": "casablanca", "dest": "tanger", "type": "car_rental", "distance": 340, "co2": 55, "duration": 4.0},

            # Rabat (~90km)
            {"origin": "casablanca", "dest": "rabat", "type": "train_shuttle", "cost": 50, "co2": 3, "duration": 1.0},
            {"origin": "casablanca", "dest": "rabat", "type": "bus_local", "cost": 35, "co2": 5, "duration": 1.5},
            {"origin": "casablanca", "dest": "rabat", "type": "car_rental", "distance": 90, "co2": 15, "duration": 1.0},

            # Essaouira (~380km from Casa)
            {"origin": "casablanca", "dest": "essaouira", "type": "bus_ctm", "cost": 140, "co2": 20, "duration": 6.5},
            {"origin": "casablanca", "dest": "essaouira", "type": "car_rental", "distance": 380, "co2": 60, "duration": 4.5},

            # From Marrakech
            # Fes (~530km)
            {"origin": "marrakech", "dest": "fes", "type": "train_via_casa", "cost": 320, "co2": 18, "duration": 6.5},
            {"origin": "marrakech", "dest": "fes", "type": "bus_ctm", "cost": 190, "co2": 28, "duration": 8.5},
            {"origin": "marrakech", "dest": "fes", "type": "car_rental", "distance": 530, "co2": 85, "duration": 5.5}, # Route nationale

            # Essaouira (~190km)
            {"origin": "marrakech", "dest": "essaouira", "type": "bus_supratours", "cost": 100, "co2": 8, "duration": 3.0},
            {"origin": "marrakech", "dest": "essaouira", "type": "car_rental", "distance": 190, "co2": 30, "duration": 2.5},
            {"origin": "marrakech", "dest": "essaouira", "type": "grand_taxi", "cost": 150, "co2": 12, "duration": 2.5}, # Per seat

            # Ouarzazate (~200km - Mountain)
            {"origin": "marrakech", "dest": "ouarzazate", "type": "bus_ctm", "cost": 100, "co2": 10, "duration": 4.5},
            {"origin": "marrakech", "dest": "ouarzazate", "type": "car_rental", "distance": 200, "co2": 35, "duration": 4.0},

            # From Fes
            # Chefchaouen (~200km)
            {"origin": "fes", "dest": "chefchaouen", "type": "bus_ctm", "cost": 100, "co2": 12, "duration": 4.0},
            {"origin": "fes", "dest": "chefchaouen", "type": "car_rental", "distance": 200, "co2": 35, "duration": 3.5},
            {"origin": "fes", "dest": "chefchaouen", "type": "grand_taxi", "cost": 150, "co2": 15, "duration": 3.5},

            # Tanger (~300km)
            {"origin": "fes", "dest": "tanger", "type": "bus_ctm", "cost": 135, "co2": 20, "duration": 5.0},
            {"origin": "fes", "dest": "tanger", "type": "train_via_kenitra", "cost": 180, "co2": 15, "duration": 3.5},
            {"origin": "fes", "dest": "tanger", "type": "car_rental", "distance": 310, "co2": 50, "duration": 4.5},
            
            # From Tanger
            # Chefchaouen (~110km)
            {"origin": "tanger", "dest": "chefchaouen", "type": "bus_ctm", "cost": 70, "co2": 8, "duration": 2.5},
            {"origin": "tanger", "dest": "chefchaouen", "type": "car_rental", "distance": 115, "co2": 20, "duration": 2.0},
            {"origin": "tanger", "dest": "chefchaouen", "type": "grand_taxi", "cost": 100, "co2": 10, "duration": 2.0},
            
            # Ouarzazate (Long - 800km)
            {"origin": "tanger", "dest": "ouarzazate", "type": "bus_multileg", "cost": 350, "co2": 60, "duration": 14.0},
            {"origin": "tanger", "dest": "ouarzazate", "type": "car_rental", "distance": 800, "co2": 130, "duration": 10.0},
        ]
        
        # 2. Dynamic Prolog Bridge: Append data from travel_rules.pl
        prolog_transports, prolog_destinations = self._load_prolog_data()
        
        # Merge datasets (Prolog data appended to Python data)
        transports = python_transports + prolog_transports
        
        # Update destinations with Prolog data (if not already present, or override)
        # We append new ones. 
        for pd in prolog_destinations:
            # Check if exists
            existing = next((d for d in destinations if d["city"] == pd["city"]), None)
            if not existing:
                destinations.append(pd)
            else:
                # Optional: Override values from Prolog?
                # Let's assume Prolog is source of truth if provided
                existing.update(pd)

        origin = origin.lower()
        results = []
        
        for t in transports:
            # Handle user typo "tanger" -> "tangier" or vice versa if needed
            # For now, just trust the data matching
            if t.get("origin") == origin:
                dest_city = t.get("dest")
                
                # Apply destination filter if provided
                if dest_filter and dest_city != dest_filter.lower():
                    continue

                dest_info = next((d for d in destinations if d["city"] == dest_city), None)
                
                if dest_info:
                    # Calculate totals based on Type
                    if t["type"] == "car_rental":
                        # Shared vehicle logic
                        # Cost is total for trip (Rental * Days + Driving)
                        # We calculate Total for the GROUP
                        trip_cost_total = estimate_car_cost(t["distance"], days)
                        co2_per_person = t["co2"] / num_people # Shared emissions
                    else:
                        # Ticket based logic
                        # Cost is per person (Ticket * People + Dest * Days * People)
                        # Wait, dest cost is separate. Let's calculate transport component first.
                        trip_cost_total = t["cost"] * num_people
                        co2_per_person = t["co2"]

                    # Add Destination Living Costs (Hotel/Food)
                    # This applies to everyone
                    living_cost_total = (dest_info["cost_per_day"] * days) * num_people
                    living_co2_total = (dest_info["co2_per_day"] * days) * num_people
                    
                    total_cost = trip_cost_total + living_cost_total
                    total_co2 = (co2_per_person * num_people) + living_co2_total
                    
                    if total_cost <= max_budget:
                        # Scoring Logic
                        final_score = self._calculate_score(
                            total_cost, total_co2, float(t["duration"]), 
                            max_budget, num_people, 
                            eco_priority, budget_priority, duration_priority
                        )
                        
                        # Clean type name for display
                        display_type = t["type"].replace("_", " ").title()
                        
                        explanation = f"Trip to {dest_city} via {display_type}: {int(total_cost)} MAD (Total for {num_people}), {int(total_co2)} kg CO2, {t['duration']}h. Score: {final_score:.1f}"
                        
                        results.append({
                            "destination": dest_city,
                            "transport": display_type,
                            "score": float(final_score),
                            "explanation": explanation,
                            "cost": int(total_cost),
                            "co2": int(total_co2),
                            "duration": float(t['duration'])
                        })
                        
        # Sort by score
        return sorted(results, key=lambda x: x['score'], reverse=True)
