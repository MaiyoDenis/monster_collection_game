##this is now my main file to the game,,,,its like the menu##
import os
import sys
import click
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cli import CLIinterface
from database import init_database

# Create an instance of CLIinterface
cli_interface = CLIinterface()

##cli helper##
@click.group()
def cli():
     init_database()
@cli.command()
def start():
    """Start the Monster Game."""
    cli_interface.handle_start()

@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def explore(player):
    """Explore the world and encounter wild monsters."""
    cli_interface.handle_explore(player)
@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def collection(player):
    """View your monster collection."""
    cli_interface.handle_collection(player)
@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def battle(player):
    """Engage in battles with wild monsters."""
    cli_interface.handle_battle(player)
@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def heal(player):
    """Heal your monsters at the Pokémon Center."""
    cli_interface.handle_heal(player)
@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def archivements(player):
    """View your achievements."""
    cli_interface.handle_archivements(player)
@cli.command()
@click.option('--player', prompt='Trainer name', help='your trainer name.')
def trade(from_player, to_player):
    """Trade monsters with other players."""
    cli_interface.handle_trade(from_player, to_player)

@cli.command()
def leaderboard():
    """View the leaderboard of top players."""
    cli_interface.handle_leaderboard()

    ##player vs player battle (my special addition)#
@cli.command()
@click.option('--player1', prompt='Trainer 1 name', help='Name of the first trainer.')
@click.option('--player2', prompt='Trainer 2 name', help='Name of the second trainer.')
def pvp_battle(player1, player2):
    """Engage in a player vs player battle."""
    cli_interface.handle_pvp_battle(player1, player2)

    #now i want it to run when someone starts the game##
if __name__ == '__main__':
    try:
        import click
        import rich
        import sqlalchemy
    except ImportError:
        print("⏳ Installing required packages...")
        os.system('pip install -r requarements.text')
        print("✅ Packages installed successfully.")
    cli()