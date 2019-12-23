"""Console script for connect_four."""
import sys
import click
import connect_four
from connect_four import ConnectFourGame, RandomPlayer, HumanPlayer, ask_for_choices, ask_for_prompt, delete_last_lines
import numpy as np


@click.command()
def main(args=None):
    """Console script for playing Connect Four."""
    import sys
    
    mode_choices = {"ai": "Play against an AI",
                    "2player": "Two-player mode"
                    }
    ai_choices = {"random": "Random player",
                  }
    
    click.echo("Welcome to Connect Four!")
    
    # Select a 1-player or 2-player mode
    mode = ask_for_choices(mode_choices, 
                           choice_name="Mode", 
                           header="Please select a game mode:", 
                           error_message="Invalid choice! Please try again. ")
            
    # If 1-player, select an AI to play against
    if mode == "2player":
        player_1 = HumanPlayer()
        player_2 = HumanPlayer()
    if mode == "ai":
        ai = ask_for_choices(ai_choices, 
                             choice_name="AI choice", 
                             header="Please select an AI type to play against:", 
                             error_message="Invalid choice! Please try again. ")
        if ai == "random":
            ai_player = RandomPlayer()
            
        order = np.random.choice([1, 2])
        if order == 1:
            player_1 = HumanPlayer()
            player_2 = ai_player
        if order == 2:
            player_1 = ai_player
            player_2 = HumanPlayer()
        
    # Playing loop
    click.echo("\nInstructions:"+
               "\n - Select a number to place a piece in that column"+
               "\n - Use -1 to revert the last move"+
               "\n")
    game = ConnectFourGame()
    while not game.done:
        click.echo(game)
        if game.next_player == 1:
            next_player = player_1
        else:
            next_player = player_2
        
        next_player.play(game=game, verbose=True)
        delete_last_lines(12)
    click.echo(game)
    if game.winner != 0:
        click.echo("Game done! The winner is Player "+str(game.winner))
    else:
        click.echo("Game done. There was a tie.")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
