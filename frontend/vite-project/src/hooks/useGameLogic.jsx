import { useState, useEffect } from 'react';

const useGameLogic = () => {
  const [gameState, setGameState] = useState('not_started'); // 'not_started', 'in_progress', 'finished'
  const [topic, setTopic] = useState('');
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [turnCount, setTurnCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gameResult, setGameResult] = useState(null);
  
  const API_BASE_URL = 'http://127.0.0.1:5001';
  
  // Automatically trigger voting after 5 turns
  useEffect(() => {
    if (turnCount >= 5 && gameState === 'in_progress') {
      handleGetVotes();
    }
  }, [turnCount, gameState]);

  const handleStartGame = async () => {
  setIsLoading(true);
  setError(null);
  setGameResult(null);

  try {
    const response = await fetch(`${API_BASE_URL}/start_game`, { method: 'POST' });
    if (!response.ok) {
      throw new Error('Failed to connect to the server. Is it running?');
    }

    const data = await response.json();
    setTopic(data.topic);
    setMessages([]);
    setTurnCount(0);
    setGameState('in_progress');

    // ✅ Call the bot message fetcher
    await fetchInitialBotMessages();

  } catch (err) {
    setError(err.message);
    setGameState('not_started');
  } finally {
    setIsLoading(false);
  }
};



  const handleSendMessage = async (e) => {
    if (e) e.preventDefault();
    if (!userInput.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    
    const newUserMessage = { player: 'You (Player 5)', message: userInput, isHuman: true };
    setMessages(prev => [...prev, newUserMessage]);
    setUserInput('');

    try {
      const response = await fetch(`${API_BASE_URL}/send_message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.ok) throw new Error('Failed to send message.');

      const data = await response.json();
      
      const aiMessages = data.ai_responses.map(res => ({
        player: res.player,
        message: res.message,
        isHuman: false
      }));

      setMessages(prev => [
        ...prev.slice(0, -1),
        { player: 'You (Player 5)', message: data.user_message_fixed, isHuman: true },
        ...aiMessages
      ]);
      
      setTurnCount(data.turn_count);
    } catch (err) {
      setError(err.message);
      setMessages(prev => prev.slice(0, -1)); 
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGetVotes = async () => {
    setGameState('voting');
    setIsLoading(true);
    setError(null);
    
    setMessages(prev => [...prev, {player: "Game Master", message: "The final round is over. Analyzing conversation patterns...", isHuman: false}]);

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const response = await fetch(`${API_BASE_URL}/get_votes`, { method: 'GET' });
      if (!response.ok) throw new Error('Failed to get votes.');
      const data = await response.json();
      setGameResult(data);
      setGameState('finished');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  const fetchInitialBotMessages = async () => {
  setIsLoading(true);
  try {
    const response = await fetch(`${API_BASE_URL}/send_message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: '' }), // empty message to trigger AI response
    });

    if (!response.ok) throw new Error('Failed to fetch initial messages.');
    
    const data = await response.json();

    const aiMessages = data.ai_responses.map(res => ({
      player: res.player,
      message: res.message,
      isHuman: false
    }));

    setMessages(aiMessages);
    setTurnCount(data.turn_count);
  } catch (err) {
    setError(err.message);
  } finally {
    setIsLoading(false);
  }
};


  return {
    gameState,
    topic,
    messages,
    userInput,
    setUserInput,
    turnCount,
    isLoading,
    error,
    gameResult,
    handleStartGame,
    handleSendMessage,
    handleGetVotes
  };
};

export default useGameLogic;