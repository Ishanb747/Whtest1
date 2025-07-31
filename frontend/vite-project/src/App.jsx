import React, { useState, useRef, useEffect } from 'react';
import { LoadingOverlay } from './components/shared';
import GameHeader from './components/GameHeader';
import StartScreen from './components/screens/StartScreen';
import ChatScreen from './components/screens/ChatScreen';
import ResultsScreen from './components/screens/ResultsScreen';
import ChatInput from './components/chat/ChatInput';
import useGameLogic from './hooks/useGameLogic';
import GlobalStyles from './styles/GlobalStyles';

const songList = [
  '/cyn.mp3',
  '/Dn.mp3',
];

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
    isTyping,
    typingPlayer,
    handleStartGame,
    handleSendMessage
  } = useGameLogic();

  const [currentSongIndex, setCurrentSongIndex] = useState(0); // Initialized to 0, but overridden in useEffect
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    // Set an initial random song when the component mounts
    const initialRandomIndex = Math.floor(Math.random() * songList.length);
    setCurrentSongIndex(initialRandomIndex); 

    const playMusic = async () => {
      try {
        await audio.play();
      } catch (error) {
        console.log("Audio autoplay was prevented. Waiting for user interaction.");
      }
    };
    
    const handleFirstInteraction = () => {
      playMusic();
      document.removeEventListener('click', handleFirstInteraction);
    };
    
    document.addEventListener('click', handleFirstInteraction);
    
    return () => {
      document.removeEventListener('click', handleFirstInteraction);
    };
  }, []);

  const handleSongEnd = () => {
    // Select a random index for the next song
    const randomIndex = Math.floor(Math.random() * songList.length);
    setCurrentSongIndex(randomIndex);
  };

  const handleAudioReady = () => {
    if (audioRef.current) {
      audioRef.current.volume = 0.013; // Set volume here, adjust as needed
    }
  };

  useEffect(() => {
    if (audioRef.current) {
        audioRef.current.load(); // Tell the audio element to load the new source
        audioRef.current.play().catch(e => console.log("Play interrupted or failed. A user interaction might be needed."));
    }
  }, [currentSongIndex]); // This effect runs when currentSongIndex changes

  const renderGameState = () => {
    switch (gameState) {
      case 'in_progress':
        return <ChatScreen topic={topic} messages={messages} isTyping={isTyping} typingPlayer={typingPlayer} />;
      case 'voting':
        return (
          <div className="flex-1 overflow-y-auto">
            <ChatScreen topic={topic} messages={messages} isTyping={isTyping} typingPlayer={typingPlayer} />
          </div>
        );
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
          
          <audio 
            ref={audioRef} 
            src={songList[currentSongIndex]}
            onEnded={handleSongEnd}
            onLoadedData={handleAudioReady}
            aria-hidden="true" 
          />

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
              isTyping={isTyping}
            />
          )}
        </div>
      </div>
    </>
  );
};

export default App;