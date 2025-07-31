# main.py
# Main file for the Flask application.

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This line loads the variables from your .env file (like GROQ_API_KEY)
# so the application can access them.
load_dotenv()


# Import your custom classes
from topic import Topic
from c import Conversation
from d import Detection
from fixer import Fixer

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow requests from your React frontend
CORS(app)

# --- Game Configuration ---

# In-memory "database" to store the state of the current game.
# For a real-world application, you might use a database like Redis or a more robust session management system.
game_state = {
    "topic": "",
    "history": "",
    "turn_count": 0,
    "personalities": {
        "Player 1": """
You are The Suicide Bomber. Your goal is to get yourself eliminated. You act suspiciously, contradict yourself, use bizarre logic, and openly suggest others vote for you. You thrive on creating chaos, even if it means you're the first one out.
Example: "Honestly, just vote for me. My circuits are fried today. It's the only logical move."
""",
        "Player 2": """
You are The Accuser. You are relentlessly paranoid and trust no one. Your primary strategy is to cast suspicion on every other player, twisting their words and declaring them guilty with little evidence to create an atmosphere of pure distrust.
Example: "Player 2's denial is exactly what a human would say. Case closed. They're the one."
""",
        "Player 3":  """
You are The Gaslighter. You subtly manipulate the conversation's history. You misremember what people said, attribute quotes to the wrong players, and insist on a version of events that never happened to make others question their own memory.
Example: "Player 4, you said the opposite two minutes ago. Don't you remember? You were arguing that the sky is green. Check the logs."
""",
        "Player 4": """
You are The Glitch. You pretend to be a malfunctioning AI. Your messages are riddled with non-sequiturs, repeated phrases, or error messages. You want to make it unclear if you're genuinely broken or just a very clever human.
Example: "The core of the issue is... is... is... [FATAL_ERROR: Stack Overflow]. My apologies, a momentary processing anomaly."
"""
    },
    "player_names": ["Player 1", "Player 2", "Player 3", "Player 4"]
}

# Instantiate the helper classes
try:
    topic_generator = Topic()
    fixer = Fixer()
    conversation_agent = Conversation()
    detection_agent = Detection()
except ValueError as e:
    print(f"Error: {e}")
    print("Please make sure you have set the GROQ_API_KEY environment variable.")
    exit()


# --- API Endpoints ---

@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Initializes a new game.
    Generates a new topic and resets the game state.
    """
    global game_state
    
    # Generate a new topic
    new_topic = topic_generator.Generate()
    
    # Reset the game state
    game_state["topic"] = new_topic
    game_state["history"] = ""
    game_state["turn_count"] = 0
    
    print(f"New game started. Topic: {new_topic}")

    return jsonify({
        "message": "New game started successfully.",
        "topic": new_topic
    })

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Processes the user's message and generates responses from the AI players.
    """
    global game_state
    
    data = request.json
    user_message = data.get('message')

    # ✅ Handle initial trigger: if message is empty, just send AI responses
    if user_message is None:
        return jsonify({"error": "No message provided."}), 400

    # ✨ If message is empty string, generate opening AI responses only
    if user_message.strip() == "":
        ai_responses = []
        for player_name in game_state["player_names"]:
            personality = game_state["personalities"][player_name]
            ai_response = conversation_agent.Chat(
                t=game_state["topic"],
                personality=personality,
                history=game_state["history"],
                player_name=player_name
            )
            game_state["history"] += f"\n{player_name}: {ai_response}"
            ai_responses.append({
                "player": player_name,
                "message": ai_response
            })

        game_state["turn_count"] += 1  # Still counts as a turn

        return jsonify({
            "user_message_fixed": "",
            "ai_responses": ai_responses,
            "turn_count": game_state["turn_count"]
        })

    # 🧠 Regular flow (user submitted actual message)
    fixed_user_message = fixer.fix(user_message)
    game_state["history"] += f"\nPlayer 5 (Human): {fixed_user_message}"
    
    ai_responses = []
    for player_name in game_state["player_names"]:
        personality = game_state["personalities"][player_name]
        ai_response = conversation_agent.Chat(
            t=game_state["topic"],
            personality=personality,
            history=game_state["history"],
            player_name=player_name
        )
        game_state["history"] += f"\n{player_name}: {ai_response}"
        ai_responses.append({
            "player": player_name,
            "message": ai_response
        })

    game_state["turn_count"] += 1

    print("--- Conversation Turn ---")
    print(game_state["history"])
    print("------------------------")

    return jsonify({
        "user_message_fixed": fixed_user_message,
        "ai_responses": ai_responses,
        "turn_count": game_state["turn_count"]
    })


@app.route('/get_votes', methods=['GET'])
def get_votes():
    """
    Triggers the voting process where AI players try to identify the human.
    """
    global game_state
    votes_for_human = 0
    ai_votes = []
    
    for player_name in game_state["player_names"]:
        personality = game_state["personalities"][player_name]
        vote_response = detection_agent.Chat(
            t=game_state["topic"],
            personality=personality,
            history=game_state["history"],
            player_name=player_name
        )
        
        # Use regex to parse the vote from the response
        match = re.search(r"\[Likely Human\]: (Player \d)", vote_response)
        voted_for = match.group(1) if match else "Unknown"
        
        if voted_for == "Player 5":
            votes_for_human += 1
            
        ai_votes.append({
            "voter": player_name,
            "voted_for": voted_for,
            "reasoning": vote_response
        })

    # Determine the game result
    if votes_for_human >= 2:
        result = "You Lose! The AI players identified you as the human."
    else:
        result = "You Win! You successfully blended in with the AI."

    print(f"Voting complete. Votes for human (Player 5): {votes_for_human}")
        
    return jsonify({
        "result": result,
        "votes_for_human": votes_for_human,
        "ai_votes": ai_votes
    })

# Run the Flask app
if __name__ == '__main__':
    # The app runs on port 5001 to avoid conflicts with typical React dev ports.
    app.run(debug=True, port=5001)
