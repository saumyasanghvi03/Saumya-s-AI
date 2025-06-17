import React from 'react';
import ChatPopup from './components/ChatPopup'; // Assuming ChatPopup.jsx is in components/
import './App.css'; // Keep or add your global styles

function App() {
  return (
    <div className="App">
      {/* You could have other page content here if this was a full app */}
      {/* For the widget, ChatPopup handles its own fixed positioning */}
      <ChatPopup />
    </div>
  );
}

export default App;
