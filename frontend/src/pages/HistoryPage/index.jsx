import React, { useState, useEffect } from 'react';
import { getSearchHistory } from '../../services/api';
import './index.scss';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getSearchHistory();
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  if (loading) {
    return (
      <div className="history-page">
        <div className="loading">Loading history...</div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="page-header">
        <h1>Search History</h1>
        <p>Your recent flight searches</p>
      </div>

      {history.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📭</div>
          <h3>No search history yet</h3>
          <p>Start searching for flights to see your history here</p>
        </div>
      ) : (
        <div className="history-list">
          {history.reverse().map((item, index) => (
            <div key={item.search_id} className="history-item">
              <div className="item-number">#{history.length - index}</div>
              <div className="item-content">
                <div className="route">
                  <span className="origin">{item.search_params.origin}</span>
                  <span className="arrow">→</span>
                  <span className="destination">{item.search_params.destination}</span>
                </div>
                <div className="details">
                  <span className="date">
                    📅 {item.search_params.departure_date}
                  </span>
                  <span className="passengers">
                    👤 {item.search_params.passengers} passenger(s)
                  </span>
                  <span className="class">
                    💺 {item.search_params.cabin_class}
                  </span>
                </div>
                <div className="meta">
                  <span className="timestamp">{formatDate(item.timestamp)}</span>
                  <span className="results">{item.result_count} flights found</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;