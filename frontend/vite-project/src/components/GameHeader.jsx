import React from 'react';

const GameHeader = () => (
  <header className="relative text-center p-5 border-b-2 border-blue-900 bg-black bg-opacity-30">
    <h1 className="text-4xl font-extrabold text-white tracking-wider uppercase">
      Human <span className="text-blue-400">or</span> Not?
    </h1>
    <p className="text-sm text-blue-200 mt-1 tracking-widest">Evade detection for 3 rounds.</p>
  </header>
);

export default GameHeader;