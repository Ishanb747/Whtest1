import React, { useEffect, useRef } from 'react';
import ChatMessage from '../chat/ChatMessage';

const ChatScreen = ({ topic, messages = [], isTyping = false, typingPlayer = '' }) => {
  const chatEndRef = useRef(null);
  
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <>
      <div className="text-center mb-6 p-4 bg-black bg-opacity-50 border-y-2 border-blue-900">
        <p className="text-blue-300 text-sm tracking-widest uppercase">Current Topic</p>
        <p className="font-bold text-xl text-white mt-1">{topic}</p>
      </div>
      <div className="px-6 pb-6 space-y-4">
        {messages.map((msg, index) => (
          <ChatMessage 
            key={index} 
            player={msg.player} 
            message={msg.message} 
            isHuman={msg.isHuman} 
          />
        ))}
        {isTyping && (
          <ChatMessage 
            player={typingPlayer} 
            message="" 
            isHuman={false} 
            isTyping={true} 
          />
        )}
        <div ref={chatEndRef} />
      </div>
    </>
  );
};

export default ChatScreen;