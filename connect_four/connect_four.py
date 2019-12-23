"""Main module."""

import numpy as np
import click
import sys


class ConnectFourGame:
    """A class for storing the Connect Four game."""
    
    # Game parameters
    LINES = 6
    COLUMNS = 7
    CONNECT = 4
    
    def __init__(self, n_lines=LINES,
                       n_columns=COLUMNS,
                       n_connect=CONNECT):
        
        assert isinstance(n_lines, int), "Number of lines must be an integer"
        assert isinstance(n_columns, int), "Number of columns must be an integer"
        assert isinstance(n_connect, int), "Number of pieces to connect must be an integer"
        
        self.n_lines = n_lines
        self.n_columns = n_columns
        self.n_connect = n_connect
        
        self.reset_game()  # Sets game variables to initial state
    
    def __str__(self):
        char_matrix = ["  "+" ".join(map(str, 1+np.arange(self.n_columns)))+"  "
                       "\n+-" + "--"*self.n_columns + "+\n"]
        for l in range(self.n_lines):
            char_line = "| "
            for c in range(self.n_columns):
                square_state = self.state[l, c]
                if square_state == 1:
                    char_line += "o "
                elif square_state == 2:
                    char_line += "x "
                else:
                    char_line += "· "
            char_line += "|\n"
            char_matrix.append(char_line)
        char_matrix.append("+-" + "--"*self.n_columns + "+\n")        
        
        return "".join(char_matrix)
    
    def __repr__(self):
        return self.__str__()
    
    def check_win(self, player=None):
        """Checks whether there are 4 pieces of the same color in line."""
        
        if player is None:
            return self.check_win(player=1) or self.check_win(player=2)
        
        layers = np.arange(self.n_connect)
        
        # Check horizontal line
        h = self.n_columns - self.n_connect + 1
        win = np.any(np.all([self.state[:, i:i+h]==player for i in layers], axis=0))
        if win: return True
        
        # Check vertical line
        v = self.n_lines - self.n_connect + 1
        win = np.any(np.all([self.state[i:i+v, :]==player for i in layers], axis=0))
        if win: return True
        
        # Check first diagonal
        win = np.any(np.all([self.state[i:i+v, i:i+h]==player for i in layers], axis=0))
        if win: return True
        
        # Check second diagonal
        l = self.n_lines
        win = np.any(np.all([self.state[l-i-v:l-i, i:i+h]==player for i in layers], axis=0))
        if win: return True
         
        return False
    
    def possible_moves(self):
        """Returns a list with all the columns where a piece can still be placed."""
        return np.argwhere((self.state==0).sum(0) != 0).flatten() + 1
    
    def move(self, column_number):
        """Make a move in the game."""
        
        # If column is already complete, the play is invalid
        if column_number not in self.possible_moves():
            print("Selected column is complete. Move is invalid.")
            return self.state.copy(), self.done, self.winner
        
        # Determine where to place the piece
        current_column = self.state[:, column_number-1]
        empty_slot = (current_column==0).sum() - 1
        
        # Place the piece in the board
        self.state[empty_slot, column_number-1] = self.next_player
        
        # Determine whether the game is over and the next player
        if self.check_win(player=self.next_player):
            self.done = True
            self.winner = self.next_player
        elif (self.state == 0).sum() == 0:  # If the board is full
            self.done = True
            self.winner = 0
        self.next_player = 3 - self.next_player
        
        # Update game history
        self.history[self.num_moves] = column_number
        self.num_moves += 1
        
        return self#.state.copy(), self.done, self.winner
    
    def reset_game(self):
        """Reset the game to the initial state."""
        self.state = np.zeros([self.n_lines, self.n_columns])
        self.history = np.zeros(self.n_lines * self.n_columns, dtype=int)
        self.num_moves = 0
        self.next_player = 1
        self.done = False
        self.winner = None
        return self#.state.copy(), self.done, self.winner
        
    def set_game(self, history):
        """Set the game state from a given history vector."""
        self.reset_game()
        for move in history[history!=0]:
            self.move(move)
        return self#.state.copy(), self.done, self.winner
    
    def revert_move(self):
        """Reset the game state to that before the last move."""
        if self.num_moves == 0:
            print("Cannot revert the last move because there have been no moves.")
            return self.state.copy(), self.done, self.winner
        revert_history = self.history.copy()  # Create a history vector without the last move
        revert_history[self.num_moves-1] = 0
        return self.set_game(revert_history) # Set game history to reverted history


class HumanPlayer():
    def __init__(self):
        pass
    def play(self, game, execute_play=True, verbose=False):
        possible_choices = np.append(game.possible_moves(), -1).flatten()
        if verbose:
            click.echo("Current player: Player "+str(game.next_player))
            move = ask_for_prompt(choice_list=possible_choices,
                                  choice_name="Column", 
                                  error_message="Invalid choice! Please try again. ")
        choice = int(move)
        if execute_play:
            if choice == -1:
                game.revert_move()
            else:
                game.move(choice)
        return choice
    

class RandomPlayer():
    def __init__(self):
        pass
    def play(self, game, execute_play=True, verbose=False):
        choice = np.random.choice(game.possible_moves())
        if verbose:
            click.echo("Current player: Player "+str(game.next_player))
            click.echo("Column: "+str(choice))
        if execute_play:
            game.move(choice)
        return choice


def ask_for_choices(choice_list, 
                    choice_name="Choice", 
                    header="", 
                    error_message=""):
    """Print a list of options and ask to select one by number."""
    
    valid_choices = list(map(str, range(1, 1+len(choice_list))))
    options = list(choice_list.keys())
    prompt_return = False
    invalid_choice = False
    while not prompt_return:
        click.echo(header)
        for i, option in enumerate(options):
            click.echo(f" {i+1} - {choice_list[option]}")  # Print options
        if invalid_choice:
            prompt = f"{error_message}{choice_name}"
        else:
            prompt = choice_name
        prompt_return = click.prompt(prompt)  # Ask for an integer associated to an option
        if prompt_return not in valid_choices:
            invalid_choice = True
            prompt_return = False
            delete_last_lines(2+len(valid_choices))
        else:
            return options[int(prompt_return)-1]
    
    
def ask_for_prompt(choice_list, 
                   choice_name, 
                   error_message=""):
    """Prompt user for input from a given list of options."""
    
    valid_choices = list(map(str, choice_list))
    options = choice_list
    prompt_return = False
    invalid_choice = False
    while not prompt_return:
        if invalid_choice:
            prompt = f"{error_message}{choice_name}"
        else:
            prompt = choice_name
        prompt_return = click.prompt(prompt)
        if prompt_return not in valid_choices:
            invalid_choice = True
            prompt_return = False
            delete_last_lines(1)
        else:
            return prompt_return
    

def delete_last_lines(n=1):
    """Delete last n lines in the console output."""
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)