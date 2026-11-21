

import random

def create_board():
    """Create an empty 3x3 board."""
    return [" " for _ in range(9)]

def display_board(board):
    """Display the board neatly in the console."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")
    print("Positions:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 \n")

def check_winner(board, symbol):
    """Check if the given symbol has 3 in a row, column, or diagonal."""
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == symbol:
            return True
    return False

def is_draw(board):
    """Return True if board is full and no one has won."""
    return " " not in board


def get_player_move(board, player_name, symbol):
    """Keep asking until a valid move is entered. Never crashes."""
    while True:
        move = input(f"{player_name} ({symbol}), enter position 1-9: ").strip()

        
        if move == "":
            print("You entered nothing! Please enter a number.")
            continue

        
        if not move.isdigit():
            print("Please enter a number only! Example: 5")
            continue

        pos = int(move)

        
        if pos < 1 or pos > 9:
            print("Please enter a number between 1 and 9 only!")
            continue

        
        if board[pos - 1] != " ":
            print(f"Cell {pos} is already filled! Try another cell.")
            continue

        return pos - 1

def get_computer_move(board, computer_symbol, player_symbol):
    """Simple AI: 1) Win if possible 2) Block player if they will win 3) Else random."""
    # 1. Try to win
    for i in range(9):
        if board[i] == " ":
            board[i] = computer_symbol
            if check_winner(board, computer_symbol):
                board[i] = " "
                return i
            board[i] = " "


    for i in range(9):
        if board[i] == " ":
            board[i] = player_symbol
            if check_winner(board, player_symbol):
                board[i] = " "
                return i
            board[i] = " "

    
    if board[4] == " ":
        return 4
    
    empty = [i for i in range(9) if board[i] == " "]
    return random.choice(empty)

def play_one_game(player1, symbol1, player2, symbol2, vs_computer):
    board = create_board()
    current_player = player1
    current_symbol = symbol1

    while True:
        display_board(board)
        print(f"Turn: {current_player} ({current_symbol})")

        
        if vs_computer and current_player == player2:
            print(f"{player2} is thinking...")
            move = get_computer_move(board, symbol2, symbol1)
            print(f"{player2} chose {move + 1}")
        else:
            move = get_player_move(board, current_player, current_symbol)

        board[move] = current_symbol

        
        if check_winner(board, current_symbol):
            display_board(board)
            print(f"🎉 {current_player} ({current_symbol}) WINS! 🎉")
            return current_player

        
        if is_draw(board):
            display_board(board)
            print("🤝 Game is a DRAW! 🤝")
            return "Draw"

        if current_player == player1:
            current_player = player2
            current_symbol = symbol2
        else:
            current_player = player1
            current_symbol = symbol1

def main():
    print("=" * 40)
    print("   TIC-TAC-TOE GAME - Python Mini Project")
    print("=" * 40)

    # Choose Mode - Bonus
    print("\nChoose Mode:")
    print("1. Two Player (Same Keyboard)")
    print("2. Single Player vs Computer")
    while True:
        mode = input("Enter 1 or 2: ").strip()
        if mode in ["1", "2"]:
            break
        print("Please enter 1 or 2 only!")

    vs_computer = (mode == "2")

    player1 = input("\nEnter Player 1 Name: ").strip() or "Player 1"
    while True:
        symbol1 = input(f"{player1}, choose your symbol (X / O): ").strip().upper()
        if symbol1 in ["X", "O"]:
            break
        print("Please enter X or O only!")

    symbol2 = "O" if symbol1 == "X" else "X"

    if vs_computer:
        player2 = "Computer"
        print(f"Computer will be {symbol2}")
    else:
        player2 = input("Enter Player 2 Name: ").strip() or "Player 2"

    # Score tally - Bonus
    scores = {player1: 0, player2: 0, "Draw": 0}

    while True:
        winner = play_one_game(player1, symbol1, player2, symbol2, vs_computer)
        scores[winner] += 1

        print("\n--- SCORE BOARD ---")
        print(f"{player1}: {scores[player1]} | {player2}: {scores[player2]} | Draw: {scores['Draw']}")
        print("-------------------")

        again = input("\nPlay Again? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing! Bye 👋")
            print(f"Final Score - {player1}: {scores[player1]}, {player2}: {scores[player2]}, Draw: {scores['Draw']}")
            break

if __name__ == "__main__":
    main()