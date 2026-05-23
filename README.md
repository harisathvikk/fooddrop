# 🌿 FoodDrop — Hyperlocal Food Waste Reducer

> Connecting hostels and canteens to nearby NGOs using optimized routing algorithms.  
> Built for **DAA + DevOps** | 4th Semester Project

---

## 📌 Problem Statement

Thousands of kilograms of surplus food go to waste daily in hostels and canteens while nearby NGOs struggle to source food for those in need. The challenge is not availability — it's **routing and coordination**.

FoodDrop solves this by modeling the dispatch problem as a **Vehicle Routing Problem (VRP)** and applying a heuristic algorithm to find near-optimal routes in polynomial time.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| Database | SQLite via SQLAlchemy |
| Algorithm | Nearest-Neighbor + 2-opt VRP Heuristic |
| Frontend | HTML/CSS/JS Dashboard |
| Containerization | Docker + Docker Compose |
| Version Control | Git + GitHub |

---

## 🧠 Algorithm Design (DAA Core)

### Problem: Vehicle Routing Problem (VRP)
The VRP is a classical **NP-Hard** combinatorial optimization problem. Given a set of food sources (hostels) and destinations (NGOs), find the minimum-distance assignment such that:
- Every hostel is assigned to exactly one NGO
- No NGO exceeds its food capacity
- Total travel distance is minimized

### Exact solution complexity: **O(n!)** — infeasible for large inputs

### Our Approach: 2-Phase Heuristic

**Phase 1 — Nearest Neighbor (Greedy)**
```
For each hostel (sorted by food quantity):
    Find the nearest NGO with sufficient capacity
    Assign hostel → NGO
    Reduce NGO remaining capacity
Time complexity: O(H × N)  where H = hostels, N = NGOs
```

**Phase 2 — 2-opt Local Search**
```
While improvement exists:
    For each pair of assignments (i, j):
        Try swapping their NGO assignments
        If total distance decreases → accept swap
Time complexity: O(n²) per iteration
```

### Distance Metric: Haversine Formula
Real-world geographic distance on a sphere — accounts for Earth's curvature.

```python
d = 2R × arctan2(√a, √(1−a))
where a = sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2)
```

### Approximation Guarantee
The Nearest-Neighbor + 2-opt heuristic achieves an approximation ratio of **≤ 2× optimal** for metric VRP instances (satisfying triangle inequality).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/danishhhh05/fooddrop.git
cd fooddrop
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API
```bash
uvicorn main:app --reload
```

### 5. Open the dashboard
Open `dashboard.html` in your browser.

API docs available at: `http://127.0.0.1:8000/docs`

---

## 🐳 Run with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/hostels/` | Register a hostel |
| GET | `/hostels/` | List all hostels |
| POST | `/ngos/` | Register an NGO |
| GET | `/ngos/` | List all NGOs |
| POST | `/optimize` | Run VRP optimizer |

### Sample `/optimize` Response
```json
{
  "assignments": [
    {
      "hostel_id": 1,
      "ngo_id": 1,
      "distance_km": 1.92,
      "food_quantity_kg": 15.0
    }
  ],
  "total_distance_km": 1.92,
  "total_food_redirected_kg": 15.0,
  "algorithm": "Nearest-Neighbor + 2-opt VRP Heuristic"
}
```

---

## 📁 Project Structure

```
fooddrop/
├── main.py              # FastAPI app + optimize endpoint
├── models.py            # SQLAlchemy database models
├── database.py          # DB connection and session
├── vrp.py               # VRP algorithm (NN + 2-opt + Haversine)
├── routers/
│   ├── hostels.py       # Hostel CRUD routes
│   └── ngos.py          # NGO CRUD routes
├── dashboard.html       # Frontend UI
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-container orchestration
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🗺️ System Architecture

```
Hostel App  ──┐
              ├──▶  FastAPI Gateway  ──▶  VRP Optimizer  ──▶  Dispatch Result
NGO Dashboard─┘         │                    │
                         ▼                    ▼
                    SQLite DB           Haversine Distance
                    (Hostels,           Nearest-Neighbor
                     NGOs,              + 2-opt Heuristic
                     Dispatches)
```

---

## 👨‍💻 Author


**Hari Sathvik** —
 AI/ML Engineer GitHub: [@harisathvikk](https://github.com/harisathvikk)
---

## 📄 License

MIT License
