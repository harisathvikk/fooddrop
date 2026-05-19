from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Hostel
from pydantic import BaseModel

router = APIRouter(prefix="/hostels", tags=["Hostels"])

class HostelCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    food_quantity_kg: float
    food_type: str

@router.post("/")
def add_hostel(data: HostelCreate, db: Session = Depends(get_db)):
    hostel = Hostel(**data.dict())
    db.add(hostel)
    db.commit()
    db.refresh(hostel)
    return hostel

@router.get("/")
def list_hostels(db: Session = Depends(get_db)):
    return db.query(Hostel).all()