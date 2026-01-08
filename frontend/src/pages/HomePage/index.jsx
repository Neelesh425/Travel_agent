import React, { useState } from 'react';
import ChatInterface from '../../components/ChatInterface';
import TravelPlanDisplay from '../../components/TravelPlanDisplay';
import { chatWithAgent, createTravelPlan, bookCompletePlan } from '../../services/api';
import './index.scss';

const HomePage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      content: 'Hi! I\'m your AI travel assistant. 👋 Tell me where you\'d like to travel and I\'ll help you plan the perfect trip!',
      timestamp: new Date().toISOString()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [extractedInfo, setExtractedInfo] = useState({});
  const [isReadyToPlan, setIsReadyToPlan] = useState(false);
  const [travelPlan, setTravelPlan] = useState(null);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);

  const handleSendMessage = async (userMessage) => {
    // Add user message to chat
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await chatWithAgent({
        message: userMessage,
        conversation_history: messages,
        extracted_info: extractedInfo
      });

      // Add AI response to chat
      const aiMessage = {
        role: 'ai',
        content: response.message,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
      setExtractedInfo(response.extracted_info);
      setIsReadyToPlan(response.is_ready_to_plan);

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'ai',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneratePlan = async () => {
    setIsGeneratingPlan(true);

    try {
      const planRequest = {
        destination: extractedInfo.destination,
        origin: extractedInfo.origin || 'Delhi',
        budget: extractedInfo.budget,
        days: extractedInfo.days,
        interests: extractedInfo.interests || [],
        departure_date: extractedInfo.departure_date,
        passengers: extractedInfo.passengers || 1
      };

      const plan = await createTravelPlan(planRequest);
      setTravelPlan(plan);

      // Add success message
      const successMessage = {
        role: 'ai',
        content: '🎉 Your personalized travel plan is ready! Scroll down to see all the details.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, successMessage]);

    } catch (error) {
      console.error('Plan generation error:', error);
      const errorMessage = {
        role: 'ai',
        content: 'Sorry, I couldn\'t generate your travel plan. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsGeneratingPlan(false);
    }
  };

  const handleBookPlan = async (passengerDetails) => {
    try {
      const response = await bookCompletePlan({
        plan: travelPlan,
        passenger_details: passengerDetails
      });

      alert(
        `🎉 Booking Successful!\n\n` +
        `Flight Confirmation: ${response.flight_booking.confirmation_code}\n` +
        `Hotel Confirmation: ${response.hotel_booking.confirmation_code}\n\n` +
        `Total Cost: ₹${response.total_cost.toLocaleString()}\n\n` +
        `Check your email for details!`
      );

      // Add success message to chat
      const successMessage = {
        role: 'ai',
        content: `Perfect! Your complete travel plan has been booked successfully! 🎊\n\nConfirmation codes:\n- Flight: ${response.flight_booking.confirmation_code}\n- Hotel: ${response.hotel_booking.confirmation_code}\n\nYou'll receive confirmation emails shortly. Have an amazing trip!`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, successMessage]);

    } catch (error) {
      console.error('Booking error:', error);
      alert('Error booking your travel plan. Please try again.');
    }
  };

  const handleStartNewConversation = () => {
    setMessages([
      {
        role: 'ai',
        content: 'Hi! I\'m your AI travel assistant. 👋 Tell me where you\'d like to travel and I\'ll help you plan the perfect trip!',
        timestamp: new Date().toISOString()
      }
    ]);
    setExtractedInfo({});
    setIsReadyToPlan(false);
    setTravelPlan(null);
  };

  return (
    <div className="home-page">
      <div className="page-hero">
        <h1>AI-Powered Travel Planning</h1>
        <p>Chat with our AI assistant to create your perfect travel plan</p>
      </div>

      <div className="home-content">
        <div className="chat-section">
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading || isGeneratingPlan}
            onGeneratePlan={isReadyToPlan ? handleGeneratePlan : null}
          />
        </div>

        {travelPlan && (
          <div className="plan-section">
            <div className="plan-header-actions">
              <button 
                className="new-conversation-button"
                onClick={handleStartNewConversation}
              >
                <span>💬</span>
                Start New Conversation
              </button>
            </div>
            <TravelPlanDisplay
              travelPlan={travelPlan}
              onBookPlan={handleBookPlan}
            />
          </div>
        )}
      </div>

      {isGeneratingPlan && (
        <div className="generating-overlay">
          <div className="generating-content">
            <div className="spinner-large"></div>
            <h3>Creating Your Perfect Travel Plan...</h3>
            <p>Searching flights, finding hotels, and building itinerary</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;