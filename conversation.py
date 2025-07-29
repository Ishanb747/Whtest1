#conversation.py
from topic import Topic
from c import Conversation
from d import Detection
from fixer import Fixer
import re

T = Topic()
t = T.Generate()

with open("output.txt" , 'w') as file:
    file.write(f"Topic given: {t} \n")

p1 = "A highly rational thinker who dissects every topic with logic, structure, and precision. Rarely influenced by emotion, and always aims for clarity, consistency, and factual accuracy."

p2 = "Deeply empathetic and emotionally intelligent. Responds with personal insight, compassion, and an emphasis on human connection. Sees value in lived experiences and emotional truth."

p3 = "Witty, unpredictable, and a master of sarcasm. Approaches topics with humor, irony, and a touch of rebellion, often challenging norms in clever or unexpected ways."

p4 = "Endlessly curious and philosophically inclined. Loves asking questions more than giving answers. Explores multiple viewpoints and thrives in ambiguity and intellectual depth."




history = f" "

converse = Conversation()
fix = Fixer()
i = 1

print(f"Topic given: {t} \n")
while i <=5:
    player1 = converse.Chat(t , p1 , history , "Player 1")
    print(f"\n [Player-1] : {player1}")
    history += f"\n player-1 : {player1}"
    player2 = converse.Chat(t , p2 , history , "Player 2")
    print(f"\n [Player-2] : {player2}")
    history += f"\n player-2 : {player2}"
    player3 = converse.Chat(t , p3 , history , "Player 3")
    print(f"\n [Player-3] : {player3}")
    history += f"\n player-3 : {player3}"
    player4 = converse.Chat(t , p4 , history , "Player 4")
    print(f"\n [Player-4] : {player4}")
    history += f"\n player-4 : {player4}"
    player5 = input("  ")
    player5 = fix.fix(player5)
    print(f"\n [Player-5] : {player5}")
    history += f"\n player-5 : {player5}"
    i = i + 1

with open("output.txt", 'a', encoding='utf-8') as file:
    file.write(history)

detector = Detection()
votes = 0

player1 = detector.Chat(t , p1 , history , "Player 1")
match = re.search(r"\[Likely Human\]: (Player \d)", player1)
if match:
    voted_player = match.group(1)
    if voted_player == "Player 5":
        votes += 1
player2 = detector.Chat(t , p2 , history , "Player 2")
match = re.search(r"\[Likely Human\]: (Player \d)", player2)
if match:
    voted_player = match.group(1)
    if voted_player == "Player 5":
        votes += 1
player3 = detector.Chat(t , p3 , history , "Player 3")
match = re.search(r"\[Likely Human\]: (Player \d)", player3)
if match:
    voted_player = match.group(1)
    if voted_player == "Player 5":
        votes += 1
player4 = detector.Chat(t , p4 , history , "Player 4")
match = re.search(r"\[Likely Human\]: (Player \d)", player4)
if match:
    voted_player = match.group(1)
    if voted_player == "Player 5":
        votes += 1


with open("output.txt" , 'a') as file:
    file.write(f'\n [ Player 1 ] : {player1}')

with open("output.txt" , 'a') as file:
    file.write(f'\n [ Player 2 ] : {player2}')

with open("output.txt" , 'a') as file:
    file.write(f'\n [ Player 3 ] : {player3}')

with open("output.txt" , 'a') as file:
    file.write(f'\n [ Player 4 ] : {player4}')

if votes >= 2:
    print("\n You lose")
else:
    print("\n You win!!!!!!!!!!!")



