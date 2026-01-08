from fastapi import APIRouter, HTTPException
from app.models import (
    SearchRequest, SearchResponse, BookingRequest, 
    BookingResponse, HistoryItem, AutonomousBookingRequest,
    AutonomousBookingResponse, ChatRequest, ChatResponse,
    TravelPlanRequest, TravelPlan, CompletePlanBookingRequest,
    CompletePlanBookingResponse, ChatMessage
)
from app.services.agent import TravelAgent
from app.services.llm_client import LLMClient
from app.services.travel_planner import TravelPlanner
from typing import List
import asyncio
from datetime import datetime

router = APIRouter()
agent = TravelAgent()
llm_client = LLMClient()
travel_planner = TravelPlanner()

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

@router.post("/api/search-and-book", response_model=AutonomousBookingResponse)
async def search_and_book_autonomous(request: AutonomousBookingRequest):
    """
    Autonomous booking: Search for flights and automatically book the best option
    """
    try:
        search_params = request.search_params.dict()
        passenger_details = request.passenger_details
        
        result = await agent.process_search_and_book(search_params, passenger_details)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        # Add to history
        history_item = HistoryItem(
            search_id=result['search_id'],
            search_params=search_params,
            timestamp=result['thoughts'][-1].timestamp if result['thoughts'] else "",
            result_count=len(result['all_flights'])
        )
        search_history.append(history_item)
        
        return AutonomousBookingResponse(
            search_id=result['search_id'],
            status=result['status'],
            thoughts=result['thoughts'],
            all_flights=result['all_flights'],
            selected_flight=result['selected_flight'],
            selection_reason=result['selection_reason'],
            booking_result=result['booking_result'],
            message=result['message']
        )
    except HTTPException:
        raise
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

# New endpoints for conversational travel planning

@router.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Conversational endpoint for travel planning
    """
    try:
        user_message = request.message
        conversation_history = request.conversation_history
        extracted_info = request.extracted_info or {}
        
        # Extract information from user message
        updated_info = await llm_client.extract_travel_info(user_message, extracted_info)
        
        # Check if we have enough information
        required_fields = ['destination', 'budget', 'days']
        has_all_info = all(updated_info.get(field) for field in required_fields)
        
        # Generate response
        if has_all_info:
            ai_message = "Perfect! I have all the information I need. Let me create an amazing travel plan for you! 🌟"
        else:
            ai_message = await llm_client.generate_next_question(updated_info)
        
        # Update conversation history
        updated_history = conversation_history + [
            ChatMessage(role="user", content=user_message, timestamp=datetime.now().isoformat()),
            ChatMessage(role="ai", content=ai_message, timestamp=datetime.now().isoformat())
        ]
        
        return ChatResponse(
            message=ai_message,
            extracted_info=updated_info,
            is_ready_to_plan=has_all_info,
            conversation_history=updated_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/plan-travel", response_model=TravelPlan)
async def create_travel_plan(request: TravelPlanRequest):
    """
    Create a complete travel plan with flights, hotels, and itinerary
    """
    try:
        travel_info = request.dict()
        plan = await travel_planner.create_complete_plan(travel_info)
        
        return TravelPlan(**plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/book-complete-plan", response_model=CompletePlanBookingResponse)
async def book_complete_plan(request: CompletePlanBookingRequest):
    """
    Book the complete travel plan (flight + hotel)
    """
    try:
        plan = request.plan.dict()
        passenger_details = request.passenger_details
        
        result = await travel_planner.book_complete_plan(plan, passenger_details)
        
        return CompletePlanBookingResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))