import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        # Initialize the game window
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x400")
        self.root.attributes("-topmost", True)

        # Initialize player names, markers, and scores
        self.player1_name = ""
        self.player2_name = ""
        self.current_player = ""
        self.current_marker = "X"

        self.player1_score = 0
        self.player2_score = 0

        # Initialize variables for playing against the computer
        self.play_with_computer = False
        self.computer_marker = "O"

        # Initialize frames for different interfaces
        self.name_frame = None
        self.game_frame = None

        # Create the name input interface
        self.create_name_input_interface()

    def create_name_input_interface(self):
        """Create an interface for players to enter their names."""
        if self.name_frame:
            self.name_frame.destroy()

        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack()

        # Input for Player 1 name
        tk.Label(self.name_frame, text="Enter Player 1 Name:").pack()
        self.player1_entry = tk.Entry(self.name_frame)
        self.player1_entry.pack()

        # Option to play against the computer
        tk.Label(self.name_frame, text="Play against Computer?").pack()
        self.play_with_computer_var = tk.BooleanVar()
        self.play_with_computer_checkbox = tk.Checkbutton(self.name_frame, variable=self.play_with_computer_var)
        self.play_with_computer_checkbox.pack()

        # Button to start the game
        tk.Button(self.name_frame, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        """Start the game by collecting player names and determining game mode."""
        self.player1_name = self.player1_entry.get()
        self.play_with_computer = self.play_with_computer_var.get()

        # Ensure Player 1 name is entered
        if not self.player1_name:
            messagebox.showerror("Error", "Please enter a name for Player 1.")
            return

        # If not playing against the computer, get Player 2 name
        if not self.play_with_computer:
            self.create_player2_input_interface()
        else:
            self.player2_name = "Computer"
            self.name_frame.destroy()
            self.create_game_board()

    def create_player2_input_interface(self):
        """Create an interface for Player 2 to enter their name."""
        if self.name_frame:
            self.name_frame.destroy()

        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack()

        # Input for Player 2 name
        tk.Label(self.name_frame, text="Enter Player 2 Name:").pack()
        self.player2_entry = tk.Entry(self.name_frame)
        self.player2_entry.pack()

        # Button to start the game with Player 2
        tk.Button(self.name_frame, text="Start Game", command=self.start_game_with_player2).pack()

    def start_game_with_player2(self):
        """Start the game after Player 2 name is entered."""
        self.player2_name = self.player2_entry.get()
        if not self.player2_name:
            messagebox.showerror("Error", "Please enter a name for Player 2.")
            return

        self.name_frame.destroy()
        self.create_game_board()

    def create_game_board(self):
        """Create the game board for Tic Tac Toe."""
        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        # Initialize the buttons (3x3 grid) for the game board
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.game_frame, text="", font=("normal", 20), width=5, height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg="light yellow"
                )
                self.buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

        # Create a label to display the score
        self.create_score_label()
        self.update_score()

    def create_score_label(self):
        """Create and display the score label."""
        score_label_text = f"{self.player1_name}: {self.player1_score} | {self.player2_name}: {self.player2_score}"
        self.score_label = tk.Label(
            self.root, text=score_label_text, font=("normal", 16)
        )
        self.score_label.pack()

    def make_move(self, row, col):
        """Handle a player's move and update the game board."""
        # Only make a move if the selected cell is empty
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = self.current_marker

            # Change text color based on the marker
            if self.current_marker == "X":
                self.buttons[row][col]["fg"] = "red"
            elif self.current_marker == "O":
                self.buttons[row][col]["fg"] = "blue"

            # Check if the move results in a win
            if self.check_winner(row, col):
                winner = self.current_player
                if winner == self.player1_name:
                    self.player1_score += 1
                elif winner == self.player2_name:
                    self.player2_score += 1
                self.update_score()
                messagebox.showinfo("Winner!", f"{winner} wins!")

                # Highlight the winning squares
                self.highlight_winning_squares(row, col)

                # Ask if the players want to play again
                if self.ask_play_again():
                    self.reset_game()
                else:
                    self.show_final_score()
                    self.root.quit()

            # Check if the game is a tie
            elif self.check_tie():
                messagebox.showinfo("Tie!", "It's a tie!")

                if self.ask_play_again():
                    self.reset_game()
                else:
                    self.show_final_score()
                    self.root.quit()
            else:
                self.toggle_players()

                # If playing against the computer, let it make a move
                if self.play_with_computer and self.current_player == "Computer":
                    self.root.after(500, self.make_computer_move)

    def toggle_players(self):
        """Switch the current player and marker."""
        self.current_player = self.player1_name if self.current_player == self.player2_name else self.player2_name
        self.current_marker = "X" if self.current_marker == "O" else "O"

    def check_winner(self, row, col):
        """Check if the current move is a winning move."""
        marker = self.buttons[row][col]["text"]

        # Check the row for a win
        if all(self.buttons[row][c]["text"] == marker for c in range(3)):
            return True

        # Check the column for a win
        if all(self.buttons[r][col]["text"] == marker for r in range(3)):
            return True

        # Check diagonals for a win
        if row == col and all(self.buttons[i][i]["text"] == marker for i in range(3)):
            return True
        if row + col == 2 and all(self.buttons[i][2 - i]["text"] == marker for i in range(3)):
            return True

        return False

    def check_tie(self):
        """Check if the game is a tie."""
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def update_score(self):
        """Update the score label to reflect the current scores."""
        score_label_text = f"{self.player1_name}: {self.player1_score} | {self.player2_name}: {self.player2_score}"
        self.score_label.config(text=score_label_text)

    def ask_play_again(self):
        """Ask the players if they want to play another round."""
        response = messagebox.askyesno("Play Again?", "Do you want to continue?")
        return response

    def reset_game(self):
        """Reset the game board for a new round."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["fg"] = "black"  # Reset text color to black
                self.buttons[i][j]["bg"] = "light yellow"

        self.current_player = self.player1_name
        self.current_marker = "X"

    def make_computer_move(self):
        """Let the computer make a move."""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            random_row, random_col = random.choice(empty_cells)
            self.make_move(random_row, random_col)

    def highlight_winning_squares(self, row, col):
        """Highlight the winning squares on the game board."""
        marker = self.current_marker

        # Highlight the row
        if all(self.buttons[row][c]["text"] == marker for c in range(3)):
            for c in range(3):
                self.buttons[row][c]["bg"] = "#ffcccb" if marker == "X" else "#ADD8E6"

        # Highlight the column
        if all(self.buttons[r][col]["text"] == marker for r in range(3)):
            for r in range(3):
                self.buttons[r][col]["bg"] = "#ffcccb" if marker == "X" else "#ADD8E6"

        # Highlight diagonals
        if row == col and all(self.buttons[i][i]["text"] == marker for i in range(3)):
            for i in range(3):
                self.buttons[i][i]["bg"] = "#ffcccb" if marker == "X" else "#ADD8E6"
        if row + col == 2 and all(self.buttons[i][2 - i]["text"] == marker for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i]["bg"] = "#ffcccb" if marker == "X" else "#ADD8E6"

    def show_final_score(self):
        """Display the final score after the game ends."""
        final_score_message = f"Final Score:\n{self.player1_name}: {self.player1_score} | {self.player2_name}: {self.player2_score}"
        messagebox.showinfo("Game Over", final_score_message)

if __name__ == "__main__":
    # Create the main window and start the TicTacToe game
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
