from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import NGO
from pydantic import BaseModel

router = APIRouter(prefix="/ngos", tags=["NGOs"])

class NGOCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    capacity_kg: float

@router.post("/")
def add_ngo(data: NGOCreate, db: Session = Depends(get_db)):
    ngo = NGO(**data.dict())
    db.add(ngo)
    db.commit()
    db.refresh(ngo)
    return ngo

@router.get("/")
def list_ngos(db: Session = Depends(get_db)):
    return db.query(NGO).all()