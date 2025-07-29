import React from 'react';

const ChatMessage = ({ player, message, isHuman }) => {
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
  const bubbleColor = isHuman ? 'bg-blue-800' : 'bg-gray-700';
  const textAlign = isHuman ? 'text-right' : 'text-left';

  return (
    <div className={`flex flex-col ${alignment} mb-4 animate-fade-in-up`}>
      <div className={`max-w-xl w-full p-4 rounded-lg shadow-lg ${bubbleColor} bg-opacity-80 backdrop-blur-sm border border-gray-600`}>
        <p className={`font-bold text-sm ${isHuman ? 'text-blue-300' : 'text-gray-300'} mb-1 ${textAlign}`}>{player}</p>
        <p className="text-white break-words">{message}</p>
      </div>
    </div>
  );
};

export default ChatMessage;