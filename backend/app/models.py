from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TripType(str, Enum):
    ONE_WAY = "one_way"
    ROUND_TRIP = "round_trip"

class SearchRequest(BaseModel):
    origin: str = Field(..., description="Departure city or airport code")
    destination: str = Field(..., description="Arrival city or airport code")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date for round trip")
    passengers: int = Field(1, ge=1, le=9, description="Number of passengers")
    trip_type: TripType = Field(TripType.ONE_WAY, description="Type of trip")
    cabin_class: str = Field("economy", description="Cabin class preference")

class Flight(BaseModel):
    flight_id: str
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    currency: str
    stops: int
    origin: str
    destination: str
    cabin_class: str

class AgentThought(BaseModel):
    step: int
    thought: str
    action: str
    timestamp: str

class SearchResponse(BaseModel):
    search_id: str
    status: str
    thoughts: List[AgentThought]
    flights: List[Flight]
    message: str
    search_params: Dict[str, Any]

class BookingRequest(BaseModel):
    flight_id: str
    passenger_details: Dict[str, Any]

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: Optional[str]
    message: str

class AutonomousBookingRequest(BaseModel):
    search_params: SearchRequest
    passenger_details: Dict[str, Any] = Field(..., description="Passenger information for booking")

class AutonomousBookingResponse(BaseModel):
    search_id: str
    status: str
    thoughts: List[AgentThought]
    all_flights: List[Dict[str, Any]]
    selected_flight: Dict[str, Any]
    selection_reason: str
    booking_result: Dict[str, Any]
    message: str

class HistoryItem(BaseModel):
    search_id: str
    search_params: Dict[str, Any]
    timestamp: str
    result_count: int

# New models for conversational travel planning

class ChatMessage(BaseModel):
    role: str = Field(..., description="Either 'user' or 'ai'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    conversation_history: List[ChatMessage] = Field(default=[], description="Previous conversation")
    extracted_info: Optional[Dict[str, Any]] = Field(default={}, description="Previously extracted travel info")

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response")
    extracted_info: Dict[str, Any] = Field(..., description="Extracted travel information")
    is_ready_to_plan: bool = Field(..., description="Whether we have enough info to generate plan")
    conversation_history: List[ChatMessage] = Field(..., description="Updated conversation history")

class TravelPlanRequest(BaseModel):
    destination: str
    origin: Optional[str] = Field(default="Delhi")
    budget: float
    days: int
    interests: List[str] = Field(default=[])
    departure_date: Optional[str] = None
    passengers: int = Field(default=1)

class Hotel(BaseModel):
    hotel_id: str
    name: str
    category: str
    rating: float
    price_per_night: float
    currency: str
    location: str
    amenities: List[str]
    available_rooms: int
    distance_from_center: str

class DayItinerary(BaseModel):
    day: int
    title: str
    activities: Dict[str, str]

class TravelPlan(BaseModel):
    destination: str
    origin: str
    departure_date: str
    return_date: str
    days: int
    passengers: int
    budget: float
    total_cost: float
    remaining_budget: float
    flight: Dict[str, Any]
    hotel: Dict[str, Any]
    itinerary: List[DayItinerary]
    summary: str
    interests: List[str]

class CompletePlanBookingRequest(BaseModel):
    plan: TravelPlan
    passenger_details: Dict[str, Any]

class CompletePlanBookingResponse(BaseModel):
    status: str
    flight_booking: Dict[str, Any]
    hotel_booking: Dict[str, Any]
    total_cost: float
    message: str