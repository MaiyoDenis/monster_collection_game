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
            self._create_new_player()
        else:
            self._login_existing_player()


            #now lets tell the user how to play the game##
        console.print("\n 📖 use 'python monster_game.py --help' to see available commands.", style="blue")
    
    def _create_new_player(self):
        """Create a new player."""
        username_name = Prompt.ask("Enter your player name")
        existing_player=self.game.db.query(Player).filter(Player.username == username_name).first()
        if existing_player:
            console.print("❌ username already exists! Try logging in instead.", style="red")
            return
        player = self.game_engine.create_player(username_name)
        console.print(f"🎉 Player '{player.username}' created successfully!", style="green")
        console.print("💖You've been given a starter monster!", style="yellow")

        ##now let show the player their monster##
        starter= self.game.db.query(PlayerMonster).filter(PlayerMonster.player_id == player.id).first()
        if starter:
            console.print(f"🐾 Your starter monster is: {starter.species.name} (Level {starter.level})", style="blue")
        else:
            console.print("❗ No starter monster found. Please try again.", style="red")


    def _login_player(self):
        """Log in an existing player."""
        username_name = Prompt.ask("Enter your trainer name")
        player = self.game.login_player(username_name)
        if not player:
            console.print("❌ Player not found! Please create a new account.", style="red")
            return
        console.print(f"🎮 Welcome back , Trainer {username_name}!", style="green")
        
    def handle_explore(self, player_name: str):
        """Explore the game world."""
        player_obj = self.game_engine.login_player(player_name)
        if not player_obj:
            console.print("❌ Trainer not found! Please create a new account.", style="red")
            return
        console.print(f"\n🌲 {player_name} ventures into the wild...", style="green")
        console.print("🔍searching for wild monsters...", style="yellow")

        ##find the random wild monster##
        wild_species = self.game_engine.encounter_wild_monster()
        console.print(f"\n💫 A wild {wild_species.name} ({wild_species.type}-type, {wild_species.rarity}) appears!", style="bold cyan")
        console.print(f"📖{wild_species.description}", style="dim")
         
         ##ask what the player wants to do##
        action = Prompt.ask(
            "\nWhat do you want to do?",
            choices=["catch", "fight", "run"],
            default="catch"
        )
        if action == "catch":
            self._catch_monster(player_obj, wild_species)
        elif action == "fight":
            self._fight_monster(player_obj, wild_species)
        else:
            console.print("🏃‍♂️ You ran away safely!", style="green")

    def _attempt_catch(self, player_obj: Player, wild_species: MonsterSpecies) :
        """Attempt to catch a wild monster."""
        console.print(f"\n🎣 Attempting to catch {wild_species.name}...", style="yellow")

        ##lets show the player coool catch animation##
        for i in track(range(3), description="Throwing Monsterball..."):
            import time
            time.sleep(0.5)   ##lets wait for some time we make it realistic##
        success = self.game_engine.attempt_catch(player_obj.id, wild_species.id)
        if success:
            console.print(f"🎉 You caught {wild_species.name}!", style="green")
            console.print(f"💫 +50 Experience gained!", style="cyan")

            #cheaking for archivements##
            new_archivement = self.game_engine.check_archivement(player_obj.id,)
            for achievement in new_archivement:
                console.print(f"🏆 New achievement unlocked: {achievement.name}!", style="bold magenta")
                console.print(f"💰 Received ${achievement.reward_money}!", style="yellow")

        else:
            console.print(f"❌ Failed to catch {wild_species.name}.", style="red")
            console.print("💡Tip: Higher level trainers have a better catch rate!", style="dim")