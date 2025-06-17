import React, { useState } from 'react';
import ChatWidget from './ChatWidget';

const ChatPopup = () => {
  const [isOpen, setIsOpen] = useState(false);

  const togglePopup = () => {
    setIsOpen(!isOpen);
  };

  // Basic styling for the popup button and widget container
  const popupButtonStyle = {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    padding: '15px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '50px', // Makes it rounder
    cursor: 'pointer',
    boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
    fontSize: '1.5em', // Larger icon/text
    zIndex: 9998, // Below widget, above content
  };

  const widgetContainerStyle = {
    position: 'fixed',
    bottom: '90px', // Above the button
    right: '20px',
    width: '350px',
    maxWidth: '90vw',
    maxHeight: '80vh',
    boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
    borderRadius: '10px',
    zIndex: 9999, // Above button and content
    display: isOpen ? 'block' : 'none',
    backgroundColor: 'white', // Ensure it has a background
  };

  return (
    <>
      <button onClick={togglePopup} style={popupButtonStyle}>
        {isOpen ? '✕' : '💬'}
      </button>
      {isOpen && (
        <div style={widgetContainerStyle}>
          <ChatWidget />
        </div>
      )}
    </>
  );
};

export default ChatPopup;
