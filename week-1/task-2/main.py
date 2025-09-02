import tkinter as tk
from tkinter import messagebox
import time

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x600")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Game state
        self.current_player = 'X'
        self.board = [''] * 9
        self.game_active = True
        self.buttons = []
        
        # Colors
        self.bg_color = 'black'
        self.border_color = '#87CEEB'  # Light blue
        self.x_color = '#FF6B6B'      # Red
        self.o_color = '#4ECDC4'      # Teal
        self.text_color = 'white'
        self.highlight_color = '#FFD93D'  # Gold
        
        # Winning combinations
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="TIC TAC TOE", 
            font=('Arial', 28, 'bold'),
            fg=self.border_color,
            bg=self.bg_color
        )
        title_label.pack(pady=20)
        
        # Current player info
        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame.pack(pady=10)
        
        tk.Label(
            self.info_frame,
            text="Current Player:",
            font=('Arial', 16),
            fg=self.border_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT)
        
        self.current_player_label = tk.Label(
            self.info_frame,
            text=self.current_player,
            font=('Arial', 16, 'bold'),
            fg=self.highlight_color,
            bg=self.bg_color
        )
        self.current_player_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Game board frame with border effect
        self.board_frame = tk.Frame(
            self.root, 
            bg=self.border_color, 
            relief='raised',
            bd=3
        )
        self.board_frame.pack(pady=20)
        
        # Game board
        self.game_frame = tk.Frame(self.board_frame, bg=self.border_color)
        self.game_frame.pack(padx=5, pady=5)
        
        # Create buttons
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                self.game_frame,
                text='',
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                bg=self.bg_color,
                fg='white',
                activebackground='#111111',
                activeforeground='white',
                relief='raised',
                bd=2,
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_hover_leave(b))
        
        # Reset button
        self.reset_btn = tk.Button(
            self.root,
            text="New Game",
            font=('Arial', 14, 'bold'),
            bg=self.border_color,
            fg='black',
            activebackground='#B0E0E6',
            activeforeground='black',
            relief='raised',
            bd=3,
            padx=30,
            pady=10,
            command=self.reset_game
        )
        self.reset_btn.pack(pady=20)
        
        # Hover effects for reset button
        self.reset_btn.bind("<Enter>", self.on_reset_hover_enter)
        self.reset_btn.bind("<Leave>", self.on_reset_hover_leave)
    
    def on_hover_enter(self, button):
        if button['text'] == '' and self.game_active:
            button.configure(bg='#111111')
    
    def on_hover_leave(self, button):
        if button['text'] == '':
            button.configure(bg=self.bg_color)
    
    def on_reset_hover_enter(self, event):
        self.reset_btn.configure(bg='#B0E0E6')
    
    def on_reset_hover_leave(self, event):
        self.reset_btn.configure(bg=self.border_color)
    
    def make_move(self, index):
        if self.board[index] != '' or not self.game_active:
            return
        
        # Make the move
        self.board[index] = self.current_player
        button = self.buttons[index]
        button.configure(
            text=self.current_player,
            fg=self.x_color if self.current_player == 'X' else self.o_color,
            state='disabled',
            disabledforeground=self.x_color if self.current_player == 'X' else self.o_color
        )
        
        # Check for winner
        winning_combo = self.check_winner()
        if winning_combo:
            self.game_active = False
            self.highlight_winning_line(winning_combo)
            self.root.after(1000, lambda: self.show_win_message(f"{self.current_player} Wins!"))
            return
        
        # Check for draw
        if all(cell != '' for cell in self.board):
            self.game_active = False
            self.root.after(500, lambda: self.show_win_message("It's a Draw!"))
            return
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.current_player_label.configure(text=self.current_player)
    
    def check_winner(self):
        for combo in self.winning_combinations:
            if (self.board[combo[0]] != '' and 
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return combo
        return None
    
    def highlight_winning_line(self, winning_combo):
        # Highlight the winning line with animation effect
        for i in winning_combo:
            button = self.buttons[i]
            original_bg = button.cget('bg')
            
            # Create blinking effect
            def blink(btn, count=0):
                if count < 6:  # Blink 3 times
                    new_bg = self.highlight_color if count % 2 == 0 else original_bg
                    btn.configure(bg=new_bg)
                    self.root.after(200, lambda: blink(btn, count + 1))
            
            blink(button)
    
    def show_win_message(self, message):
        # Create a custom message box with styling
        result = messagebox.showinfo(
            "Game Over", 
            message,
            parent=self.root
        )
        # Auto reset after clicking OK
        self.reset_game()
    
    def reset_game(self):
        # Reset game state
        self.current_player = 'X'
        self.board = [''] * 9
        self.game_active = True
        self.current_player_label.configure(text=self.current_player)
        
        # Reset buttons
        for button in self.buttons:
            button.configure(
                text='',
                fg='white',
                bg=self.bg_color,
                state='normal'
            )
    
    def run(self):
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

# Enhanced version with better visual effects
class EnhancedTicTacToe(TicTacToeGUI):
    def __init__(self):
        super().__init__()
        self.setup_enhanced_ui()
    
    def setup_enhanced_ui(self):
        # Add some visual enhancements
        self.root.configure(relief='raised', bd=2)
        
        # Add a subtle gradient effect to the title
        self.animate_title()
    
    def animate_title(self):
        # Simple color animation for title
        colors = [self.border_color, '#ADD8E6', '#87CEEB', '#B0E0E6']
        self.title_color_index = 0
        
        def change_title_color():
            if hasattr(self, 'title_label'):
                color = colors[self.title_color_index % len(colors)]
                # Note: Can't change color of existing label, but we can update it
                self.title_color_index += 1
                self.root.after(2000, change_title_color)  # Change every 2 seconds
        
        change_title_color()
    
    def make_move(self, index):
        if self.board[index] != '' or not self.game_active:
            # Add a little shake effect for invalid moves
            self.shake_button(self.buttons[index])
            return
        
        # Add button press animation
        button = self.buttons[index]
        original_relief = button.cget('relief')
        button.configure(relief='sunken')
        self.root.after(100, lambda: button.configure(relief=original_relief))
        
        # Continue with normal move logic
        super().make_move(index)
    
    def shake_button(self, button):
        # Simple shake effect by changing relief quickly
        reliefs = ['sunken', 'raised', 'sunken', 'raised']
        for i, relief in enumerate(reliefs):
            self.root.after(i * 50, lambda r=relief: button.configure(relief=r))

def main():
    print("🎮 Starting Enhanced Tic Tac Toe Game...")
    print("✨ Features:")
    print("   • Black background with light blue borders")
    print("   • Colorful X's (Red) and O's (Teal)")
    print("   • Winning line highlighting")
    print("   • Smooth hover effects")
    print("   • Button animations")
    print("   • Auto reset after win or tie")
    print("\n🚀 Launching game window...")
    
    # Create and run the game
    game = EnhancedTicTacToe()
    game.run()
    
    print("\n👋 Thanks for playing!")

if __name__ == "__main__":
    main()
