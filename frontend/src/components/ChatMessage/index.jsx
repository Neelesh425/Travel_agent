import React from 'react';
import './index.scss';

const ChatMessage = ({ role, content, timestamp, isTyping = false }) => {
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`chat-message ${role}`}>
      <div className="message-avatar">
        {role === 'ai' ? '🤖' : '👤'}
      </div>
      <div className="message-content-wrapper">
        <div className="message-bubble">
          {isTyping ? (
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          ) : (
            <p className="message-text">{content}</p>
          )}
        </div>
        {timestamp && !isTyping && (
          <span className="message-time">{formatTime(timestamp)}</span>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;