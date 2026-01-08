from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models import (
    SearchRequest, SearchResponse, BookingRequest, 
    BookingResponse, HistoryItem, AutonomousBookingRequest,
    AutonomousBookingResponse, ChatRequest, ChatResponse,
    TravelPlanRequest, TravelPlan, CompletePlanBookingRequest,
    CompletePlanBookingResponse, ChatMessage
)
from app.db_models import SearchHistory, Booking, TravelPlan as DBTravelPlan
from app.database import get_db
from app.services.agent import TravelAgent
from app.services.llm_client import LLMClient
from app.services.travel_planner import TravelPlanner
from typing import List, Optional
import asyncio
from datetime import datetime
import uuid

router = APIRouter()
agent = TravelAgent()
llm_client = LLMClient()
travel_planner = TravelPlanner()

@router.post("/api/search", response_model=SearchResponse)
async def search_flights(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Search for flights based on user criteria
    """
    try:
        search_params = request.dict()
        response = await agent.process_search(search_params)
        
        # Save to database
        if response.status == "success":
            db_search = SearchHistory(
                search_id=response.search_id,
                origin=search_params.get('origin'),
                destination=search_params.get('destination'),
                departure_date=search_params.get('departure_date'),
                return_date=search_params.get('return_date'),
                passengers=search_params.get('passengers', 1),
                trip_type=search_params.get('trip_type', 'one_way'),
                cabin_class=search_params.get('cabin_class', 'economy'),
                result_count=len(response.flights),
                search_status='success'
            )
            db.add(db_search)
            db.commit()
            db.refresh(db_search)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/search-and-book", response_model=AutonomousBookingResponse)
async def search_and_book_autonomous(request: AutonomousBookingRequest, db: Session = Depends(get_db)):
    """
    Autonomous booking: Search for flights and automatically book the best option
    """
    try:
        search_params = request.search_params.dict()
        passenger_details = request.passenger_details
        
        result = await agent.process_search_and_book(search_params, passenger_details)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        # Save search to database
        db_search = SearchHistory(
            search_id=result['search_id'],
            origin=search_params.get('origin'),
            destination=search_params.get('destination'),
            departure_date=search_params.get('departure_date'),
            return_date=search_params.get('return_date'),
            passengers=search_params.get('passengers', 1),
            trip_type=search_params.get('trip_type', 'one_way'),
            cabin_class=search_params.get('cabin_class', 'economy'),
            result_count=len(result['all_flights']),
            search_status='success'
        )
        db.add(db_search)
        db.commit()
        
        # Save booking to database
        db_booking = Booking(
            booking_id=result['booking_result']['booking_id'],
            search_id=result['search_id'],
            flight_id=result['selected_flight']['flight_id'],
            booking_type='autonomous',
            passenger_first_name=passenger_details.get('firstName'),
            passenger_last_name=passenger_details.get('lastName'),
            passenger_email=passenger_details.get('email'),
            passenger_phone=passenger_details.get('phone'),
            flight_details=result['selected_flight'],
            total_amount=result['selected_flight']['price'],
            currency=result['selected_flight']['currency'],
            status='confirmed',
            confirmation_code=result['booking_result'].get('confirmation_code')
        )
        db.add(db_booking)
        db.commit()
        
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
async def book_flight(request: BookingRequest, db: Session = Depends(get_db)):
    """
    Book a selected flight
    """
    try:
        result = await agent.make_booking(
            request.flight_id,
            request.passenger_details
        )
        
        # Save booking to database
        db_booking = Booking(
            booking_id=result['booking_id'],
            flight_id=request.flight_id,
            booking_type='flight_only',
            passenger_first_name=request.passenger_details.get('firstName'),
            passenger_last_name=request.passenger_details.get('lastName'),
            passenger_email=request.passenger_details.get('email'),
            passenger_phone=request.passenger_details.get('phone'),
            total_amount=0,  # Would come from flight details
            status='confirmed',
            confirmation_code=result.get('confirmation_code')
        )
        db.add(db_booking)
        db.commit()
        
        return BookingResponse(
            booking_id=result['booking_id'],
            status=result['status'],
            confirmation_code=result.get('confirmation_code'),
            message=result['message']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/history")
async def get_search_history(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    destination: Optional[str] = None,
    origin: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Get search history with filters and pagination
    """
    try:
        # Build query
        query = db.query(SearchHistory)
        
        # Apply filters
        if destination:
            query = query.filter(SearchHistory.destination.ilike(f"%{destination}%"))
        if origin:
            query = query.filter(SearchHistory.origin.ilike(f"%{origin}%"))
        if status:
            query = query.filter(SearchHistory.search_status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        searches = query.order_by(SearchHistory.created_at.desc()).offset(offset).limit(limit).all()
        
        # Convert to response format
        history_items = []
        for search in searches:
            # Get related bookings
            bookings = db.query(Booking).filter(Booking.search_id == search.search_id).all()
            
            history_items.append({
                "search_id": search.search_id,
                "origin": search.origin,
                "destination": search.destination,
                "departure_date": search.departure_date,
                "return_date": search.return_date,
                "passengers": search.passengers,
                "cabin_class": search.cabin_class,
                "result_count": search.result_count,
                "search_status": search.search_status,
                "created_at": search.created_at.isoformat(),
                "bookings": [
                    {
                        "booking_id": b.booking_id,
                        "confirmation_code": b.confirmation_code,
                        "status": b.status,
                        "total_amount": b.total_amount
                    } for b in bookings
                ]
            })
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": history_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/bookings")
async def get_bookings(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None
):
    """
    Get all bookings with filters
    """
    try:
        query = db.query(Booking)
        
        if status:
            query = query.filter(Booking.status == status)
        
        total = query.count()
        bookings = query.order_by(Booking.created_at.desc()).offset(offset).limit(limit).all()
        
        booking_list = []
        for booking in bookings:
            booking_list.append({
                "booking_id": booking.booking_id,
                "booking_type": booking.booking_type,
                "passenger_name": f"{booking.passenger_first_name} {booking.passenger_last_name}",
                "passenger_email": booking.passenger_email,
                "flight_details": booking.flight_details,
                "hotel_details": booking.hotel_details,
                "total_amount": booking.total_amount,
                "currency": booking.currency,
                "status": booking.status,
                "confirmation_code": booking.confirmation_code,
                "created_at": booking.created_at.isoformat()
            })
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": booking_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "Travel booking agent is running", "database": "SQLite"}

# Conversational endpoints

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
async def create_travel_plan(request: TravelPlanRequest, db: Session = Depends(get_db)):
    """
    Create a complete travel plan with flights, hotels, and itinerary
    """
    try:
        travel_info = request.dict()
        plan = await travel_planner.create_complete_plan(travel_info)
        
        # Save plan to database
        plan_id = str(uuid.uuid4())
        db_plan = DBTravelPlan(
            plan_id=plan_id,
            destination=plan['destination'],
            origin=plan['origin'],
            departure_date=plan['departure_date'],
            return_date=plan['return_date'],
            days=plan['days'],
            passengers=plan['passengers'],
            budget=plan['budget'],
            total_cost=plan['total_cost'],
            remaining_budget=plan['remaining_budget'],
            interests=plan['interests'],
            plan_json=plan,
            is_booked=0
        )
        db.add(db_plan)
        db.commit()
        
        return TravelPlan(**plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/book-complete-plan", response_model=CompletePlanBookingResponse)
async def book_complete_plan(request: CompletePlanBookingRequest, db: Session = Depends(get_db)):
    """
    Book the complete travel plan (flight + hotel)
    """
    try:
        plan = request.plan.dict()
        passenger_details = request.passenger_details
        
        result = await travel_planner.book_complete_plan(plan, passenger_details)
        
        # Save booking to database
        db_booking = Booking(
            booking_id=result['flight_booking']['booking_id'],
            flight_id=plan['flight']['flight_id'],
            hotel_id=plan['hotel']['hotel_id'],
            booking_type='complete_plan',
            passenger_first_name=passenger_details.get('firstName'),
            passenger_last_name=passenger_details.get('lastName'),
            passenger_email=passenger_details.get('email'),
            passenger_phone=passenger_details.get('phone'),
            flight_details=plan['flight'],
            hotel_details=plan['hotel'],
            total_amount=plan['total_cost'],
            currency='INR',
            status='confirmed',
            confirmation_code=result['flight_booking'].get('confirmation_code')
        )
        db.add(db_booking)
        db.commit()
        
        return CompletePlanBookingResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))