from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Destination Schemas
class DestinationBase(BaseModel):
    name: str
    country: str
    description: str
    latitude: float
    longitude: float
    image_url: str
    category: str
    rating: Optional[float] = 4.8
    budget_level: Optional[str] = "$$"
    duration: Optional[str] = "3-5 days"
    weather: Optional[str] = "Sunny"
    highlights: Optional[str] = None

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Wishlist Schemas
class WishlistCreate(BaseModel):
    destination_id: int
    notes: Optional[str] = None

class Wishlist(BaseModel):
    id: int
    user_id: int
    destination_id: int
    destination: Optional[Destination] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Itinerary Item Schemas
class ItineraryItemBase(BaseModel):
    day: int
    time: str
    activity: str
    location: str
    estimated_cost: float = 0.0
    notes: Optional[str] = None
    category: Optional[str] = "Sightseeing"

class ItineraryItemCreate(ItineraryItemBase):
    pass

class ItineraryItem(ItineraryItemBase):
    id: int
    trip_id: int
    model_config = ConfigDict(from_attributes=True)

# Expense Schemas
class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: str
    date: str

class ExpenseCreate(ExpenseBase):
    trip_id: int

class Expense(ExpenseBase):
    id: int
    trip_id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Trip Schemas
class TripBase(BaseModel):
    name: str
    destination: str
    start_date: str
    end_date: str
    travelers: int = 1
    budget: float = 1000.0
    travel_style: str = "Adventure"
    status: Optional[str] = "Upcoming"
    image_url: Optional[str] = None

class TripCreate(TripBase):
    itinerary_items: Optional[List[ItineraryItemBase]] = []

class Trip(TripBase):
    id: int
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    itinerary_items: List[ItineraryItem] = []
    expenses: List[Expense] = []
    model_config = ConfigDict(from_attributes=True)
