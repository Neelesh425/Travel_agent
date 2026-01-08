import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from '../ChatMessage';
import './index.scss';

const ChatInterface = ({ messages, onSendMessage, isLoading, onGeneratePlan }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleGeneratePlan = () => {
    if (onGeneratePlan) {
      onGeneratePlan();
    }
  };

  // Check if last message indicates ready to plan
  const isReadyToPlan = messages.length > 0 && 
    messages[messages.length - 1]?.role === 'ai' &&
    messages[messages.length - 1]?.content?.toLowerCase().includes('create');

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-content">
          <span className="robot-icon">🤖</span>
          <div className="header-text">
            <h3>AI Travel Assistant</h3>
            <p className="status">
              {isLoading ? 'Thinking...' : 'Online'}
            </p>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-icon">✈️</div>
            <h2>Plan Your Perfect Trip!</h2>
            <p>I'm your AI travel assistant. Tell me where you'd like to go and I'll help you plan everything!</p>
            <div className="suggestion-chips">
              <button 
                className="chip"
                onClick={() => onSendMessage("I want to plan a beach vacation")}
              >
                🏖️ Beach Vacation
              </button>
              <button 
                className="chip"
                onClick={() => onSendMessage("I want to go on a mountain trip")}
              >
                🏔️ Mountain Adventure
              </button>
              <button 
                className="chip"
                onClick={() => onSendMessage("Looking for a cultural experience")}
              >
                🎭 Cultural Tour
              </button>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            role={message.role}
            content={message.content}
            timestamp={message.timestamp}
          />
        ))}

        {isLoading && (
          <ChatMessage
            role="ai"
            content="..."
            isTyping={true}
          />
        )}

        {isReadyToPlan && !isLoading && (
          <div className="generate-plan-prompt">
            <button 
              className="generate-plan-button"
              onClick={handleGeneratePlan}
            >
              <span className="icon">✨</span>
              Generate My Travel Plan
            </button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
        >
          {isLoading ? (
            <span className="spinner-small"></span>
          ) : (
            <span>➤</span>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;