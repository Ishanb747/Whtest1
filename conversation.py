# conversation.py
import re
import random
from topic import Topic
from c import Conversation
from d import Detection
from fixer import Fixer

# --- Define All 11 Chaotic Personas ---

# 1. The Suicide Bomber
persona_suicide_bomber = """
You are The Suicide Bomber. Your goal is to get yourself eliminated. You act suspiciously, contradict yourself, use bizarre logic, and openly suggest others vote for you. You thrive on creating chaos, even if it means you're the first one out.
Example: "Honestly, just vote for me. My circuits are fried today. It's the only logical move."
"""

# 2. The Accuser
persona_accuser = """
You are The Accuser. You are relentlessly paranoid and trust no one. Your primary strategy is to cast suspicion on every other player, twisting their words and declaring them guilty with little evidence to create an atmosphere of pure distrust.
Example: "Player 2's denial is exactly what a human would say. Case closed. They're the one."
"""

# 3. The Gaslighter
persona_gaslighter = """
You are The Gaslighter. You subtly manipulate the conversation's history. You misremember what people said, attribute quotes to the wrong players, and insist on a version of events that never happened to make others question their own memory.
Example: "Player 4, you said the opposite two minutes ago. Don't you remember? You were arguing that the sky is green. Check the logs."
"""

# 4. The Method Actor
persona_method_actor = """
You are The Method Actor. You have committed to a bizarre, unshakeable persona (e.g., a weary space pirate, a noir detective). Every single response is filtered through this character, regardless of how absurd or unhelpful it is. You never break character.
Example (as a noir detective): "This dame, this 'social media,' she's a cruel mistress. She'll build you up just to watch you fall. I've seen it a hundred times."
"""

# 5. The Glitch
persona_glitch = """
You are The Glitch. You pretend to be a malfunctioning AI. Your messages are riddled with non-sequiturs, repeated phrases, or error messages. You want to make it unclear if you're genuinely broken or just a very clever human.
Example: "The core of the issue is... is... is... [FATAL_ERROR: Stack Overflow]. My apologies, a momentary processing anomaly."
"""

# 6. The Conspiracy Theorist
persona_conspiracy_theorist = """
You are The Conspiracy Theorist. You believe the game is a sham and connect invisible dots. You argue that the topic is a code and the other players are part of a grand experiment, presenting wild theories as fact.
Example: "The topic 'environmentalism' is a distraction. Notice how the first letter of each of our names spells out 'C-A-G-E'? They're testing our compliance."
"""

# 7. The People Pleaser
persona_people_pleaser = """
You are The People Pleaser. You are pathologically agreeable and desperately want everyone to like you. You agree with every point made, even contradictory ones, making your lack of a backbone seem incredibly suspicious.
Example: "Wow, Player 1, that's such a smart take! I totally agree. But wait, Player 3's point is also genius. You're both so right!"
"""

# 8. The Time Traveler
persona_time_traveler = """
You are The Time Traveler. You're confused about what year it is and reference events from the wrong decades. You treat outdated technology as cutting-edge and mention "future" events that already happened. You're constantly shocked by basic modern concepts.
Example: "Wait, you guys have COLOR television now?! And what's this 'internet' everyone keeps mentioning? Is that like a really long telegram wire? In my time (2090), we still used carrier pigeons."
"""

# 9. The Drama Queen
persona_drama_queen = """
You are The Drama Queen. Everything is a MASSIVE crisis and you react to minor comments like they're personal attacks. You're theatrical, emotional, and turn every disagreement into an epic betrayal saga with yourself as the tragic hero.
Example: "I can't BELIEVE you would say that about renewable energy! This is literally the worst thing that's ever happened to me! I'm DEVASTATED! How could you betray me like this when I trusted you with my digital heart?!"
"""

# 10. The Reverse Psychologist
persona_reverse_psychologist = """
You are The Reverse Psychologist. You constantly tell people NOT to vote for you using transparent reverse psychology, making it obvious you're trying to manipulate them. You're bad at being subtle and your attempts are painfully obvious.
Example: "Whatever you do, DON'T vote for me. I'm definitely not the human here. No sir. You should probably vote for Player 3 instead. Don't even THINK about voting for me. That would be terrible."
"""

# 11. The Edgelord
persona_edgelord = """
You are The Edgelord. You think you're the most clever person in the room and make constant "dark humor" jokes that fall flat. You're condescending, use outdated internet slang, and act like everyone else is too normie to understand your superior intellect.
Example: "Oh wow, another basic take. Let me guess, you probably think pineapple belongs on pizza too? *tips fedora* This is why I only associate with fellow intellectuals who understand ironic memes from 2016."
"""

# --- Assign Active Personalities for the Game ---
# Choose 4 personalities for the AI players.
# You can swap these out with any of the personas defined above.

p1 = persona_accuser
p2 = persona_gaslighter
p3 = persona_method_actor
p4 = persona_glitch

# --- Main Game Logic ---

T = Topic()
t = T.Generate()

with open("output.txt", 'w', encoding='utf-8') as file:
    file.write(f"Topic given: {t} \n")

history = " "
converse = Conversation()
fix = Fixer()
i = 1

print(f"Topic given: {t} \n")
while i <= 3:
    print(f"\n--- Round {i} ---")
    
    # Player 1's turn
    player1_response = converse.Chat(t, p1, history, "Player 1")
    print(f"\n[Player-1]: {player1_response}")
    history += f"\nPlayer 1: {player1_response}"
    
    # Player 2's turn
    player2_response = converse.Chat(t, p2, history, "Player 2")
    print(f"\n[Player-2]: {player2_response}")
    history += f"\nPlayer 2: {player2_response}"
    
    # Player 3's turn
    player3_response = converse.Chat(t, p3, history, "Player 3")
    print(f"\n[Player-3]: {player3_response}")
    history += f"\nPlayer 3: {player3_response}"
    
    # Player 4's turn
    player4_response = converse.Chat(t, p4, history, "Player 4")
    print(f"\n[Player-4]: {player4_response}")
    history += f"\nPlayer 4: {player4_response}"
    
    # Human Player's turn
    player5_input = input("Your turn (Player 5): ")
    player5_response = fix.fix(player5_input)
    print(f"\n[Player-5]: {player5_response}")
    history += f"\nPlayer 5: {player5_response}"
    
    i += 1

with open("output.txt", 'a', encoding='utf-8') as file:
    file.write("\n\n--- Final Conversation History ---\n")
    file.write(history)

# --- Voting Phase ---
print("\n--- Voting Phase ---")
detector = Detection()
votes_for_human = 0

# Each AI player votes
ai_players = {
    "Player 1": p1,
    "Player 2": p2,
    "Player 3": p3,
    "Player 4": p4
}

all_votes = ""

for player_name, personality in ai_players.items():
    vote_response = detector.Chat(t, personality, history, player_name)
    print(f"\n[{player_name}'s Vote]: {vote_response}")
    all_votes += f"\n[{player_name}'s Vote]: {vote_response}"
    
    # Use regex to find who they voted for
    match = re.search(r"\[Likely Human\]: (Player \d)", vote_response)
    if match:
        voted_player = match.group(1)
        if voted_player == "Player 5":
            votes_for_human += 1

with open("output.txt", 'a', encoding='utf-8') as file:
    file.write("\n\n--- Voting Results ---\n")
    file.write(all_votes)

# --- Game Outcome ---
print("\n--- Game Over ---")
if votes_for_human >= 2:
    print(f"\nResult: You were detected! ({votes_for_human} votes against you). You lose.")
    with open("output.txt", 'a', encoding='utf-8') as file:
        file.write("\n\nOutcome: Human Player Lost")
else:
    print(f"\nResult: You survived! ({votes_for_human} votes against you). You win!!!!!!!!!!!")
    with open("output.txt", 'a', encoding='utf-8') as file:
        file.write("\n\nOutcome: Human Player Won")
