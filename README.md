# TripScout - AI Travel Planner Agent

An autonomous AI-powered travel planning system that creates personalized end-to-end trip itineraries based on user preferences, budget, and interests. The agent autonomously searches, compares, and books flights and hotels while optimizing for cost and user experience.

## Features

- **Intelligent Trip Planning**: Input your budget, travel dates, interests (historical sites, beaches, adventure, etc.), and duration to get a complete itinerary
- **Autonomous Booking**: AI agent automatically searches and compares flight and hotel options, selecting the best match for your preferences
- **Multi-Step Reasoning**: Uses Llama 3.2 via Ollama to chain decisions, handle edge cases, and optimize travel plans
- **Personalized Recommendations**: Tailors itineraries based on user interests like historical places, nature, food, culture, etc.
- **Real-Time Updates**: React frontend displays itinerary generation and booking status in real-time

## Tech Stack

**Frontend:**
- React
- SCSS
- Vite

**Backend:**
- FastAPI
- MongoDB
- Ollama (Llama 3.2)

**AI/LLM:**
- Llama 3.2 for reasoning and decision-making
- Custom agent workflow for multi-step planning

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)
- [Ollama](https://ollama.ai/) installed locally
- Llama 3.2 model pulled in Ollama

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/tripscout.git
cd tripscout
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
# API Configuration
FLIGHT_API_KEY=your_flight_api_key_here
FLIGHT_API_URL=https://api.example.com/flights

# LLM Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest

# Server Configuration
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

### 4. Pull Llama 3.2 Model
```bash
ollama pull llama3.2:latest
```

## Running the Application

### 1. Start Ollama
```bash
ollama serve
```

### 2. Start MongoDB
Make sure MongoDB is running locally or update your connection string in the backend configuration.

### 3. Start Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Start Frontend
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## Usage

1. Open the application in your browser
2. Enter your travel preferences:
   - Destination
   - Budget
   - Travel dates
   - Trip duration (number of days)
   - Interests (historical places, beaches, adventure, etc.)
   - Any additional preferences
3. The AI agent will:
   - Generate a personalized itinerary
   - Search for flights and hotels
   - Compare options based on your budget and preferences
   - Automatically book the best available options
4. View your complete trip plan with bookings

## Project Structure
```
tripscout/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
```

## Note

This project uses simulated flight and hotel APIs for demonstration purposes. In a production environment, you would integrate real travel APIs like Amadeus, Skyscanner, or Booking.com.

## Future Enhancements

- [ ] Integration with real flight and hotel booking APIs
- [ ] Multi-city trip support
- [ ] Activity and restaurant recommendations
- [ ] Price tracking and alerts
- [ ] Export itinerary to PDF
- [ ] User authentication and trip history


## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
