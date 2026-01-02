from fastapi import FastAPI

import sys
import os

# Ensure logic module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic.engine import LogicEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from pydantic import BaseModel
from typing import List, Optional
import os

class Preference(BaseModel):
    origin: str
    max_budget: float
    duration_days: int
    num_people: int = 1
    destination_filter: Optional[str] = None
    eco_priority: int = 50
    budget_priority: int = 30
    duration_priority: int = 20

class Recommendation(BaseModel):
    destination: str
    transport: str
    score: float
    explanation: str
    cost: float
    co2: float
    duration: float

# Init Logic Engine
logic_engine = LogicEngine()
logic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logic/travel_rules.pl"))
logic_engine.load_rules(logic_path)

@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "prolog_available": logic_engine.prolog_available
    }

@app.post("/recommend", response_model=List[Recommendation])
def recommend(prefs: Preference):
    # LogicEngine handles fallback
    results = logic_engine.recommend(
        prefs.origin, 
        prefs.max_budget, 
        prefs.duration_days, 
        prefs.destination_filter,
        prefs.num_people,
        prefs.eco_priority,
        prefs.budget_priority,
        prefs.duration_priority
    )
    
    recommendations = []
    for res in results:
        recommendations.append(Recommendation(
            destination=res['destination'],
            transport=res['transport'],
            score=res['score'],
            explanation=res['explanation'],
            cost=res['cost'],
            co2=res['co2'],
            duration=res['duration']
        ))
        
    return recommendations
