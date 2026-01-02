from pyswip import Prolog
import os

prolog = Prolog()
# Get absolute path to logic file
logic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logic/travel_rules.pl"))
# Fix path separators for Prolog (it likes forward slashes)
logic_path = logic_path.replace("\\", "/")

print(f"Loading prolog file from: {logic_path}")
prolog.consult(logic_path)

# Query
# recommend(Origin, MaxBudget, Days, Dest, TransportType, Score, Explanation)
origin = "london"
budget = 1000
days = 5

query = f"recommend({origin}, {budget}, {days}, Dest, Transport, Score, Explanation)"
print(f"Querying: {query}")

results = list(prolog.query(query))

if not results:
    print("No recommendations found.")
else:
    for res in results:
        print(f"Dest: {res['Dest']}, Transport: {res['Transport']}, Score: {res['Score']}")
        print(f"Explanation: {res['Explanation']}")
