import random
from typing import List, Dict, Any
from datetime import datetime, timedelta

class HotelAPI:
    def __init__(self):
        self.hotels_database = {
            "goa": [
                {"name": "Taj Exotica", "category": "luxury", "base_price": 8000, "rating": 4.8, "amenities": ["Pool", "Spa", "Beach Access", "Restaurant"]},
                {"name": "The Leela Goa", "category": "luxury", "base_price": 7500, "rating": 4.7, "amenities": ["Golf Course", "Spa", "Beach Access", "Multiple Restaurants"]},
                {"name": "Alila Diwa", "category": "premium", "base_price": 5500, "rating": 4.6, "amenities": ["Pool", "Spa", "Gym", "Restaurant"]},
                {"name": "Novotel Goa", "category": "premium", "base_price": 4500, "rating": 4.4, "amenities": ["Pool", "Beach Access", "Restaurant", "Bar"]},
                {"name": "Fortune Miramar", "category": "mid-range", "base_price": 3000, "rating": 4.2, "amenities": ["Pool", "Restaurant", "Room Service"]},
                {"name": "Ginger Goa", "category": "budget", "base_price": 2000, "rating": 3.9, "amenities": ["WiFi", "Restaurant", "Parking"]},
                {"name": "FabHotel Palm Grove", "category": "budget", "base_price": 1500, "rating": 3.8, "amenities": ["WiFi", "AC", "Room Service"]},
            ],
            "mumbai": [
                {"name": "The Taj Mahal Palace", "category": "luxury", "base_price": 12000, "rating": 4.9, "amenities": ["Pool", "Spa", "Multiple Restaurants", "Sea View"]},
                {"name": "The Oberoi Mumbai", "category": "luxury", "base_price": 11000, "rating": 4.8, "amenities": ["Pool", "Spa", "Fine Dining", "Business Center"]},
                {"name": "JW Marriott Mumbai", "category": "premium", "base_price": 7000, "rating": 4.6, "amenities": ["Pool", "Gym", "Restaurant", "Bar"]},
                {"name": "Novotel Mumbai", "category": "mid-range", "base_price": 4500, "rating": 4.3, "amenities": ["Restaurant", "Gym", "Business Center"]},
                {"name": "Treebo Trend", "category": "budget", "base_price": 2500, "rating": 4.0, "amenities": ["WiFi", "AC", "Breakfast"]},
            ],
            "delhi": [
                {"name": "The Imperial", "category": "luxury", "base_price": 10000, "rating": 4.8, "amenities": ["Pool", "Spa", "Fine Dining", "Heritage Property"]},
                {"name": "ITC Maurya", "category": "luxury", "base_price": 9500, "rating": 4.7, "amenities": ["Multiple Restaurants", "Spa", "Business Center"]},
                {"name": "Radisson Blu", "category": "premium", "base_price": 6000, "rating": 4.5, "amenities": ["Pool", "Restaurant", "Gym"]},
                {"name": "Lemon Tree Premier", "category": "mid-range", "base_price": 3500, "rating": 4.2, "amenities": ["Restaurant", "WiFi", "Room Service"]},
                {"name": "OYO Flagship", "category": "budget", "base_price": 1800, "rating": 3.9, "amenities": ["WiFi", "AC", "TV"]},
            ],
            "bangalore": [
                {"name": "The Leela Palace", "category": "luxury", "base_price": 9000, "rating": 4.8, "amenities": ["Pool", "Spa", "Fine Dining", "Butler Service"]},
                {"name": "Taj West End", "category": "luxury", "base_price": 8500, "rating": 4.7, "amenities": ["Heritage Property", "Garden", "Spa", "Restaurant"]},
                {"name": "Marriott Whitefield", "category": "premium", "base_price": 5500, "rating": 4.5, "amenities": ["Pool", "Gym", "Restaurant", "Business Center"]},
                {"name": "Ramada Bangalore", "category": "mid-range", "base_price": 3200, "rating": 4.1, "amenities": ["Restaurant", "Gym", "WiFi"]},
                {"name": "Zostel Bangalore", "category": "budget", "base_price": 1200, "rating": 4.0, "amenities": ["Hostel", "Common Area", "WiFi"]},
            ],
            "jaipur": [
                {"name": "Rambagh Palace", "category": "luxury", "base_price": 15000, "rating": 4.9, "amenities": ["Palace Hotel", "Pool", "Spa", "Heritage Dining"]},
                {"name": "Fairmont Jaipur", "category": "luxury", "base_price": 10000, "rating": 4.7, "amenities": ["Pool", "Spa", "Multiple Restaurants", "Golf"]},
                {"name": "Hilton Jaipur", "category": "premium", "base_price": 6000, "rating": 4.5, "amenities": ["Pool", "Restaurant", "Rooftop Bar"]},
                {"name": "Hotel Clarks Amer", "category": "mid-range", "base_price": 3500, "rating": 4.2, "amenities": ["Pool", "Restaurant", "Cultural Shows"]},
                {"name": "Moustache Hostel", "category": "budget", "base_price": 1500, "rating": 4.0, "amenities": ["Hostel", "Rooftop", "Common Kitchen"]},
            ],
        }
    
    async def search_hotels(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for hotels based on destination, budget, and preferences
        """
        destination = search_params.get('destination', '').lower()
        budget_per_night = search_params.get('budget_per_night', 5000)
        interests = search_params.get('interests', [])
        check_in = search_params.get('check_in')
        check_out = search_params.get('check_out')
        
        # Get hotels for destination
        hotels = self.hotels_database.get(destination, self.hotels_database.get('goa', []))
        
        # Filter by budget
        filtered_hotels = [h for h in hotels if h['base_price'] <= budget_per_night * 1.2]
        
        # If no hotels in budget, return cheapest options
        if not filtered_hotels:
            filtered_hotels = sorted(hotels, key=lambda x: x['base_price'])[:3]
        
        # Prioritize based on interests
        if 'luxury' in interests or 'relaxation' in interests:
            filtered_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)
        elif 'budget' in interests or 'backpacking' in interests:
            filtered_hotels = sorted(filtered_hotels, key=lambda x: x['base_price'])
        else:
            # Balance of price and rating
            filtered_hotels = sorted(filtered_hotels, key=lambda x: (x['rating'] * 100 - x['base_price']), reverse=True)
        
        # Generate hotel results with mock data
        results = []
        for i, hotel in enumerate(filtered_hotels[:6]):
            # Add some price variation
            price_variation = random.uniform(0.9, 1.1)
            final_price = round(hotel['base_price'] * price_variation)
            
            hotel_result = {
                "hotel_id": f"HTL{random.randint(1000, 9999)}",
                "name": hotel['name'],
                "category": hotel['category'],
                "rating": hotel['rating'],
                "price_per_night": final_price,
                "currency": "INR",
                "location": destination.title(),
                "amenities": hotel['amenities'],
                "images": [f"https://via.placeholder.com/400x300?text={hotel['name'].replace(' ', '+')}"],
                "available_rooms": random.randint(2, 10),
                "check_in": check_in or "14:00",
                "check_out": check_out or "11:00",
                "cancellation_policy": "Free cancellation up to 24 hours before check-in",
                "distance_from_center": f"{random.uniform(0.5, 5.0):.1f} km"
            }
            results.append(hotel_result)
        
        return results
    
    async def get_hotel_details(self, hotel_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific hotel
        """
        return {
            "hotel_id": hotel_id,
            "details": "Hotel details would come from the actual API",
            "rooms": [
                {"type": "Deluxe Room", "price": 4500, "available": 3},
                {"type": "Suite", "price": 7500, "available": 2},
            ],
            "policies": {
                "check_in": "14:00",
                "check_out": "11:00",
                "cancellation": "Free cancellation up to 24 hours"
            }
        }
    
    async def book_hotel(self, hotel_id: str, booking_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Book a hotel (mock implementation)
        """
        return {
            "booking_id": f"HB{random.randint(10000, 99999)}",
            "confirmation_code": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}",
            "status": "confirmed",
            "message": "Hotel booking successful! Confirmation email sent.",
            "hotel_id": hotel_id,
            "check_in": booking_details.get('check_in'),
            "check_out": booking_details.get('check_out'),
            "guest_name": f"{booking_details.get('firstName', '')} {booking_details.get('lastName', '')}",
            "total_amount": booking_details.get('total_amount', 0)
        }