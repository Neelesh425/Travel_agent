import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from app.config import get_settings
from app.models import Flight

settings = get_settings()

class FlightAPI:
    def __init__(self):
        self.api_key = settings.flight_api_key
        self.api_url = settings.flight_api_url
    
    async def search_flights(self, search_params: Dict[str, Any]) -> List[Flight]:
        """
        Search for flights based on the given parameters.
        For now, this returns mock data. Replace with actual API calls.
        """
        # Mock data generation for demonstration
        # In production, replace this with actual API calls
        
        airlines = ["Air India", "IndiGo", "SpiceJet", "Vistara", "GoAir"]
        mock_flights = []
        
        base_price = 3000 if search_params.get('cabin_class') == 'economy' else 8000
        
        for i in range(10):
            flight = Flight(
                flight_id=f"FL{random.randint(1000, 9999)}",
                airline=random.choice(airlines),
                flight_number=f"{random.choice(['6E', 'AI', 'SG', 'UK', 'G8'])}{random.randint(100, 999)}",
                departure_time=self._generate_time(search_params['departure_date'], i),
                arrival_time=self._generate_time(search_params['departure_date'], i, hours_offset=random.randint(2, 8)),
                duration=f"{random.randint(2, 8)}h {random.randint(0, 59)}m",
                price=round(base_price + random.uniform(-1000, 3000), 2),
                currency="INR",
                stops=random.choice([0, 1, 2]),
                origin=search_params['origin'],
                destination=search_params['destination'],
                cabin_class=search_params.get('cabin_class', 'economy')
            )
            mock_flights.append(flight)
        
        # Sort by price
        mock_flights.sort(key=lambda x: x.price)
        
        return mock_flights
    
    def _generate_time(self, date_str: str, offset: int, hours_offset: int = 0) -> str:
        """Generate a time string for mock data"""
        base_hour = 6 + offset
        hour = (base_hour + hours_offset) % 24
        minute = random.randint(0, 59)
        return f"{date_str}T{hour:02d}:{minute:02d}:00"
    
    async def get_flight_details(self, flight_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific flight
        """
        # Mock implementation
        return {
            "flight_id": flight_id,
            "details": "Flight details would come from the actual API",
            "baggage": "15kg checked, 7kg cabin",
            "amenities": ["In-flight meals", "Entertainment", "WiFi"]
        }
    
    async def book_flight(self, flight_id: str, passenger_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Book a flight (mock implementation)
        """
        # In production, this would make actual booking API calls
        return {
            "booking_id": f"BK{random.randint(10000, 99999)}",
            "confirmation_code": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}",
            "status": "confirmed",
            "message": "Booking successful! Confirmation email sent."
        }