import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchFlights = async (searchParams) => {
  try {
    const response = await api.post('/api/search', searchParams);
    return response.data;
  } catch (error) {
    console.error('Error searching flights:', error);
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

export const getSearchHistory = async () => {
  try {
    const response = await api.get('/api/history');
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default api;