import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './index.scss';

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Travel MadeEasy</h2>
        <p className="subtitle">AI-Powered Booking</p>
      </div>

      <nav className="sidebar-nav">
        <Link 
          to="/" 
          className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}
        >
          <span className="icon">🤖</span>
          <span className="label">AI Travel Planner</span>
        </Link>

        <Link 
          to="/search" 
          className={`nav-item ${location.pathname === '/search' ? 'active' : ''}`}
        >
          <span className="icon">🔍</span>
          <span className="label">Search Flights</span>
        </Link>

        <Link 
          to="/history" 
          className={`nav-item ${location.pathname === '/history' ? 'active' : ''}`}
        >
          <span className="icon">📜</span>
          <span className="label">Search History</span>
        </Link>
      </nav>

      <div className="sidebar-footer">
        <div className="ai-status">
          <div className="status-indicator active"></div>
          <span>AI Agent Active</span>
        </div>
        <p className="footer-text">Made by Shunya</p>
      </div>
    </div>
  );
};

export default Sidebar;