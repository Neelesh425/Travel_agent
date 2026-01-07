import React, { useState } from 'react';
import './index.scss';

const SearchForm = ({ onSearch, loading }) => {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    departure_date: '',
    return_date: '',
    passengers: 1,
    trip_type: 'one_way',
    cabin_class: 'economy'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(formData);
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Search Flights</h2>
        <p>Let our AI agent find the best flights for you</p>
      </div>

      <div className="form-group trip-type">
        <label className="radio-label">
          <input
            type="radio"
            name="trip_type"
            value="one_way"
            checked={formData.trip_type === 'one_way'}
            onChange={handleChange}
          />
          <span>One Way</span>
        </label>
        <label className="radio-label">
          <input
            type="radio"
            name="trip_type"
            value="round_trip"
            checked={formData.trip_type === 'round_trip'}
            onChange={handleChange}
          />
          <span>Round Trip</span>
        </label>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="origin">From</label>
          <input
            type="text"
            id="origin"
            name="origin"
            value={formData.origin}
            onChange={handleChange}
            placeholder="e.g., Delhi, DEL"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="destination">To</label>
          <input
            type="text"
            id="destination"
            name="destination"
            value={formData.destination}
            onChange={handleChange}
            placeholder="e.g., Mumbai, BOM"
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="departure_date">Departure Date</label>
          <input
            type="date"
            id="departure_date"
            name="departure_date"
            value={formData.departure_date}
            onChange={handleChange}
            min={today}
            required
          />
        </div>

        {formData.trip_type === 'round_trip' && (
          <div className="form-group">
            <label htmlFor="return_date">Return Date</label>
            <input
              type="date"
              id="return_date"
              name="return_date"
              value={formData.return_date}
              onChange={handleChange}
              min={formData.departure_date || today}
            />
          </div>
        )}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="passengers">Passengers</label>
          <input
            type="number"
            id="passengers"
            name="passengers"
            value={formData.passengers}
            onChange={handleChange}
            min="1"
            max="9"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="cabin_class">Cabin Class</label>
          <select
            id="cabin_class"
            name="cabin_class"
            value={formData.cabin_class}
            onChange={handleChange}
            required
          >
            <option value="economy">Economy</option>
            <option value="premium_economy">Premium Economy</option>
            <option value="business">Business</option>
            <option value="first">First Class</option>
          </select>
        </div>
      </div>

      <button type="submit" className="search-button" disabled={loading}>
        {loading ? (
          <>
            <span className="spinner"></span>
            AI Agent Searching...
          </>
        ) : (
          <>
            <span></span>
            Search with Agent
          </>
        )}
      </button>
    </form>
  );
};

export default SearchForm;