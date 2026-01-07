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

class HistoryItem(BaseModel):
    search_id: str
    search_params: Dict[str, Any]
    timestamp: str
    result_count: int