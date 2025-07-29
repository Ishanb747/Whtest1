# topic.py
# Generates a new discussion topic.

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import os

class Topic:
    def __init__(self):
        """
        Initializes the Groq model for topic generation.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
            
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama3-70b-8192",
            temperature=1  # Higher temperature for more creative/varied topics
        )

    def Generate(self):
        """
        Generates a single, short, and engaging opinion-based topic.
        """
        messages = [
            SystemMessage(content="You are the head of a community that shares interesting topics anyone can share their opinion or experience on. Generate only one short and engaging topic. Do not include any explanation or description — just output the topic line."),
            HumanMessage(content="Give me one opinion-based topic.")
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content