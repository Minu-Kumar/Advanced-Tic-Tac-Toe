# =========================================================
# IMPORT REQUIRED LIBRARIES
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
import os
from pygame import mixer

# =========================================================
# SOUND CONFIGURATION
# =========================================================

SOUND_PATH = r"C:\Users\HP\AppData\Local\Programs\Python\Python310\pythonproject\ribhavagrawal-you-lose-game-sound-230514.mp3"

mixer.init()

try:
    lose_sound = mixer.Sound(SOUND_PATH)
except:
    lose_sound = None

# =========================================================
# MAIN APPLICATION WINDOW
# =========================================================

root = tk.Tk()
root.title("TIC TAC TOE")
root.geometry("900x650")
root.configure(bg="#1a1a2e")

# =========================================================
# GLOBAL GAME VARIABLES
# =========================================================

player_name = tk.StringVar()
difficulty = tk.StringVar(value="Easy")

board = [""] * 9
buttons = []

player_score = 0
computer_score = 0
draw_score = 0

# =========================================================
# SCREEN MANAGEMENT
# =========================================================

def show_frame(frame):
    """Display the selected screen and hide all others."""
    for current_frame in (start_frame, game_frame_screen, dashboard_frame):
        current_frame.pack_forget()

    frame.pack(fill="both", expand=True)


# =========================================================
# SAVE PLAYER STATISTICS
# =========================================================

def save_score():
    global player_score, computer_score, draw_score

    name = player_name.get().strip()

    if not name:
        return

    rows = []

    if os.path.exists("scores.csv"):
        with open("scores.csv", "r", newline="") as file:
            rows = list(csv.reader(file))

    if not rows:
        rows.append(["Name", "Wins", "Losses", "Draws"])

    player_found = False

    for i in range(1, len(rows)):
        if rows[i][0].lower() == name.lower():
            rows[i] = [
                name,
                str(player_score),
                str(computer_score),
                str(draw_score)
            ]
            player_found = True
            break

    if not player_found:
        rows.append([
            name,
            str(player_score),
            str(computer_score),
            str(draw_score)
        ])

    with open("scores.csv", "w", newline="") as file:
        csv.writer(file).writerows(rows)


# =========================================================
# LOAD DASHBOARD DATA
# =========================================================

def load_dashboard():
    for item in tree.get_children():
        tree.delete(item)

    if os.path.exists("scores.csv"):
        with open("scores.csv", "r") as file:
            reader = csv.reader(file)

            next(reader, None)

            serial_no = 1

            for row in reader:
                tree.insert("", "end", values=(serial_no, *row))
                serial_no += 1


# =========================================================
# WINNING COMBINATIONS
# =========================================================

winning_patterns = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


# =========================================================
# CHECK WINNER
# =========================================================

def winner(board_state):

    for a, b, c in winning_patterns:

        if board_state[a] == board_state[b] == board_state[c] != "":
            return board_state[a]

    if "" not in board_state:
        return "Draw"

    return None


# =========================================================
# MINIMAX AI ALGORITHM
# =========================================================

def minimax(board_state, maximizing_player):

    result = winner(board_state)

    if result == "O":
        return 1

    if result == "X":
        return -1

    if result == "Draw":
        return 0

    if maximizing_player:

        best_score = -99

        for i in range(9):

            if board_state[i] == "":
                board_state[i] = "O"

                best_score = max(
                    best_score,
                    minimax(board_state, False)
                )

                board_state[i] = ""

        return best_score

    best_score = 99

    for i in range(9):

        if board_state[i] == "":
            board_state[i] = "X"

            best_score = min(
                best_score,
                minimax(board_state, True)
            )

            board_state[i] = ""

    return best_score


# =========================================================
# FIND BEST MOVE FOR COMPUTER
# =========================================================

def best_move():

    highest_score = -99
    best_position = 0

    for i in range(9):

        if board[i] == "":
            board[i] = "O"

            score = minimax(board, False)

            board[i] = ""

            if score > highest_score:
                highest_score = score
                best_position = i

    return best_position


# =========================================================
# COMPUTER TURN
# =========================================================

def computer_move():

    empty_positions = [
        index
        for index, value in enumerate(board)
        if value == ""
    ]

    if not empty_positions:
        return

    level = difficulty.get()

    if level == "Easy":
        move = random.choice(empty_positions)

    elif level == "Medium":
        move = (
            random.choice(empty_positions)
            if random.random() < 0.5
            else best_move()
        )

    else:
        move = best_move()

    board[move] = "O"

    buttons[move].config(
        text="O",
        bg="#ff6b6b"
    )

    end_check()


# =========================================================
# CHECK GAME RESULT
# =========================================================

def end_check():
    global player_score, computer_score, draw_score

    result = winner(board)

    if not result:
        return

    if result == "X":

        player_score += 1

        messagebox.showinfo(
            "Winner",
            f"{player_name.get()} Wins!"
        )

    elif result == "O":

        computer_score += 1

        if lose_sound:
            lose_sound.play()

        messagebox.showinfo(
            "Lost",
            "Computer Wins!"
        )

    else:

        draw_score += 1

        messagebox.showinfo(
            "Draw",
            "Match Draw"
        )

    lbl1.config(text=f"Player Wins: {player_score}")
    lbl2.config(text=f"Computer Wins: {computer_score}")
    lbl3.config(text=f"Draws: {draw_score}")

    save_score()


# =========================================================
# PLAYER TURN
# =========================================================

def click(index):

    if board[index] != "":
        return

    board[index] = "X"

    buttons[index].config(
        text="X",
        bg="#4ecdc4"
    )

    if winner(board):
        end_check()
    else:
        root.after(300, computer_move)


# =========================================================
# RESTART GAME
# =========================================================

def restart():
    global board

    board = [""] * 9

    for button in buttons:
        button.config(
            text="",
            bg="white"
        )
def start_game():
    if player_name.get().strip() == "":
        messagebox.showwarning(
            "Name Required",
            "Please enter your name first!"
        )
        return

    show_frame(game_frame_screen)        


# =========================================================
# START SCREEN
# =========================================================
start_frame = tk.Frame(root, bg="#1a1a2e")

tk.Label(
    start_frame,
    text="ADVANCED TIC TAC TOE",
    font=("Arial", 24, "bold"),
    fg="gold",
    bg="#1a1a2e"
).pack(pady=20)

# Name Label
tk.Label(
    start_frame,
    text="Enter Your Name",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#1a1a2e"
).pack(pady=5)

# Name Entry
tk.Entry(
    start_frame,
    textvariable=player_name,
    font=("Arial", 14),
    width=25
).pack(pady=10)

# Level Label
tk.Label(
    start_frame,
    text="Choose Level",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#1a1a2e"
).pack(pady=5)

# Difficulty Dropdown
ttk.Combobox(
    start_frame,
    textvariable=difficulty,
    values=["Easy", "Medium", "Hard"],
    state="readonly",
    width=22
).pack(pady=10)

# Start Button
tk.Button(
    start_frame,
    text="Start Game",
    font=("Arial", 14, "bold"),
    bg="#4ecdc4",
    fg="black",
    command=start_game
).pack(pady=20)

# =========================================================
# GAME SCREEN
# =========================================================

game_frame_screen = tk.Frame(root, bg="#0f3460")

tk.Label(
    game_frame_screen,
    textvariable=player_name,
    font=("Arial", 18, "bold"),
    fg="gold",
    bg="#0f3460"
).pack()

lbl1 = tk.Label(game_frame_screen, text="Player Wins: 0", fg="white", bg="#0f3460")
lbl1.pack()

lbl2 = tk.Label(game_frame_screen, text="Computer Wins: 0", fg="white", bg="#0f3460")
lbl2.pack()

lbl3 = tk.Label(game_frame_screen, text="Draws: 0", fg="white", bg="#0f3460")
lbl3.pack()

game_board = tk.Frame(game_frame_screen, bg="#0f3460")
game_board.pack(pady=20)

for i in range(9):

    button = tk.Button(
        game_board,
        width=5,
        height=2,
        font=("Arial", 22, "bold"),
        command=lambda i=i: click(i)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5
    )

    buttons.append(button)

tk.Button(
    game_frame_screen,
    text="Restart",
    command=restart,
    bg="green",
    fg="white"
).pack(pady=5)

tk.Button(
    game_frame_screen,
    text="Dashboard",
    command=lambda: (load_dashboard(), show_frame(dashboard_frame))
).pack(pady=5)

tk.Button(
    game_frame_screen,
    text="Quit",
    command=root.destroy,
    bg="red",
    fg="white"
).pack(pady=5)

# =========================================================
# DASHBOARD SCREEN
# =========================================================

dashboard_frame = tk.Frame(root, bg="#16213e")

tk.Label(
    dashboard_frame,
    text="Dashboard",
    font=("Arial", 20, "bold"),
    bg="#16213e",
    fg="white"
).pack(pady=10)

tree = ttk.Treeview(
    dashboard_frame,
    columns=("No", "Name", "Wins", "Losses", "Draws"),
    show="headings",
    height=15
)

for column in ("No", "Name", "Wins", "Losses", "Draws"):
    tree.heading(column, text=column)
    tree.column(column, width=120, anchor="center")

tree.pack(pady=10)

tk.Button(
    dashboard_frame,
    text="Back",
    command=lambda: show_frame(game_frame_screen)
).pack()

# =========================================================
# START APPLICATION
# =========================================================

show_frame(start_frame)
root.mainloop()
