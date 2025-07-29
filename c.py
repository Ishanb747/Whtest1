# c.py
# Handles the conversation logic for AI players.

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import os

class Conversation:
    def __init__(self):
        """
        Initializes the Groq model for conversation responses.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama3-70b-8192",
            temperature=1  # Higher temperature for more human-like, varied responses
        )

    def Chat(self, t, personality, history, player_name):
        """
        Generates a chat response for an AI player based on its personality.
        """
        system_prompt = f"""
You are one of five players in a group discussion on a given topic.

Your personality: {personality}

Speak naturally and keep your replies brief—like a real conversation. Limit your response to **no more than 20 words**. Respond in your own style, add to what others say, and stay on topic. Avoid repeating points unless you're building on them.

Let your personality shape how you think and speak.
"""
        
        user_prompt = f"""
Topic: {t}

Conversation so far:
{history}

Your turn. Respond as [{player_name}].
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content