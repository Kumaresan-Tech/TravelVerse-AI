from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.auth import get_current_user_optional

router = APIRouter()

@router.get("/", response_model=List[schemas.Trip])
def get_trips(db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_current_user_optional)):
    user_id = current_user.id if current_user else 1
    trips = db.query(models.Trip).filter((models.Trip.user_id == user_id) | (models.Trip.user_id == None)).all()
    return trips

@router.get("/{trip_id}", response_model=schemas.Trip)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/", response_model=schemas.Trip)
def create_trip(
    trip_data: schemas.TripCreate,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else 1
    
    trip_dict = trip_data.model_dump(exclude={"itinerary_items"})
    db_trip = models.Trip(**trip_dict, user_id=user_id)
    if not db_trip.image_url:
        # Default destination image fallback
        db_trip.image_url = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"
    
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    # Save itinerary items if provided
    if trip_data.itinerary_items:
        for item in trip_data.itinerary_items:
            db_item = models.ItineraryItem(**item.model_dump(), trip_id=db_trip.id)
            db.add(db_item)
        db.commit()
        db.refresh(db_trip)

    return db_trip

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}

@router.post("/{trip_id}/itinerary", response_model=schemas.ItineraryItem)
def add_itinerary_item(trip_id: int, item_data: schemas.ItineraryItemCreate, db: Session = Depends(get_db)):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db_item = models.ItineraryItem(**item_data.model_dump(), trip_id=trip_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
