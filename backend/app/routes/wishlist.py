from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.auth import get_current_user_optional

router = APIRouter()

@router.get("/", response_model=List[schemas.Wishlist])
def get_wishlist(db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_current_user_optional)):
    user_id = current_user.id if current_user else 1
    items = db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).all()
    return items

@router.post("/", response_model=schemas.Wishlist)
def add_to_wishlist(
    item_data: schemas.WishlistCreate,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else 1
    
    # Check if already in wishlist
    existing = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == user_id,
        models.Wishlist.destination_id == item_data.destination_id
    ).first()
    
    if existing:
        return existing
        
    db_item = models.Wishlist(
        user_id=user_id,
        destination_id=item_data.destination_id,
        notes=item_data.notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{destination_id}")
def remove_from_wishlist(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else 1
    item = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == user_id,
        models.Wishlist.destination_id == destination_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
        
    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
