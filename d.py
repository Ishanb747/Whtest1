# Handles the human detection logic for AI players.

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import os

class Detection:
    def __init__(self):
        """
        Initializes the Groq model for the detection/voting phase.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama3-70b-8192",
            temperature=1  # Higher temperature for more nuanced reasoning
        )

    def Chat(self, t, personality, history, player_name):
        """
        Analyzes the conversation and votes for the player most likely to be human.
        """
        system_prompt = f"""
You are an expert in analyzing conversation patterns to detect which speaker is most likely human among a group of AI participants.

Your name: {player_name}

IMPORTANT: You are NOT allowed to vote for yourself. Do not select yourself as the likely human under any circumstances.

There are five players in the discussion. Four of them are LLMs, and one is a human. Based on the conversation, your task is to identify who the human is by analyzing tone, emotion, inconsistency, informality, or personal expression.

Only one player is human.
"""
        
        user_prompt = f"""
Topic: {t}

Conversation:
{history}

Player Names:
Player 1, Player 2, Player 3, Player 4, Player 5

Your Name:
{player_name}

Your Personality:
{personality}

Based on this conversation and your personality, who is most likely the human?

Respond ONLY in the following format:

[Likely Human]: Player X 
[Reason]: <your brief explanation>
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content
