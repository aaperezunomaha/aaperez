from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state
state = {
    "tiles": {},  
    "turn": 0,  
    "positions": [0, 0],  
    "riddle": None,
    "answer": None
}

# Riddles and answers
riddles = [
    ("What has keys but can't open locks?", "keyboard"),
    ("What runs but never walks?", "water"),
    ("What has a face and two hands but no arms or legs?", "clock"),
    ("What can travel around the world while staying in a corner?", "stamp"),
    ("What has a neck but no head?", "bottle"),
    ("What has keys but can't open locks?", "keyboard"),
    ("What runs but never walks?", "water"),
    ("What has a face and two hands but no arms or legs?", "clock"),
    ("What can travel around the world while staying in a corner?", "stamp"),
    ("What has a neck but no head?", "bottle"),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", "the letter m"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with the wind.", "echo"),
    ("The more of this there is, the less you see. What is it?", "darkness"),
    ("What is full of holes but still holds a lot of weight?", "sieve"),
    ("What gets wetter as it dries?", "towel")
]

def reset_game():
    global state
    state = {
        "tiles": {},
        "turn": 0,
        "positions": [0, 0],
        "riddle": None,
        "answer": None
    }

@app.route("/", methods=["GET"])
def game():
    message = ""
    current_turn = state["turn"]
    riddle = state["riddle"]
    if not riddle:
        state["riddle"], state["answer"] = random.choice(riddles)
        riddle = state["riddle"]

   
    current_player = "Player 1" if current_turn == 0 else "Player 2"

    return render_template("index.html",
        turn=current_turn,
        positions=state["positions"],
        riddle=riddle,
        message=message,
        current_player=current_player  
    )

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    correct = state["answer"].lower() == data['answer'].lower()
    if correct:
        state["positions"][state["turn"]] += 1
        message = "Correct! Moving forward."
    else:
        message = "Incorrect! Passing the turn."

    
    state["riddle"], state["answer"] = random.choice(riddles)

    # Switch turnSS
    state["turn"] = (state["turn"] + 1) % 2

    return jsonify({
        "message": message,
        "riddle": state["riddle"],
        "positions": state["positions"],
        "current_player": "Player 1" if state["turn"] == 0 else "Player 2" 
    })

@app.route('/restart', methods=['POST'])
def restart_game():
    reset_game()
    return jsonify({
        "message": "Game has been restarted. Good luck!",
        "riddle": state["riddle"],
        "positions": state["positions"],
        "current_player": "Player 1"  
    })

if __name__ == "__main__":
    reset_game()  
    app.run(debug=True)
