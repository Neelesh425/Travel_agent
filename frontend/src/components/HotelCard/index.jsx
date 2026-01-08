import React from 'react';
import './index.scss';

const HotelCard = ({ hotel, isSelected = false }) => {
  const renderStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    return (
      <div className="stars">
        {[...Array(fullStars)].map((_, i) => (
          <span key={i} className="star full">★</span>
        ))}
        {hasHalfStar && <span className="star half">★</span>}
        <span className="rating-number">({rating})</span>
      </div>
    );
  };

  return (
    <div className={`hotel-card ${isSelected ? 'selected' : ''}`}>
      {isSelected && (
        <div className="selected-badge">
          <span>✓ Selected by AI</span>
        </div>
      )}
      
      <div className="hotel-image">
        <img 
          src={hotel.images?.[0] || `https://via.placeholder.com/400x300?text=${hotel.name.replace(' ', '+')}`}
          alt={hotel.name}
        />
        <div className="category-badge">{hotel.category}</div>
      </div>

      <div className="hotel-info">
        <div className="hotel-header">
          <h4>{hotel.name}</h4>
          {renderStars(hotel.rating)}
        </div>

        <div className="hotel-location">
          <span className="location-icon">📍</span>
          <span>{hotel.location}</span>
          {hotel.distance_from_center && (
            <span className="distance"> • {hotel.distance_from_center} from center</span>
          )}
        </div>

        <div className="amenities">
          {hotel.amenities.slice(0, 4).map((amenity, index) => (
            <span key={index} className="amenity-tag">
              {amenity}
            </span>
          ))}
          {hotel.amenities.length > 4 && (
            <span className="amenity-tag more">
              +{hotel.amenities.length - 4} more
            </span>
          )}
        </div>

        <div className="hotel-footer">
          <div className="availability">
            <span className="rooms-left">
              {hotel.available_rooms} rooms left
            </span>
          </div>
          <div className="price-section">
            <div className="price">
              <span className="currency">{hotel.currency}</span>
              <span className="amount">{hotel.price_per_night?.toLocaleString() || 0}</span>
              <span className="per-night">/night</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HotelCard;