import React, { useState, useEffect } from 'react';
import { getSearchHistory, getBookings } from '../../services/api';
import './index.scss';

const HistoryPage = () => {
  const [activeTab, setActiveTab] = useState('searches'); // 'searches' or 'bookings'
  const [searches, setSearches] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    destination: '',
    origin: '',
    status: ''
  });
  const [pagination, setPagination] = useState({
    limit: 20,
    offset: 0,
    total: 0
  });

  useEffect(() => {
    loadData();
  }, [activeTab, filters, pagination.offset]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'searches') {
        const response = await getSearchHistory({
          limit: pagination.limit,
          offset: pagination.offset,
          ...filters
        });
        setSearches(response.items || []);
        setPagination(prev => ({ ...prev, total: response.total || 0 }));
      } else {
        const response = await getBookings({
          limit: pagination.limit,
          offset: pagination.offset,
          status: filters.status
        });
        setBookings(response.items || []);
        setPagination(prev => ({ ...prev, total: response.total || 0 }));
      }
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    setPagination(prev => ({ ...prev, offset: 0 })); // Reset to first page
  };

  const handleClearFilters = () => {
    setFilters({ destination: '', origin: '', status: '' });
  };

  const handlePageChange = (direction) => {
    setPagination(prev => ({
      ...prev,
      offset: direction === 'next' 
        ? prev.offset + prev.limit 
        : Math.max(0, prev.offset - prev.limit)
    }));
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadgeClass = (status) => {
    switch(status) {
      case 'confirmed': return 'badge-success';
      case 'cancelled': return 'badge-danger';
      case 'pending': return 'badge-warning';
      default: return 'badge-default';
    }
  };

  const renderSearchHistory = () => {
    if (searches.length === 0) {
      return (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h3>No Search History</h3>
          <p>Your flight searches will appear here</p>
        </div>
      );
    }

    return (
      <div className="history-list">
        {searches.map((search) => (
          <div key={search.search_id} className="history-card">
            <div className="history-header">
              <div className="route-info">
                <h3>{search.origin} → {search.destination}</h3>
                <span className="search-id">Search ID: {search.search_id}</span>
              </div>
              <div className="search-stats">
                <span className="result-count">{search.result_count} flights found</span>
                <span className={`status-badge ${search.search_status === 'success' ? 'badge-success' : 'badge-danger'}`}>
                  {search.search_status}
                </span>
              </div>
            </div>

            <div className="history-details">
              <div className="detail-item">
                <span className="label">Departure:</span>
                <span className="value">{formatDate(search.departure_date)}</span>
              </div>
              {search.return_date && (
                <div className="detail-item">
                  <span className="label">Return:</span>
                  <span className="value">{formatDate(search.return_date)}</span>
                </div>
              )}
              <div className="detail-item">
                <span className="label">Passengers:</span>
                <span className="value">{search.passengers}</span>
              </div>
              <div className="detail-item">
                <span className="label">Class:</span>
                <span className="value">{search.cabin_class}</span>
              </div>
              <div className="detail-item">
                <span className="label">Searched:</span>
                <span className="value">{formatDate(search.created_at)}</span>
              </div>
            </div>

            {search.bookings && search.bookings.length > 0 && (
              <div className="related-bookings">
                <h4>Related Bookings:</h4>
                {search.bookings.map((booking) => (
                  <div key={booking.booking_id} className="booking-chip">
                    <span className="confirmation-code">{booking.confirmation_code}</span>
                    <span className={`status-badge ${getStatusBadgeClass(booking.status)}`}>
                      {booking.status}
                    </span>
                    <span className="amount">₹{booking.total_amount?.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderBookings = () => {
    if (bookings.length === 0) {
      return (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No Bookings Yet</h3>
          <p>Your flight and hotel bookings will appear here</p>
        </div>
      );
    }

    return (
      <div className="history-list">
        {bookings.map((booking) => (
          <div key={booking.booking_id} className="history-card booking-card">
            <div className="history-header">
              <div className="booking-info">
                <h3>Booking #{booking.booking_id}</h3>
                <span className="booking-type">{booking.booking_type.replace('_', ' ')}</span>
              </div>
              <div className={`status-badge large ${getStatusBadgeClass(booking.status)}`}>
                {booking.status}
              </div>
            </div>

            <div className="history-details">
              <div className="detail-item">
                <span className="label">Passenger:</span>
                <span className="value">{booking.passenger_name}</span>
              </div>
              <div className="detail-item">
                <span className="label">Email:</span>
                <span className="value">{booking.passenger_email}</span>
              </div>
              <div className="detail-item">
                <span className="label">Confirmation:</span>
                <span className="value confirmation-code">{booking.confirmation_code}</span>
              </div>
              <div className="detail-item">
                <span className="label">Total Amount:</span>
                <span className="value amount">{booking.currency} {booking.total_amount?.toLocaleString()}</span>
              </div>
              <div className="detail-item">
                <span className="label">Booked:</span>
                <span className="value">{formatDate(booking.created_at)}</span>
              </div>
            </div>

            {booking.flight_details && (
              <div className="booking-details-section">
                <h4>✈️ Flight Details</h4>
                <div className="details-grid">
                  <span><strong>Airline:</strong> {booking.flight_details.airline}</span>
                  <span><strong>Flight:</strong> {booking.flight_details.flight_number}</span>
                  <span><strong>Route:</strong> {booking.flight_details.origin} → {booking.flight_details.destination}</span>
                  <span><strong>Duration:</strong> {booking.flight_details.duration}</span>
                </div>
              </div>
            )}

            {booking.hotel_details && (
              <div className="booking-details-section">
                <h4>🏨 Hotel Details</h4>
                <div className="details-grid">
                  <span><strong>Hotel:</strong> {booking.hotel_details.name}</span>
                  <span><strong>Location:</strong> {booking.hotel_details.location}</span>
                  <span><strong>Rating:</strong> {booking.hotel_details.rating} ⭐</span>
                  <span><strong>Per Night:</strong> {booking.hotel_details.currency} {booking.hotel_details.price_per_night}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  const totalPages = Math.ceil(pagination.total / pagination.limit);
  const currentPage = Math.floor(pagination.offset / pagination.limit) + 1;

  return (
    <div className="history-page">
      <div className="page-header">
        <h1>History & Bookings</h1>
        <p>View your search history and manage bookings</p>
      </div>

      <div className="tabs-container">
        <button 
          className={`tab ${activeTab === 'searches' ? 'active' : ''}`}
          onClick={() => setActiveTab('searches')}
        >
          <span className="icon">🔍</span>
          Search History
          {pagination.total > 0 && activeTab === 'searches' && (
            <span className="count">{pagination.total}</span>
          )}
        </button>
        <button 
          className={`tab ${activeTab === 'bookings' ? 'active' : ''}`}
          onClick={() => setActiveTab('bookings')}
        >
          <span className="icon">📋</span>
          Bookings
          {pagination.total > 0 && activeTab === 'bookings' && (
            <span className="count">{pagination.total}</span>
          )}
        </button>
      </div>

      <div className="filters-container">
        <div className="filters">
          {activeTab === 'searches' && (
            <>
              <input
                type="text"
                name="origin"
                placeholder="Filter by origin..."
                value={filters.origin}
                onChange={handleFilterChange}
                className="filter-input"
              />
              <input
                type="text"
                name="destination"
                placeholder="Filter by destination..."
                value={filters.destination}
                onChange={handleFilterChange}
                className="filter-input"
              />
            </>
          )}
          
          <select
            name="status"
            value={filters.status}
            onChange={handleFilterChange}
            className="filter-select"
          >
            <option value="">All Status</option>
            <option value="success">Success</option>
            {activeTab === 'bookings' && (
              <>
                <option value="confirmed">Confirmed</option>
                <option value="cancelled">Cancelled</option>
                <option value="pending">Pending</option>
              </>
            )}
          </select>

          <button onClick={handleClearFilters} className="clear-filters-btn">
            Clear Filters
          </button>
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading history...</p>
        </div>
      ) : (
        <>
          {activeTab === 'searches' ? renderSearchHistory() : renderBookings()}

          {pagination.total > pagination.limit && (
            <div className="pagination">
              <button 
                onClick={() => handlePageChange('prev')}
                disabled={pagination.offset === 0}
                className="pagination-btn"
              >
                ← Previous
              </button>
              <span className="pagination-info">
                Page {currentPage} of {totalPages} ({pagination.total} total)
              </span>
              <button 
                onClick={() => handlePageChange('next')}
                disabled={pagination.offset + pagination.limit >= pagination.total}
                className="pagination-btn"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HistoryPage;