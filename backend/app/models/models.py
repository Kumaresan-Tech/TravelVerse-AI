from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trips = relationship("Trip", back_populates="user")
    wishlists = relationship("Wishlist", back_populates="user")

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
    category = Column(String, index=True)
    rating = Column(Float, default=4.8)
    budget_level = Column(String, default="$$")
    duration = Column(String, default="3-5 days")
    weather = Column(String, default="Sunny")
    highlights = Column(Text, nullable=True) # JSON or comma separated string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="wishlists")
    destination = relationship("Destination")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String)
    destination = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    travelers = Column(Integer, default=1)
    budget = Column(Float, default=1000.0)
    travel_style = Column(String, default="Adventure")
    status = Column(String, default="Upcoming") # Upcoming, Completed, Active
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="trips")
    itinerary_items = relationship("ItineraryItem", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")

class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    day = Column(Integer)
    time = Column(String)
    activity = Column(String)
    location = Column(String)
    estimated_cost = Column(Float, default=0.0)
    notes = Column(String, nullable=True)
    category = Column(String, default="Sightseeing")

    trip = relationship("Trip", back_populates="itinerary_items")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    category = Column(String) # Accommodation, Food, Transport, Activities, Shopping, Other
    amount = Column(Float)
    description = Column(String)
    date = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip", back_populates="expenses")
