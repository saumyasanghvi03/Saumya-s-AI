import React from 'react';

const MessageList = ({ messages }) => {
  return (
    <div style={{ maxHeight: '300px', overflowY: 'auto', padding: '10px', flexGrow: 1 }}>
      {messages.map((msg, index) => (
        <div
          key={index}
          style={{
            marginBottom: '10px',
            padding: '8px 12px',
            borderRadius: '7px',
            backgroundColor: msg.sender === 'user' ? '#007bff' : '#e9ecef',
            color: msg.sender === 'user' ? 'white' : 'black',
            textAlign: msg.sender === 'user' ? 'right' : 'left',
            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '70%',
            marginLeft: msg.sender === 'user' ? 'auto' : '0',
            marginRight: msg.sender === 'user' ? '0' : 'auto',
          }}
        >
          {msg.text}
          {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
            <div style={{ fontSize: '0.8em', color: msg.sender === 'user' ? '#f0f0f0' : '#555', marginTop: '5px' }}>
              <small>Sources:</small>
              <ul style={{ margin: '2px 0 0 15px', padding: 0 }}>
                {msg.sources.slice(0, 2).map((source, idx) => (
                  <li key={idx} title={source.metadata ? `Source: ${source.metadata.source}` : 'Source document'}>
                    {source.content.substring(0, 50)}...
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageList;
