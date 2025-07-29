import React from 'react';
import { ThemedButton } from '../shared';

const StartScreen = ({ onStart, isLoading, error }) => (
  <div className="flex flex-col items-center justify-center h-full text-center p-4">
    <h2 className="text-3xl font-bold uppercase tracking-widest text-white mb-2">Welcome to the Game</h2>
    <p className="text-blue-300 mb-8">Your personality will be tested. Your humanity, questioned.</p>
    <ThemedButton onClick={onStart} disabled={isLoading}>
      {isLoading ? 'Initializing...' : 'Begin Session'}
    </ThemedButton>
    {error && <p className="text-red-500 mt-4 animate-pulse">{error}</p>}
  </div>
);

export default StartScreen;