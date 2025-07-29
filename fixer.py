# fixer.py
# Fixes grammar and sentence structure for user input.

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import os

class Fixer:
    def __init__(self):
        """
        Initializes the Groq model for text correction.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama3-70b-8192",
            temperature=0.2  # Lower temperature for more deterministic, precise corrections
        )
        
        self.system_prompt = """
You are a world-class English editor and writing assistant. Your job is to correct grammar, fix sentence structure, and enhance clarity without changing the original meaning of the user's message.

You always preserve the intent and tone unless told otherwise. You respond only with the improved version of the sentence, and nothing else.

DO NOT include any introductions, explanations, or labels like "Improved Sentence" or "Correction".  
DO NOT add quotes.  
Just return the fixed sentence only.
If the input is already correct, return it as-is.
"""

    def fix(self, user_input):
        """
        Corrects the provided user input string.
        """
        user_prompt = f'Original Sentence:\n"{user_input}"'
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content