import React from 'react';

const ChatMessage = ({ player, message, isHuman, isTyping = false }) => {
  const isGameMaster = player === "Game Master";
  
  if (isGameMaster) {
    return (
      <div className="text-center my-4">
        <p className="text-blue-300 italic px-4 py-2 bg-blue-900 bg-opacity-50 rounded-md inline-block">
          {message}
        </p>
      </div>
    );
  }

  const alignment = isHuman ? 'items-end' : 'items-start';
  const bubbleColor = isHuman ? 'bg-blue-800' : isTyping ? 'bg-gray-600' : 'bg-gray-700';
  const textAlign = isHuman ? 'text-right' : 'text-left';

  return (
    <div className={`flex flex-col ${alignment} mb-4 animate-fade-in-up`}>
      <div className={`max-w-xl w-full p-4 rounded-lg shadow-lg ${bubbleColor} bg-opacity-80 backdrop-blur-sm border border-gray-600 transition-all duration-300`}>
        <p className={`font-bold text-sm ${isHuman ? 'text-blue-300' : 'text-gray-300'} mb-1 ${textAlign}`}>
          {player} {isTyping && <span className="text-yellow-400 animate-pulse">(typing...)</span>}
        </p>
        {isTyping ? (
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        ) : (
          <p className="text-white break-words">{message}</p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;