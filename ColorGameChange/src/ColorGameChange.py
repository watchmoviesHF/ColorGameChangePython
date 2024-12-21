import tkinter as tk
from tkinter import messagebox
import random

# Initialize variables
score = 0
hearts = 3
isPaused = False
topScores = []

# Create the main window
window = tk.Tk()
window.title("Color Change Button Game")
window.geometry("800x800")

# Create the score and hearts labels
scoreLabel = tk.Label(window, text="Score: 0", font=("Arial", 16))
scoreLabel.pack()

heartsLabel = tk.Label(window, text="Hearts: ♥♥♥", font=("Arial", 16))
heartsLabel.pack()

# Create the "Click" button
button = tk.Button(window, text="Click", font=("Times New Roman", 16), width=10, height=2, command=lambda: on_button_click())
button.pack()

# Create other buttons
newGameButton = tk.Button(window, text="New Game", command=lambda: new_game())
newGameButton.pack()

pauseButton = tk.Button(window, text="Pause", command=lambda: toggle_pause())
pauseButton.pack()

saveButton = tk.Button(window, text="Save", command=lambda: save_game())
saveButton.pack()

missedLabel = tk.Label(window, text="", font=("Arial", 14))
missedLabel.pack()

def on_button_click():
    global score
    if not isPaused:
        # Randomly reposition the button
        x = random.randint(100, 700)
        y = random.randint(100, 600)
        button.place(x=x, y=y)
        score += 1
        scoreLabel.config(text="Score: " + str(score))
        missedLabel.config(text="")
        
def on_mouse_click(event):
    global hearts
    if not button.winfo_containing(event.x_root, event.y_root):
        hearts -= 1
        heartsLabel.config(text="Hearts: " + "♥" * hearts)
        missedLabel.config(text="Missed!")
        missedLabel.place(x=event.x, y=event.y)
        
        if hearts == 0:
            end_game()

def new_game():
    global score, hearts, isPaused
    confirm = messagebox.askyesno("New Game", "Are you sure you want to start a new game?")
    if confirm:
        score = 0
        hearts = 3
        isPaused = False
        scoreLabel.config(text="Score: " + str(score))
        heartsLabel.config(text="Hearts: ♥♥♥")
        missedLabel.config(text="")
        button.place(x=100, y=100)  # Reset button position

def toggle_pause():
    global isPaused
    isPaused = not isPaused
    if isPaused:
        pauseButton.config(text="Resume")
    else:
        pauseButton.config(text="Pause")

def save_game():
    try:
        with open("game_save.txt", "w") as f:
            f.write(f"Score: {score}\nHearts: {hearts}")
        messagebox.showinfo("Save", "Game saved successfully.")
    except Exception as e:
        messagebox.showerror("Save Error", str(e))

def load_game():
    global score, hearts
    try:
        with open("game_save.txt", "r") as f:
            data = f.readlines()
            score = int(data[0].strip().split(": ")[1])
            hearts = int(data[1].strip().split(": ")[1])
            scoreLabel.config(text="Score: " + str(score))
            heartsLabel.config(text="Hearts: " + "♥" * hearts)
            messagebox.showinfo("Load", "Game loaded successfully.")
    except Exception as e:
        messagebox.showerror("Load Error", "No saved game found.")

def end_game():
    global score, hearts
    topScores.append(score)
    topScores.sort(reverse=True)
    
    leaderboard = "\nTop 3 Scores:\n"
    for i in range(min(3, len(topScores))):
        leaderboard += f"{i + 1}. {topScores[i]}\n"
    
    messagebox.showinfo("Game Over", f"Game Over! Your score: {score}\n{leaderboard}")
    score = 0
    hearts = 3
    scoreLabel.config(text="Score: 0")
    heartsLabel.config(text="Hearts: ♥♥♥")
    missedLabel.config(text="")

# Bind mouse click event to track missed clicks
window.bind("<Button-1>", on_mouse_click)

# Load saved game if available
load_game()

# Start the game
window.mainloop()
