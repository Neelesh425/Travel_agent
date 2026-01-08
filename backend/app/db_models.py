from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    """User table - for future authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = relationship("SearchHistory", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    travel_plans = relationship("TravelPlan", back_populates="user")

class SearchHistory(Base):
    """Search history table"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(String(100), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Search parameters
    origin = Column(String(100))
    destination = Column(String(100))
    departure_date = Column(String(50))
    return_date = Column(String(50), nullable=True)
    passengers = Column(Integer)
    trip_type = Column(String(50))
    cabin_class = Column(String(50))
    
    # Results
    result_count = Column(Integer)
    search_status = Column(String(50))  # 'success', 'error'
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    bookings = relationship("Booking", back_populates="search")

class Booking(Base):
    """Bookings table"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(100), unique=True, index=True)
    search_id = Column(String(100), ForeignKey("search_history.search_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Booking details
    flight_id = Column(String(100), nullable=True)
    hotel_id = Column(String(100), nullable=True)
    booking_type = Column(String(50))  # 'flight_only', 'hotel_only', 'complete_plan', 'autonomous'
    
    # Passenger details
    passenger_first_name = Column(String(100))
    passenger_last_name = Column(String(100))
    passenger_email = Column(String(255))
    passenger_phone = Column(String(50))
    
    # Flight details (stored as JSON)
    flight_details = Column(JSON, nullable=True)
    hotel_details = Column(JSON, nullable=True)
    
    # Financial
    total_amount = Column(Float)
    currency = Column(String(10), default="INR")
    
    # Status
    status = Column(String(50), default="confirmed")  # 'confirmed', 'cancelled', 'pending'
    confirmation_code = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    search = relationship("SearchHistory", back_populates="bookings")

class TravelPlan(Base):
    """Travel plans table - for conversational planning"""
    __tablename__ = "travel_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(String(100), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Plan basics
    destination = Column(String(100))
    origin = Column(String(100))
    departure_date = Column(String(50))
    return_date = Column(String(50))
    days = Column(Integer)
    passengers = Column(Integer)
    
    # Budget
    budget = Column(Float)
    total_cost = Column(Float)
    remaining_budget = Column(Float)
    
    # Interests (stored as JSON array)
    interests = Column(JSON)
    
    # Complete plan (stored as JSON)
    plan_json = Column(JSON)
    
    # Status
    is_booked = Column(Integer, default=0)  # 0 = not booked, 1 = booked
    booking_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="travel_plans")

class Conversation(Base):
    """Conversation history - for chat feature"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Conversation data
    messages = Column(JSON)  # Array of messages
    extracted_info = Column(JSON)  # Extracted travel info
    
    # Status
    is_completed = Column(Integer, default=0)  # 0 = ongoing, 1 = completed
    resulted_in_plan = Column(Integer, default=0)  # 0 = no, 1 = yes
    plan_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)