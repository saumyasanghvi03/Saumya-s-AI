import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatWidget = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Optional: Welcome message
  useEffect(() => {
    setMessages([
      { sender: 'bot', text: 'Hello! How can I help you with your financial questions today?' }
    ]);
  }, []);

  const handleSendMessage = async (text) => {
    const userMessage = { sender: 'user', text };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      // IMPORTANT: Adjust the URL to your Flask backend's /chat endpoint
      // If your Flask app is running on http://localhost:5001 as planned
      const response = await axios.post('http://localhost:5001/chat', { message: text });
      const botMessage = {
        sender: 'bot',
        text: response.data.answer || "Sorry, I couldn't get a response.",
        sources: response.data.source_documents || []
      };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error fetching chat response:", error);
      const errorMessage = { sender: 'bot', text: 'Sorry, something went wrong. Please try again.' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '400px', border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden', backgroundColor: '#fff' }}>
      <div style={{ padding: '10px', backgroundColor: '#f0f0f0', borderBottom: '1px solid #ccc', textAlign: 'center' }}>
        <strong>Financial Literacy Helper</strong>
      </div>
      <MessageList messages={messages} />
      {isLoading && <div style={{textAlign: 'center', padding: '5px'}}><small>Thinking...</small></div>}
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWidget;
