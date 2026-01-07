import React, { useState } from 'react';
import SearchForm from '../../components/SearchForm';
import AgentThinking from '../../components/AgentThinking';
import ResultsDisplay from '../../components/ResultsDisplay';
import { searchFlights, bookFlight } from '../../services/api';
import './index.scss';

const SearchPage = () => {
  const [loading, setLoading] = useState(false);
  const [searchResponse, setSearchResponse] = useState(null);
  const [bookingStatus, setBookingStatus] = useState(null);

  const handleSearch = async (searchParams) => {
    setLoading(true);
    setSearchResponse(null);
    setBookingStatus(null);

    try {
      const response = await searchFlights(searchParams);
      setSearchResponse(response);
    } catch (error) {
      console.error('Search error:', error);
      alert('Error searching flights. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async (bookingData) => {
    try {
      const response = await bookFlight(bookingData);
      setBookingStatus(response);
      alert(`Booking successful! Confirmation code: ${response.confirmation_code}`);
    } catch (error) {
      console.error('Booking error:', error);
      alert('Error booking flight. Please try again.');
    }
  };

  return (
    <div className="search-page">
      <div className="page-header">
        <h1>Find Your Perfect Flight</h1>
        <p>Our AI agent will search and analyze the best options for you</p>
      </div>

      <SearchForm onSearch={handleSearch} loading={loading} />

      {(loading || searchResponse) && (
        <AgentThinking 
          thoughts={searchResponse?.thoughts || []} 
          isProcessing={loading} 
        />
      )}

      {searchResponse && !loading && (
        <ResultsDisplay 
          searchResponse={searchResponse} 
          onBook={handleBook} 
        />
      )}

      {bookingStatus && (
        <div className="booking-success">
          <div className="success-icon">✅</div>
          <h3>Booking Confirmed!</h3>
          <p>Confirmation Code: <strong>{bookingStatus.confirmation_code}</strong></p>
          <p>{bookingStatus.message}</p>
        </div>
      )}
    </div>
  );
};

export default SearchPage;