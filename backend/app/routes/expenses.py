from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.get("/trip/{trip_id}", response_model=List[schemas.Expense])
def get_trip_expenses(trip_id: int, db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).filter(models.Expense.trip_id == trip_id).all()
    return expenses

@router.post("/", response_model=schemas.Expense)
def add_expense(expense_data: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    trip = db.query(models.Trip).filter(models.Trip.id == expense_data.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    db_expense = models.Expense(**expense_data.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}
