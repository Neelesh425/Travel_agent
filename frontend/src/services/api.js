import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flight search and booking
export const searchFlights = async (searchParams) => {
  try {
    const response = await api.post('/api/search', searchParams);
    return response.data;
  } catch (error) {
    console.error('Error searching flights:', error);
    throw error;
  }
};

export const searchAndBookAutonomous = async (searchParams, passengerDetails) => {
  try {
    const response = await api.post('/api/search-and-book', {
      search_params: searchParams,
      passenger_details: passengerDetails
    });
    return response.data;
  } catch (error) {
    console.error('Error in autonomous booking:', error);
    throw error;
  }
};

export const bookFlight = async (bookingData) => {
  try {
    const response = await api.post('/api/book', bookingData);
    return response.data;
  } catch (error) {
    console.error('Error booking flight:', error);
    throw error;
  }
};

// History - Updated with filters and pagination
export const getSearchHistory = async (params = {}) => {
  try {
    const { limit = 20, offset = 0, destination, origin, status } = params;
    const queryParams = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
    });
    
    if (destination) queryParams.append('destination', destination);
    if (origin) queryParams.append('origin', origin);
    if (status) queryParams.append('status', status);
    
    const response = await api.get(`/api/history?${queryParams.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

// Bookings - New endpoint
export const getBookings = async (params = {}) => {
  try {
    const { limit = 20, offset = 0, status } = params;
    const queryParams = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
    });
    
    if (status) queryParams.append('status', status);
    
    const response = await api.get(`/api/bookings?${queryParams.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching bookings:', error);
    throw error;
  }
};

// Health check
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

// Conversational travel planning
export const chatWithAgent = async (chatRequest) => {
  try {
    const response = await api.post('/api/chat', chatRequest);
    return response.data;
  } catch (error) {
    console.error('Error in chat:', error);
    throw error;
  }
};

export const createTravelPlan = async (planRequest) => {
  try {
    const response = await api.post('/api/plan-travel', planRequest);
    return response.data;
  } catch (error) {
    console.error('Error creating travel plan:', error);
    throw error;
  }
};

export const bookCompletePlan = async (bookingRequest) => {
  try {
    const response = await api.post('/api/book-complete-plan', bookingRequest);
    return response.data;
  } catch (error) {
    console.error('Error booking complete plan:', error);
    throw error;
  }
};

export default api;