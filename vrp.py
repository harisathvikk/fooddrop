import math
from typing import List, Dict

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def nearest_neighbor(hostels: List[Dict], ngos: List[Dict]) -> List[Dict]:
    assignments = []
    available_ngos = [n.copy() for n in ngos if n["is_active"]]

    for hostel in hostels:
        if not hostel["is_available"] or not available_ngos:
            continue
        best_ngo = None
        best_dist = float("inf")
        for ngo in available_ngos:
            if ngo["capacity_kg"] >= hostel["food_quantity_kg"]:
                dist = haversine(
                    hostel["latitude"], hostel["longitude"],
                    ngo["latitude"], ngo["longitude"]
                )
                if dist < best_dist:
                    best_dist = dist
                    best_ngo = ngo

        if best_ngo:
            assignments.append({
                "hostel_id": hostel["id"],
                "ngo_id": best_ngo["id"],
                "distance_km": round(best_dist, 2),
                "food_quantity_kg": hostel["food_quantity_kg"]
            })
            best_ngo["capacity_kg"] -= hostel["food_quantity_kg"]

    return assignments

def two_opt_improve(assignments: List[Dict], hostels: List[Dict], ngos: List[Dict]) -> List[Dict]:
    improved = True
    while improved:
        improved = False
        for i in range(len(assignments)):
            for j in range(i + 1, len(assignments)):
                hi = next(h for h in hostels if h["id"] == assignments[i]["hostel_id"])
                hj = next(h for h in hostels if h["id"] == assignments[j]["hostel_id"])
                ni = next(n for n in ngos if n["id"] == assignments[i]["ngo_id"])
                nj = next(n for n in ngos if n["id"] == assignments[j]["ngo_id"])

                old_dist = haversine(hi["latitude"], hi["longitude"], ni["latitude"], ni["longitude"]) + \
                           haversine(hj["latitude"], hj["longitude"], nj["latitude"], nj["longitude"])
                new_dist = haversine(hi["latitude"], hi["longitude"], nj["latitude"], nj["longitude"]) + \
                           haversine(hj["latitude"], hj["longitude"], ni["latitude"], ni["longitude"])

                if new_dist < old_dist - 0.01:
                    assignments[i]["ngo_id"], assignments[j]["ngo_id"] = assignments[j]["ngo_id"], assignments[i]["ngo_id"]
                    assignments[i]["distance_km"] = round(new_dist / 2, 2)
                    assignments[j]["distance_km"] = round(new_dist / 2, 2)
                    improved = True
    return assignments