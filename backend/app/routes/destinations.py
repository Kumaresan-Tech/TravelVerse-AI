from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Destination])
def get_destinations(
    category: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(get_db)
):
    query = db.query(models.Destination)
    if category and category.lower() != "all":
        query = query.filter(models.Destination.category.ilike(f"%{category}%"))
    if q:
        search_pattern = f"%{q}%"
        query = query.filter(
            (models.Destination.name.ilike(search_pattern)) |
            (models.Destination.country.ilike(search_pattern)) |
            (models.Destination.description.ilike(search_pattern))
        )
    destinations = query.offset(skip).limit(limit).all()
    return destinations

@router.get("/{destination_id}", response_model=schemas.Destination)
def get_destination(destination_id: str, db: Session = Depends(get_db)):
    if destination_id.isdigit():
        destination = db.query(models.Destination).filter(models.Destination.id == int(destination_id)).first()
    else:
        destination = db.query(models.Destination).filter(models.Destination.name.ilike(f"%{destination_id}%")).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@router.post("/", response_model=schemas.Destination)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    db_destination = models.Destination(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

@router.delete("/{destination_id}")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    db.delete(dest)
    db.commit()
    return {"message": "Destination deleted successfully"}
