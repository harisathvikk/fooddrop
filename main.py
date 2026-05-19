from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from routers import hostels, ngos
from vrp import nearest_neighbor, two_opt_improve

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Waste Reducer API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hostels.router)
app.include_router(ngos.router)

@app.get("/")
def root():
    return {"message": "Hyperlocal Food Waste Reducer API running"}

@app.post("/optimize")
def optimize_dispatch(db: Session = Depends(get_db)):
    hostel_list = [
        {"id": h.id, "latitude": h.latitude, "longitude": h.longitude,
         "food_quantity_kg": h.food_quantity_kg, "is_available": h.is_available}
        for h in db.query(models.Hostel).filter(models.Hostel.is_available == True).all()
    ]
    ngo_list = [
        {"id": n.id, "latitude": n.latitude, "longitude": n.longitude,
         "capacity_kg": n.capacity_kg, "is_active": n.is_active}
        for n in db.query(models.NGO).filter(models.NGO.is_active == True).all()
    ]

    assignments = nearest_neighbor(hostel_list, ngo_list)
    optimized = two_opt_improve(assignments, hostel_list, ngo_list)

    total_distance = sum(a["distance_km"] for a in optimized)
    total_food = sum(a["food_quantity_kg"] for a in optimized)

    return {
        "assignments": optimized,
        "total_distance_km": round(total_distance, 2),
        "total_food_redirected_kg": total_food,
        "algorithm": "Nearest-Neighbor + 2-opt VRP Heuristic"
    }