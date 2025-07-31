import React from 'react';
import { ThemedSpinner } from '../shared';

const ChatInput = ({ value, onChange, onSubmit, isLoading, isTyping = false }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit(e);
    }
  };

  const isDisabled = isLoading || isTyping || !value.trim();

  return (
    <footer className="p-4 bg-black bg-opacity-50 border-t-2 border-blue-900">
      <div className="flex items-center gap-4">
        <input
          type="text"
          value={value}
          onChange={onChange}
          onKeyPress={handleKeyPress}
          placeholder={isTyping ? "Someone is typing..." : "Your response..."}
          disabled={isLoading || isTyping}
          className="flex-1 bg-gray-900 border-2 border-gray-600 rounded-md px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition placeholder-gray-500 disabled:opacity-50"
        />
        <button
          onClick={onSubmit}
          disabled={isDisabled}
          className="px-6 py-3 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-500 transition-colors disabled:bg-gray-700 disabled:cursor-not-allowed flex items-center justify-center w-32"
        >
          {isLoading ? (
            <ThemedSpinner />
          ) : isTyping ? (
            <span className="text-sm">Wait...</span>
          ) : (
            'Send'
          )}
        </button>
      </div>
      {isTyping && (
        <div className="mt-2 text-center">
          <p className="text-yellow-400 text-sm animate-pulse">
            Players are responding...
          </p>
        </div>
      )}
    </footer>
  );
};

export default ChatInput;