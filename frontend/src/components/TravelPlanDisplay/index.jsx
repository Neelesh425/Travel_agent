import React, { useState } from 'react';
import HotelCard from '../HotelCard';
import './index.scss';

const TravelPlanDisplay = ({ travelPlan, onBookPlan }) => {
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [passengerDetails, setPassengerDetails] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });

  if (!travelPlan) return null;

  const { 
    destination, 
    origin, 
    departure_date, 
    return_date,
    days, 
    budget, 
    total_cost, 
    remaining_budget,
    flight, 
    hotel, 
    itinerary,
    summary 
  } = travelPlan;

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const handlePassengerChange = (e) => {
    const { name, value } = e.target;
    setPassengerDetails(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleBookingSubmit = (e) => {
    e.preventDefault();
    onBookPlan(passengerDetails);
    setShowBookingModal(false);
  };

  return (
    <div className="travel-plan-display">
      <div className="plan-header">
        <div className="header-content">
          <h2>Your Personalized Travel Plan</h2>
          <p className="summary">{summary}</p>
        </div>
        <div className="plan-stats">
          <div className="stat">
            <span className="label">Destination</span>
            <span className="value">{destination}</span>
          </div>
          <div className="stat">
            <span className="label">Duration</span>
            <span className="value">{days} Days</span>
          </div>
          <div className="stat">
            <span className="label">Total Cost</span>
            <span className="value">₹{total_cost.toLocaleString()}</span>
          </div>
          <div className="stat">
            <span className="label">Budget Remaining</span>
            <span className="value" style={{ color: remaining_budget >= 0 ? '#10b981' : '#ef4444' }}>
              ₹{remaining_budget.toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      {/* Flight Section */}
      <section className="plan-section">
        <h3>
          <span className="section-icon">✈️</span>
          Your Flights
        </h3>
        <div className="flight-details">
          <div className="flight-card-plan">
            <div className="flight-badge">Outbound</div>
            <div className="flight-info-grid">
              <div className="info-item">
                <span className="label">Airline</span>
                <span className="value">{flight.airline} {flight.flight_number}</span>
              </div>
              <div className="info-item">
                <span className="label">Route</span>
                <span className="value">{origin} → {destination}</span>
              </div>
              <div className="info-item">
                <span className="label">Date</span>
                <span className="value">{formatDate(departure_date)}</span>
              </div>
              <div className="info-item">
                <span className="label">Time</span>
                <span className="value">
                  {flight.departure_time?.split('T')[1]?.substring(0, 5)} - {flight.arrival_time?.split('T')[1]?.substring(0, 5)}
                </span>
              </div>
              <div className="info-item">
                <span className="label">Duration</span>
                <span className="value">{flight.duration}</span>
              </div>
              <div className="info-item">
                <span className="label">Price (Round Trip)</span>
                <span className="value">₹{(flight.price * 2).toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Hotel Section */}
      <section className="plan-section">
        <h3>
          <span className="section-icon">🏨</span>
          Your Accommodation
        </h3>
        <div className="hotel-details">
          <HotelCard hotel={hotel} isSelected={true} />
          <div className="hotel-summary">
            <div className="summary-item">
              <span className="label">Check-in:</span>
              <span className="value">{formatDate(departure_date)}</span>
            </div>
            <div className="summary-item">
              <span className="label">Check-out:</span>
              <span className="value">{formatDate(return_date)}</span>
            </div>
            <div className="summary-item">
              <span className="label">Nights:</span>
              <span className="value">{days}</span>
            </div>
            <div className="summary-item total">
              <span className="label">Total Hotel Cost:</span>
              <span className="value">₹{(hotel.price_per_night * days).toLocaleString()}</span>
            </div>
          </div>
        </div>
      </section>

      {/* Itinerary Section */}
      <section className="plan-section">
        <h3>
          <span className="section-icon">📋</span>
          Day-by-Day Itinerary
        </h3>
        <div className="itinerary">
          {itinerary.map((day) => (
            <div key={day.day} className="itinerary-day">
              <div className="day-header">
                <span className="day-number">Day {day.day}</span>
                <span className="day-title">{day.title}</span>
              </div>
              <div className="day-activities">
                <div className="activity">
                  <span className="time-label">Morning</span>
                  <span className="activity-desc">{day.activities.morning}</span>
                </div>
                <div className="activity">
                  <span className="time-label">Afternoon</span>
                  <span className="activity-desc">{day.activities.afternoon}</span>
                </div>
                <div className="activity">
                  <span className="time-label">Evening</span>
                  <span className="activity-desc">{day.activities.evening}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Cost Breakdown */}
      <section className="plan-section cost-breakdown">
        <h3>
          <span className="section-icon">💰</span>
          Cost Breakdown
        </h3>
        <div className="breakdown-table">
          <div className="breakdown-row">
            <span className="item">Round Trip Flights</span>
            <span className="amount">₹{(flight.price * 2).toLocaleString()}</span>
          </div>
          <div className="breakdown-row">
            <span className="item">Hotel ({days} nights)</span>
            <span className="amount">₹{(hotel.price_per_night * days).toLocaleString()}</span>
          </div>
          <div className="breakdown-row total">
            <span className="item">Total</span>
            <span className="amount">₹{total_cost.toLocaleString()}</span>
          </div>
          <div className="breakdown-row remaining">
            <span className="item">Remaining from Budget</span>
            <span className="amount">₹{remaining_budget.toLocaleString()}</span>
          </div>
        </div>
      </section>

      {/* Booking Button */}
      <div className="plan-actions">
        <button 
          className="book-plan-button"
          onClick={() => setShowBookingModal(true)}
        >
          <span>🎉</span>
          Book This Complete Plan
        </button>
      </div>

      {/* Booking Modal */}
      {showBookingModal && (
        <div className="booking-modal">
          <div className="modal-content">
            <button 
              className="close-button"
              onClick={() => setShowBookingModal(false)}
            >
              ×
            </button>
            
            <h3>Complete Your Booking</h3>
            <div className="booking-summary">
              <p><strong>Total Cost:</strong> ₹{total_cost.toLocaleString()}</p>
              <p>Flight + Hotel for {days} days to {destination}</p>
            </div>

            <form onSubmit={handleBookingSubmit}>
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  name="firstName"
                  value={passengerDetails.firstName}
                  onChange={handlePassengerChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  name="lastName"
                  value={passengerDetails.lastName}
                  onChange={handlePassengerChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={passengerDetails.email}
                  onChange={handlePassengerChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={passengerDetails.phone}
                  onChange={handlePassengerChange}
                  required
                />
              </div>

              <button type="submit" className="submit-button">
                Confirm Complete Booking
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TravelPlanDisplay;