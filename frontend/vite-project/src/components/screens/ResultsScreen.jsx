import React from 'react';
import { ThemedButton } from '../shared';

const ResultsScreen = ({ result, onRestart, isLoading }) => (
  <div className="text-center h-full flex flex-col justify-center items-center p-6 animate-fade-in">
    <h2 className={`text-6xl font-black uppercase tracking-widest mb-4 ${result.result.includes('Win') ? 'text-green-400' : 'text-red-400'}`}>
      {result.result.includes('Win') ? 'Victory' : 'Defeat'}
    </h2>
    <p className="text-lg text-gray-300 mb-8">{result.result}</p>
    <p className="mb-8 text-xl">You received <span className="font-bold text-blue-400 text-2xl">{result.votes_for_human}</span> out of 4 votes.</p>
     
    <div className="w-full max-w-lg bg-black bg-opacity-50 p-4 rounded-lg border border-blue-900 text-left mb-8">
      <h3 className="font-bold mb-4 text-xl text-center tracking-wider uppercase">Voting Analysis</h3>
      <ul className="space-y-3 text-sm">
        {result.ai_votes.map((vote, index) => (
          <li key={index} className="p-3 bg-gray-900 bg-opacity-70 rounded-md border-l-4 border-blue-600">
            <p><span className="font-bold text-white">{vote.voter}</span> voted for <span className="font-bold text-blue-400">{vote.voted_for}</span></p>
            <p className="text-gray-400 italic mt-1">Reason: "{vote.reasoning.split('[Reason]:')[1]?.trim()}"</p>
          </li>
        ))}
      </ul>
    </div>

<ThemedButton onClick={() => window.location.reload()} disabled={isLoading}>
  {isLoading ? 'Restarting...' : 'Play Again'}
</ThemedButton>

  </div>
);

export default ResultsScreen;