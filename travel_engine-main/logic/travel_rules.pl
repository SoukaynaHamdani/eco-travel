% Knowledge Base

% Destinations: destination(City, Country, BaseCostPerDay, BaseCO2PerDay)
destination(marrakech, morocco, 80, 12).
destination(fes, morocco, 60, 10).
destination(casablanca, morocco, 90, 15).
destination(tanger, morocco, 70, 12).
destination(chefchaouen, morocco, 50, 8).
destination(essaouira, morocco, 60, 10).
destination(rabat, morocco, 75, 12).
destination(ouarzazate, morocco, 55, 10).

% Transport: transport(Origin, Dest, Type, Cost, CO2, DurationHours)

% International Flights (Removed per user request)

% Domestic Trains (ONCF Realism)
transport(casablanca, marrakech, train, 15, 5, 2.5).
transport(casablanca, fes, train, 12, 6, 4).
transport(casablanca, tanger, high_speed_train, 25, 4, 2.1).
transport(casablanca, rabat, train, 8, 2, 1).
transport(tanger, rabat, high_speed_train, 15, 3, 1.2).
transport(rabat, fes, train, 10, 4, 2.5).
transport(marrakech, fes, train, 20, 8, 6.5).

% Domestic Bus / Collective Taxi (CTM / Supratours) / Trains (Expanded)
transport(marrakech, essaouira, bus, 10, 3, 3).
transport(marrakech, ouarzazate, bus, 15, 4, 4.5).
transport(tanger, chefchaouen, taxi, 10, 5, 2).
transport(fes, chefchaouen, bus, 12, 4, 4).

% Missing Connectivity (Casablanca)
transport(casablanca, chefchaouen, bus, 20, 6, 5.5).
transport(casablanca, ouarzazate, bus, 25, 7, 6.5).

% Missing Connectivity (Marrakech)
transport(marrakech, tanger, train, 35, 9, 3.5). % Via Casa
transport(marrakech, chefchaouen, bus, 30, 10, 8.5).
transport(marrakech, meknes, train, 22, 6, 4.5).

% Missing Connectivity (Fes)
transport(fes, essaouira, bus, 30, 10, 9).
transport(fes, ouarzazate, bus, 35, 12, 10).
transport(fes, agadir, bus, 32, 11, 9).
transport(fes, marrakech, train, 22, 6, 4.5).
transport(fes, tanger, train, 22, 6, 4.5).
transport(fes, chefchaouen, train, 22, 6, 4.5).

% Missing Connectivity (Rabat)
transport(rabat, chefchaouen, bus, 15, 5, 4.5).
transport(rabat, essaouira, bus, 25, 8, 7).
transport(rabat, ouarzazate, bus, 30, 9, 7.5).
transport(rabat, agadir, bus, 28, 9, 7).

% Missing Connectivity (tanger)
transport(tanger, marrakech, train, 35, 9, 3.5). % Via Casa
transport(tanger, essaouira, bus, 35, 10, 8).
transport(tanger, ouarzazate, bus, 40, 12, 10).
transport(tanger, agadir, bus, 38, 11, 9).

% NEW: Test Route PROLOG-BRIDGE
transport(marrakech, tanger, flight_prolog_test, 555, 100, 1.1).

% Rules

% Calculate total cost
% TripCost = TransportCost + (DestCostPerDay * Days)
total_cost(Origin, Dest, TransportType, Days, Cost) :-
    transport(Origin, Dest, TransportType, TCost, _, _),
    destination(Dest, _, DCost, _),
    Cost is TCost + (DCost * Days).

% Calculate total CO2
% TripCO2 = TransportCO2 + (DestCO2PerDay * Days)
total_co2(Origin, Dest, TransportType, Days, CO2) :-
    transport(Origin, Dest, TransportType, _, TCO2, _),
    destination(Dest, _, _, DCO2),
    CO2 is TCO2 + (DCO2 * Days).

% Scoring: Lower is better for Cost and CO2.
% We can normalize or just use a weighted sum.
% Score = (Cost * CostWeight) + (CO2 * CO2Weight).
% Let's assume CostWeight=1, CO2Weight=2 (user cares more about eco).

score_trip(Origin, Dest, Days, TransportType, Score, Explanation) :-
    total_cost(Origin, Dest, TransportType, Days, Cost),
    total_co2(Origin, Dest, TransportType, Days, CO2),
    Score is (Cost * 1) + (CO2 * 2),
    format(atom(Explanation), 'Trip to ~w via ~w: ~w EUR, ~w kg CO2. Score: ~w', [Dest, TransportType, Cost, CO2, Score]).

% Recommendation: Find trips within Budget.
recommend(Origin, MaxBudget, Days, Dest, TransportType, Score, Explanation, Cost, CO2, Duration) :-
    transport(Origin, Dest, TransportType, _, _, Duration),
    total_cost(Origin, Dest, TransportType, Days, Cost),
    Cost =< MaxBudget,
    total_co2(Origin, Dest, TransportType, Days, CO2),
    score_trip(Origin, Dest, Days, TransportType, Score, Explanation).