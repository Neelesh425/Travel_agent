import ollama
from typing import Dict, Any, List
from app.config import get_settings

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