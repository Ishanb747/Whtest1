import React from 'react';
import { LoadingOverlay } from './components/shared';
import GameHeader from './components/GameHeader';
import StartScreen from './components/screens/StartScreen';
import ChatScreen from './components/screens/ChatScreen';
import ResultsScreen from './components/screens/ResultsScreen';
import ChatInput from './components/chat/ChatInput';
import useGameLogic from './hooks/useGameLogic';
import GlobalStyles from './styles/GlobalStyles';

const App = () => {
  const {
    gameState,
    topic,
    messages,
    userInput,
    setUserInput,
    isLoading,
    error,
    gameResult,
    handleStartGame,
    handleSendMessage
  } = useGameLogic();

  const renderGameState = () => {
    switch (gameState) {
      case 'in_progress':
        return <ChatScreen topic={topic} messages={messages} />;
      case 'voting':
        return <div className="flex-1 overflow-y-auto"><ChatScreen topic={topic} messages={messages} /></div>;
      case 'finished':
        return <ResultsScreen result={gameResult} onRestart={handleStartGame} isLoading={isLoading} />;
      case 'not_started':
      default:
        return <StartScreen onStart={handleStartGame} isLoading={isLoading} error={error} />;
    }
  };

  return (
    <>
      <GlobalStyles />
      <div className="animated-bg text-white min-h-screen flex flex-col items-center justify-center font-sans p-4">
        <div className="relative w-full max-w-3xl h-[95vh] bg-black bg-opacity-40 rounded-lg shadow-2xl flex flex-col border-2 border-blue-900/50 overflow-hidden">
          
          {(gameState === 'voting' || (gameState !== 'in_progress' && isLoading)) && <LoadingOverlay />}
          
          <GameHeader />

          <main className="flex-1 overflow-y-auto">
            {renderGameState()}
          </main>

          {gameState === 'in_progress' && (
            <ChatInput 
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onSubmit={handleSendMessage}
              isLoading={isLoading}
            />
          )}
        </div>
      </div>
    </>
  );
};

export default App;