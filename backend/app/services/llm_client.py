import ollama
from typing import Dict, Any, List
from app.config import get_settings
import json
import re

settings = get_settings()

class LLMClient:
    def __init__(self):
        self.model = settings.ollama_model
        self.host = settings.ollama_host
    
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from the LLM
        """
        try:
            messages = context or []
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return f"Error: {str(e)}"
    
    async def analyze_search_intent(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the user's search intent and determine the best approach
        """
        prompt = f"""
        Analyze this flight search request and provide insights:
        
        Origin: {search_params.get('origin')}
        Destination: {search_params.get('destination')}
        Departure Date: {search_params.get('departure_date')}
        Return Date: {search_params.get('return_date', 'N/A')}
        Passengers: {search_params.get('passengers')}
        Trip Type: {search_params.get('trip_type')}
        Cabin Class: {search_params.get('cabin_class')}
        
        Provide a brief analysis in 2-3 sentences about:
        1. The search parameters
        2. What to look for in the results
        
        Keep it concise and helpful.
        """
        
        response = await self.generate_response(prompt)
        
        return {
            "analysis": response,
            "search_strategy": "price_focused" if search_params.get('cabin_class') == 'economy' else "comfort_focused"
        }
    
    async def select_best_flight(self, flights: List[Dict[str, Any]], search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use AI to select the best flight from available options
        """
        # Prepare flight summary for LLM
        flight_summaries = []
        for i, flight in enumerate(flights[:10]):  # Limit to top 10 to avoid token limits
            flight_summaries.append(
                f"Flight {i+1}: {flight['airline']} {flight['flight_number']} - "
                f"Price: {flight['currency']} {flight['price']}, "
                f"Duration: {flight['duration']}, "
                f"Stops: {flight['stops']}, "
                f"Departure: {flight['departure_time'].split('T')[1][:5]}, "
                f"ID: {flight['flight_id']}"
            )
        
        cabin_class = search_params.get('cabin_class', 'economy')
        
        prompt = f"""
        You are a travel booking AI agent. Select the BEST flight from these options for the user.
        
        User preferences:
        - Cabin Class: {cabin_class}
        - Passengers: {search_params.get('passengers', 1)}
        
        Available flights:
        {chr(10).join(flight_summaries)}
        
        Selection criteria priority:
        1. For economy class: Best value (balance of price and convenience)
        2. For business/first: Comfort and convenience over price
        3. Prefer non-stop or fewer stops
        4. Prefer reasonable departure times
        
        Respond ONLY in this exact format:
        FLIGHT_ID: [the flight_id]
        REASON: [one sentence explaining why this is the best choice]
        
        Example:
        FLIGHT_ID: FL1234
        REASON: Best value with non-stop service at a competitive price.
        """
        
        response = await self.generate_response(prompt)
        
        # Parse the response
        flight_id_match = re.search(r'FLIGHT_ID:\s*(\S+)', response)
        reason_match = re.search(r'REASON:\s*(.+?)(?:\n|$)', response, re.DOTALL)
        
        if flight_id_match:
            flight_id = flight_id_match.group(1).strip()
            reason = reason_match.group(1).strip() if reason_match else "Selected as the best overall option"
        else:
            # Fallback: select the first flight (best price since they're sorted)
            flight_id = flights[0]['flight_id']
            reason = "Selected based on best price and value"
        
        return {
            "flight_id": flight_id,
            "reason": reason
        }
    
    async def make_decision(self, situation: str, options: List[str]) -> str:
        """
        Make a decision based on the given situation and options
        """
        prompt = f"""
        Situation: {situation}
        
        Available options:
        {chr(10).join(f"{i+1}. {opt}" for i, opt in enumerate(options))}
        
        Choose the best option and explain why in one sentence.
        Format: "Option X because [reason]"
        """
        
        response = await self.generate_response(prompt)
        return response
    
    async def generate_search_summary(self, flights: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of the search results
        """
        if not flights:
            return "No flights found matching your criteria."
        
        prompt = f"""
        Summarize these flight search results in 2-3 sentences:
        
        Total flights found: {len(flights)}
        Price range: ${min(f.get('price', 0) for f in flights)} - ${max(f.get('price', 0) for f in flights)}
        Airlines: {', '.join(set(f.get('airline', 'Unknown') for f in flights[:5]))}
        
        Provide a helpful summary for the user.
        """
        
        response = await self.generate_response(prompt)
        return response
    
    # New methods for conversational travel planning
    
    async def extract_travel_info(self, user_message: str, current_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract travel information from user message
        """
        prompt = f"""
        Extract travel information from this user message. Current information we have:
        {json.dumps(current_info, indent=2)}
        
        User message: "{user_message}"
        
        Extract and respond ONLY with a JSON object containing any of these fields that you can identify:
        {{
            "destination": "city name or null",
            "origin": "city name or null",
            "budget": number or null,
            "days": number or null,
            "interests": ["interest1", "interest2"] or [],
            "departure_date": "YYYY-MM-DD or null",
            "passengers": number or null
        }}
        
        Rules:
        - Only include fields that are mentioned in the message
        - For budget, extract numeric values (convert "50k" to 50000, "1 lakh" to 100000)
        - For interests, look for keywords like: relaxation, adventure, food, culture, luxury, budget, beach, mountains, etc.
        - For days, extract numbers like "3 days", "a week" (7 days)
        - Return valid JSON only, no explanation
        """
        
        response = await self.generate_response(prompt)
        
        try:
            # Clean the response
            cleaned = response.strip()
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            extracted = json.loads(cleaned)
            
            # Merge with current info
            result = {**current_info}
            for key, value in extracted.items():
                if value is not None and value != [] and value != "":
                    if key == 'interests' and isinstance(value, list):
                        # Append interests instead of replacing
                        result[key] = list(set(result.get(key, []) + value))
                    else:
                        result[key] = value
            
            return result
        except Exception as e:
            print(f"Error parsing LLM extraction: {e}, Response: {response}")
            return current_info
    
    async def generate_next_question(self, extracted_info: Dict[str, Any]) -> str:
        """
        Generate the next question to ask based on what information is missing
        """
        missing_fields = []
        if not extracted_info.get('destination'):
            missing_fields.append('destination')
        if not extracted_info.get('budget'):
            missing_fields.append('budget')
        if not extracted_info.get('days'):
            missing_fields.append('days')
        if not extracted_info.get('interests'):
            missing_fields.append('interests')
        
        if not missing_fields:
            return "Great! I have all the information. Let me create your travel plan!"
        
        prompt = f"""
        You are a friendly travel planning AI assistant. Generate a natural follow-up question.
        
        Information we have:
        {json.dumps(extracted_info, indent=2)}
        
        Missing information: {', '.join(missing_fields)}
        
        Generate ONE friendly question to ask next. Priority order:
        1. destination (if missing)
        2. budget (if missing)
        3. days (if missing)
        4. interests (if missing)
        
        Keep it conversational and friendly. Don't ask for all missing info at once.
        Response should be 1-2 sentences maximum.
        """
        
        response = await self.generate_response(prompt)
        return response.strip()
    
    async def generate_travel_plan_summary(self, plan_details: Dict[str, Any]) -> str:
        """
        Generate a friendly summary of the travel plan
        """
        prompt = f"""
        Create a brief, exciting summary (2-3 sentences) of this travel plan:
        
        Destination: {plan_details['destination']}
        Duration: {plan_details['days']} days
        Budget: ₹{plan_details['budget']}
        Total Cost: ₹{plan_details['total_cost']}
        Flight: {plan_details['flight'].get('airline', '')} {plan_details['flight'].get('flight_number', '')}
        Hotel: {plan_details['hotel'].get('name', '')} ({plan_details['hotel'].get('rating', 0)}★)
        Interests: {', '.join(plan_details.get('interests', []))}
        
        Make it enthusiastic and highlight key features!
        """
        
        response = await self.generate_response(prompt)
        return response.strip()