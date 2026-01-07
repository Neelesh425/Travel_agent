import React, { useState } from 'react';
import './index.scss';

const ResultsDisplay = ({ searchResponse, onBook }) => {
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [showBookingForm, setShowBookingForm] = useState(false);
  const [passengerDetails, setPassengerDetails] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });

  if (!searchResponse || searchResponse.flights.length === 0) {
    return null;
  }

  const handleSelectFlight = (flight) => {
    setSelectedFlight(flight);
    setShowBookingForm(true);
  };

  const handleBookingSubmit = (e) => {
    e.preventDefault();
    onBook({
      flight_id: selectedFlight.flight_id,
      passenger_details: passengerDetails
    });
    setShowBookingForm(false);
    setSelectedFlight(null);
    setPassengerDetails({ firstName: '', lastName: '', email: '', phone: '' });
  };

  const formatDuration = (duration) => {
    return duration;
  };

  const getStopsText = (stops) => {
    if (stops === 0) return 'Non-stop';
    if (stops === 1) return '1 Stop';
    return `${stops} Stops`;
  };

  return (
    <div className="results-display">
      <div className="results-header">
        <h3>Available Flights</h3>
        <p className="summary">{searchResponse.message}</p>
        <div className="results-count">
          Found {searchResponse.flights.length} flights
        </div>
      </div>

      <div className="flights-list">
        {searchResponse.flights.map((flight, index) => (
          <div key={flight.flight_id} className="flight-card">
            <div className="flight-rank">#{index + 1}</div>
            
            <div className="flight-info">
              <div className="airline-section">
                <h4>{flight.airline}</h4>
                <span className="flight-number">{flight.flight_number}</span>
              </div>

              <div className="route-section">
                <div className="time-location">
                  <div className="time">{flight.departure_time.split('T')[1].substring(0, 5)}</div>
                  <div className="location">{flight.origin}</div>
                </div>

                <div className="flight-path">
                  <div className="duration">{formatDuration(flight.duration)}</div>
                  <div className="path-line">
                    <div className="line"></div>
                    <div className="plane-icon">✈️</div>
                  </div>
                  <div className="stops">{getStopsText(flight.stops)}</div>
                </div>

                <div className="time-location">
                  <div className="time">{flight.arrival_time.split('T')[1].substring(0, 5)}</div>
                  <div className="location">{flight.destination}</div>
                </div>
              </div>

              <div className="details-section">
                <span className="cabin-class">{flight.cabin_class}</span>
              </div>
            </div>

            <div className="price-section">
              <div className="price">
                <span className="currency">{flight.currency}</span>
                <span className="amount">{flight.price.toLocaleString()}</span>
              </div>
              <button 
                className="book-button"
                onClick={() => handleSelectFlight(flight)}
              >
                Book Now
              </button>
            </div>
          </div>
        ))}
      </div>

      {showBookingForm && selectedFlight && (
        <div className="booking-modal">
          <div className="modal-content">
            <button 
              className="close-button"
              onClick={() => setShowBookingForm(false)}
            >
              ×
            </button>
            
            <h3>Complete Your Booking</h3>
            <div className="selected-flight-summary">
              <p><strong>{selectedFlight.airline}</strong> - {selectedFlight.flight_number}</p>
              <p>{selectedFlight.origin} → {selectedFlight.destination}</p>
              <p className="price">{selectedFlight.currency} {selectedFlight.price.toLocaleString()}</p>
            </div>

            <form onSubmit={handleBookingSubmit}>
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  value={passengerDetails.firstName}
                  onChange={(e) => setPassengerDetails({...passengerDetails, firstName: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  value={passengerDetails.lastName}
                  onChange={(e) => setPassengerDetails({...passengerDetails, lastName: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={passengerDetails.email}
                  onChange={(e) => setPassengerDetails({...passengerDetails, email: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  value={passengerDetails.phone}
                  onChange={(e) => setPassengerDetails({...passengerDetails, phone: e.target.value})}
                  required
                />
              </div>

              <button type="submit" className="submit-button">
                Confirm Booking
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;