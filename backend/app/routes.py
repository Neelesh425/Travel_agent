from fastapi import APIRouter, HTTPException
from app.models import (
    SearchRequest, SearchResponse, BookingRequest, 
    BookingResponse, HistoryItem
)
from app.services.agent import TravelAgent
from typing import List
import asyncio

router = APIRouter()
agent = TravelAgent()

# In-memory storage for search history (use database in production)
search_history: List[HistoryItem] = []

@router.post("/api/search", response_model=SearchResponse)
async def search_flights(request: SearchRequest):
    """
    Search for flights based on user criteria
    """
    try:
        search_params = request.dict()
        response = await agent.process_search(search_params)
        
        # Add to history
        if response.status == "success":
            history_item = HistoryItem(
                search_id=response.search_id,
                search_params=search_params,
                timestamp=response.thoughts[-1].timestamp if response.thoughts else "",
                result_count=len(response.flights)
            )
            search_history.append(history_item)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/book", response_model=BookingResponse)
async def book_flight(request: BookingRequest):
    """
    Book a selected flight
    """
    try:
        result = await agent.make_booking(
            request.flight_id,
            request.passenger_details
        )
        
        return BookingResponse(
            booking_id=result['booking_id'],
            status=result['status'],
            confirmation_code=result.get('confirmation_code'),
            message=result['message']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/history", response_model=List[HistoryItem])
async def get_search_history():
    """
    Get search history
    """
    return search_history[-20:]  # Return last 20 searches

@router.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "Travel booking agent is running"}