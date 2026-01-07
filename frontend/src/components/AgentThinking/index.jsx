import React, { useEffect, useState } from 'react';
import './index.scss';

const AgentThinking = ({ thoughts, isProcessing }) => {
  const [visibleThoughts, setVisibleThoughts] = useState([]);

  useEffect(() => {
    if (thoughts && thoughts.length > 0) {
      setVisibleThoughts([]);
      thoughts.forEach((thought, index) => {
        setTimeout(() => {
          setVisibleThoughts(prev => [...prev, thought]);
        }, index * 500);
      });
    }
  }, [thoughts]);

  if (!isProcessing && visibleThoughts.length === 0) {
    return null;
  }

  return (
    <div className="agent-thinking">
      <div className="thinking-header">
        <div className="brain-icon">🧠</div>
        <h3>AI Agent Thinking Process</h3>
        {isProcessing && <div className="processing-indicator">Processing...</div>}
      </div>

      <div className="thoughts-container">
        {visibleThoughts.map((thought, index) => (
          <div 
            key={index} 
            className="thought-item"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="thought-step">Step {thought.step}</div>
            <div className="thought-content">
              <div className="thought-action">
                <span className="action-badge">{thought.action}</span>
              </div>
              <p className="thought-text">{thought.thought}</p>
              <span className="thought-time">
                {new Date(thought.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {isProcessing && (
          <div className="thought-item processing">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Thinking...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentThinking;