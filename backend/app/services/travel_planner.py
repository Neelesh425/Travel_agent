from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.services.flight_api import FlightAPI
from app.services.hotel_api import HotelAPI
from app.services.llm_client import LLMClient
import random

class TravelPlanner:
    def __init__(self):
        self.flight_api = FlightAPI()
        self.hotel_api = HotelAPI()
        self.llm = LLMClient()
    
    async def create_complete_plan(self, travel_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a complete travel plan with flights, hotels, and itinerary
        """
        destination = travel_info.get('destination')
        origin = travel_info.get('origin', 'Delhi')
        budget = travel_info.get('budget', 50000)
        days = travel_info.get('days', 3)
        interests = travel_info.get('interests', [])
        departure_date = travel_info.get('departure_date')
        passengers = travel_info.get('passengers', 1)
        
        # Calculate dates
        if not departure_date:
            departure_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        return_date = (datetime.strptime(departure_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Allocate budget (40% flights, 50% hotels, 10% buffer)
        flight_budget = budget * 0.4
        hotel_budget = budget * 0.5
        hotel_budget_per_night = hotel_budget / days
        
        # Search for flights
        flight_search_params = {
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'passengers': passengers,
            'trip_type': 'round_trip',
            'cabin_class': 'economy' if budget < 80000 else 'business'
        }
        
        flights = await self.flight_api.search_flights(flight_search_params)
        
        # Filter flights within budget
        affordable_flights = [f for f in flights if f.price * passengers * 2 <= flight_budget]
        if not affordable_flights:
            affordable_flights = sorted(flights, key=lambda x: x.price)[:3]
        
        # Select best flight using LLM
        selected_flight = await self._select_best_option(
            [f.dict() for f in affordable_flights],
            'flight',
            interests,
            flight_budget
        )
        
        # Search for hotels
        hotel_search_params = {
            'destination': destination.lower(),
            'budget_per_night': hotel_budget_per_night,
            'interests': interests,
            'check_in': departure_date,
            'check_out': return_date
        }
        
        hotels = await self.hotel_api.search_hotels(hotel_search_params)
        
        # Select best hotel using LLM
        selected_hotel = await self._select_best_option(
            hotels,
            'hotel',
            interests,
            hotel_budget_per_night
        )
        
        # Calculate costs
        flight_cost = selected_flight['price'] * passengers * 2  # Round trip
        hotel_cost = selected_hotel['price_per_night'] * days
        total_cost = flight_cost + hotel_cost
        remaining_budget = budget - total_cost
        
        # Generate day-wise itinerary
        itinerary = await self._generate_itinerary(destination, days, interests)
        
        # Generate summary
        summary = await self.llm.generate_travel_plan_summary({
            'destination': destination,
            'days': days,
            'budget': budget,
            'total_cost': total_cost,
            'flight': selected_flight,
            'hotel': selected_hotel,
            'interests': interests
        })
        
        return {
            'destination': destination,
            'origin': origin,
            'departure_date': departure_date,
            'return_date': return_date,
            'days': days,
            'passengers': passengers,
            'budget': budget,
            'total_cost': total_cost,
            'remaining_budget': remaining_budget,
            'flight': selected_flight,
            'hotel': selected_hotel,
            'itinerary': itinerary,
            'summary': summary,
            'interests': interests
        }
    
    async def _select_best_option(self, options: List[Dict], option_type: str, interests: List[str], budget: float) -> Dict[str, Any]:
        """
        Use LLM to select best option based on interests and budget
        """
        if not options:
            return {}
        
        if option_type == 'flight':
            # For flights, return the first one (already sorted by price)
            return options[0]
        else:
            # For hotels, use interest-based selection
            if 'luxury' in interests or 'relaxation' in interests:
                # Prefer higher rated hotels
                return sorted(options, key=lambda x: x['rating'], reverse=True)[0]
            elif 'budget' in interests or 'adventure' in interests:
                # Prefer cheaper hotels
                return sorted(options, key=lambda x: x['price_per_night'])[0]
            else:
                # Balance of price and rating
                return options[0]
    
    async def _generate_itinerary(self, destination: str, days: int, interests: List[str]) -> List[Dict[str, Any]]:
        """
        Generate day-wise itinerary based on destination and interests
        """
        # Mock itinerary templates
        itinerary_templates = {
            'goa': {
                'relaxation': [
                    {'morning': 'Beach yoga and meditation', 'afternoon': 'Spa treatment', 'evening': 'Sunset at beach'},
                    {'morning': 'Leisure breakfast', 'afternoon': 'Pool relaxation', 'evening': 'Beach dinner'},
                    {'morning': 'Beach walk', 'afternoon': 'Water sports', 'evening': 'Local seafood dinner'}
                ],
                'adventure': [
                    {'morning': 'Scuba diving', 'afternoon': 'Jet skiing', 'evening': 'Beach party'},
                    {'morning': 'Parasailing', 'afternoon': 'Island hopping', 'evening': 'Night market'},
                    {'morning': 'Kayaking', 'afternoon': 'Snorkeling', 'evening': 'Seafood shack'}
                ],
                'food': [
                    {'morning': 'Goan breakfast tour', 'afternoon': 'Spice plantation visit', 'evening': 'Fine dining'},
                    {'morning': 'Local market exploration', 'afternoon': 'Cooking class', 'evening': 'Beach shack dinner'},
                    {'morning': 'Café hopping', 'afternoon': 'Vineyard tour', 'evening': 'Traditional Goan feast'}
                ]
            },
            'default': [
                {'morning': 'City tour and sightseeing', 'afternoon': 'Local attractions', 'evening': 'Traditional dinner'},
                {'morning': 'Cultural exploration', 'afternoon': 'Shopping and leisure', 'evening': 'Local entertainment'},
                {'morning': 'Day trip to nearby attraction', 'afternoon': 'Return and relax', 'evening': 'Farewell dinner'}
            ]
        }
        
        # Select appropriate template
        dest_lower = destination.lower()
        interest_key = interests[0] if interests else 'relaxation'
        
        if dest_lower in itinerary_templates:
            templates = itinerary_templates[dest_lower].get(interest_key, itinerary_templates['default'])
        else:
            templates = itinerary_templates['default']
        
        # Generate itinerary for each day
        itinerary = []
        for day in range(1, days + 1):
            template_index = (day - 1) % len(templates)
            day_plan = templates[template_index]
            
            itinerary.append({
                'day': day,
                'title': f'Day {day} - {destination}',
                'activities': day_plan
            })
        
        return itinerary
    
    async def book_complete_plan(self, plan: Dict[str, Any], passenger_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Book both flight and hotel from the plan
        """
        # Book flight
        flight_booking = await self.flight_api.book_flight(
            plan['flight']['flight_id'],
            passenger_details
        )
        
        # Book hotel
        hotel_booking_details = {
            **passenger_details,
            'check_in': plan['departure_date'],
            'check_out': plan['return_date'],
            'total_amount': plan['hotel']['price_per_night'] * plan['days']
        }
        
        hotel_booking = await self.hotel_api.book_hotel(
            plan['hotel']['hotel_id'],
            hotel_booking_details
        )
        
        return {
            'status': 'success',
            'flight_booking': flight_booking,
            'hotel_booking': hotel_booking,
            'total_cost': plan['total_cost'],
            'message': f"Complete travel plan booked successfully! Total cost: ₹{plan['total_cost']}"
        }