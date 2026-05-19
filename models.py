from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime

class Hostel(Base):
    __tablename__ = "hostels"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    food_quantity_kg = Column(Float)
    food_type = Column(String)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class NGO(Base):
    __tablename__ = "ngos"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity_kg = Column(Float)
    is_active = Column(Boolean, default=True)

class Dispatch(Base):
    __tablename__ = "dispatches"
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer)
    ngo_id = Column(Integer)
    distance_km = Column(Float)
    food_quantity_kg = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)