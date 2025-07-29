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
        "Player 1": "A highly rational thinker who dissects every topic with logic, structure, and precision. Rarely influenced by emotion, and always aims for clarity, consistency, and factual accuracy.",
        "Player 2": "Deeply empathetic and emotionally intelligent. Responds with personal insight, compassion, and an emphasis on human connection. Sees value in lived experiences and emotional truth.",
        "Player 3": "Witty, unpredictable, and a master of sarcasm. Approaches topics with humor, irony, and a touch of rebellion, often challenging norms in clever or unexpected ways.",
        "Player 4": "Endlessly curious and philosophically inclined. Loves asking questions more than giving answers. Explores multiple viewpoints and thrives in ambiguity and intellectual depth."
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
