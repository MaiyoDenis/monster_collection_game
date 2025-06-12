import random
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import track
from rich import print as rprint

#getting the game brain interface now##
from game_engine import GameEngine
from database import init_database
from models import Player, PlayerMonster, MonsterSpecies
from config import HEAL_COST

console= Console()
class CLIInterface:
    def __init__(self):
        self.game_engine = GameEngine()

    def display_welcome(self):
        ##my game opening screen##
        """Display the welcome message."""
        console.print("\n 🐉 Welcome to the Monster collection Game! 🐉", style="bold magenta")
        console.print("=" * 50,style="magenta")   

    def handle_start(self):
        """Start the Monster Game."""
        self.display_welcome()

        choice = Prompt.ask(
            "\nChoose an option",
            choices=["new", "login"],
            default="new",
        )
        if choice == "new":

    def handle_explore(self, player: str):
        """Explore the world and encounter wild monsters."""
        console.print(f"[bold green]Exploring the world as {player}...[/bold green]")
        # Logic for exploring and encountering monsters
        # For now, just a placeholder
        console.print("You encountered a wild monster!")

    def handle_collection(self, player: str):
        """View your monster collection."""
        console.print(f"[bold blue]{player}'s Monster Collection:[/bold blue]")
        # Logic to display player's monsters
        monsters = self.game_engine.get_player_monsters(player)
        if not monsters:
            console.print("You have no monsters in your collection.")
            return
        table = Table(title="Monsters")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Level", style="green")
        for monster in monsters:
            table.add_row(str(monster.id), monster.species.name, str(monster.level))
        console.print(table)

    def handle_battle(self, player: str):
        """Engage in battles with wild monsters."""
        console.print(f"[bold red]{player} is ready for battle![/bold red]")
        # Logic for battling wild monsters
        # Placeholder logic
        console.print("You won the battle!")

    def handle_heal(self, player: str):
        """Heal your monsters at the Pokémon Center."""
        console.print(f"Healing {player}'s monsters...")
        cost = HEAL_COST * len(self.game_engine.get_player_monsters(player))
        if Confirm.ask(f"This will cost {cost} coins. Do you want to proceed?"):
            console.print(f"{player}'s monsters have been healed!")
            # Logic to heal monsters

    def handle_archivements(self, player: str):
        """View your achievements."""
        console.print(f"[bold yellow]{player}'s Achievements:[/bold yellow]")
        # Logic to display player's achievements
        achievements = self.game_engine.get_player_achievements(player)
        if not achievements:
            console.print("You have no achievements yet.")
            return
        table
