import React from 'react';

// A more stylized loading spinner for the theme
export const ThemedSpinner = () => (
  <div className="relative w-8 h-8">
    <div className="absolute inset-0 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
    <div className="absolute inset-2 border-2 border-blue-400 border-b-transparent rounded-full animate-spin-reverse"></div>
  </div>
);

// A loading overlay for when the whole screen is busy
export const LoadingOverlay = () => (
  <div className="absolute inset-0 bg-black bg-opacity-75 flex flex-col items-center justify-center z-50">
    <ThemedSpinner />
    <p className="mt-4 text-blue-300 tracking-widest">LOADING...</p>
  </div>
);

// Themed button with sharp angles and hover effects
export const ThemedButton = ({ onClick, disabled, children, className = '' }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className={`relative px-8 py-3 bg-blue-600 text-white font-bold tracking-wider uppercase overflow-hidden transition-all duration-300 ease-in-out disabled:bg-gray-600 disabled:cursor-not-allowed hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-gray-900 ${className}`}
  >
    <span className="relative z-10">{children}</span>
    <div className="absolute inset-0 bg-white opacity-0 transition-opacity duration-300 group-hover:opacity-20"></div>
  </button>
);