import React, { useState, useEffect, useCallback, useRef } from 'react';

const useGameLogic = () => {
  const [gameState, setGameState] = useState('not_started'); // 'not_started', 'in_progress', 'finished'
  const [topic, setTopic] = useState('');
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [turnCount, setTurnCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gameResult, setGameResult] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [typingPlayer, setTypingPlayer] = useState('');
  
  const API_BASE_URL = 'http://127.0.0.1:5001';
  
  // Sound effects using Web Audio API
  const playSound = useCallback((type) => {
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      // Different sounds for different events
      switch (type) {
        case 'message':
          oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
          oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
          gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
          oscillator.start(audioContext.currentTime);
          oscillator.stop(audioContext.currentTime + 0.2);
          break;
        case 'typing':
          oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
          gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
          oscillator.start(audioContext.currentTime);
          oscillator.stop(audioContext.currentTime + 0.1);
          break;
        case 'gameStart':
          oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
          oscillator.frequency.setValueAtTime(880, audioContext.currentTime + 0.1);
          oscillator.frequency.setValueAtTime(660, audioContext.currentTime + 0.2);
          gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
          oscillator.start(audioContext.currentTime);
          oscillator.stop(audioContext.currentTime + 0.3);
          break;
      }
    } catch (error) {
      console.log('Audio not supported or blocked');
    }
  }, []);

  // Function to add messages with realistic delays
  const addMessagesWithDelay = useCallback(async (messagesToAdd) => {
    for (let i = 0; i < messagesToAdd.length; i++) {
      const message = messagesToAdd[i];
      const delay = Math.random() * 3000 + 1500; // Random delay between 1.5-4.5 seconds
      
      // Show typing indicator
      if (!message.isHuman) {
        setIsTyping(true);
        setTypingPlayer(message.player);
        playSound('typing');
        
        // Random typing duration (0.5-2 seconds)
        const typingDuration = Math.random() * 1500 + 500;
        await new Promise(resolve => setTimeout(resolve, typingDuration));
        
        setIsTyping(false);
        setTypingPlayer('');
      }
      
      // Add the actual message
      setMessages(prev => [...prev, message]);
      playSound('message');
      
      // Wait before next message (except for the last one)
      if (i < messagesToAdd.length - 1) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }, [playSound]);

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
      
      playSound('gameStart');

      // Fetch and display initial bot messages with delays
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
    if (!userInput.trim() || isLoading || isTyping) return;

    setIsLoading(true);
    setError(null);
    
    const newUserMessage = { player: 'You (Player 5)', message: userInput, isHuman: true };
    setMessages(prev => [...prev, newUserMessage]);
    playSound('message');
    setUserInput('');

    try {
      const response = await fetch(`${API_BASE_URL}/send_message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.ok) throw new Error('Failed to send message.');

      const data = await response.json();
      
      // Update user message with server response
      setMessages(prev => [
        ...prev.slice(0, -1),
        { player: 'You (Player 5)', message: data.user_message_fixed, isHuman: true }
      ]);
      
      // Add AI messages with realistic delays
      const aiMessages = data.ai_responses.map(res => ({
        player: res.player,
        message: res.message,
        isHuman: false
      }));

      await addMessagesWithDelay(aiMessages);
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
    
    const gameMasterMessage = {
      player: "Game Master", 
      message: "The final round is over. Analyzing conversation patterns...", 
      isHuman: false
    };
    
    await addMessagesWithDelay([gameMasterMessage]);

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

      await addMessagesWithDelay(aiMessages);
      setTurnCount(data.turn_count);
      
    } catch (err) {
      setError(err.message);
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
    isTyping,
    typingPlayer,
    handleStartGame,
    handleSendMessage,
    handleGetVotes
  };
};

export default useGameLogic;