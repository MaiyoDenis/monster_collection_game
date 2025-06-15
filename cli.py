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
            self._login_player()


            #now lets tell the user how to play the game##
        console.print("\n 📖 use 'python monster_game.py --help' to see available commands.", style="blue")
    
    def _create_new_player(self):
        """Create a new player."""
        username_name = Prompt.ask("Enter your player name")
        existing_player=self.game_engine.db.query(Player).filter(Player.username == username_name).first()
        if existing_player:
            console.print("❌ username already exists! Try logging in instead.", style="red")
            return
        player = self.game_engine.create_player(username_name)
        console.print(f"🎉 Player '{player.username}' created successfully!", style="green")
        console.print("💖You've been given a starter monster!", style="yellow")

        ##now let show the player their monster##
        starter= self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id == player.id).first()
        if starter:
            console.print(f"🐾 Your starter monster is: {starter.species.name} (Level {starter.level})", style="blue")
        else:
            console.print("❗ No starter monster found. Please try again.", style="red")


    def _login_player(self):
        """Log in an existing player."""
        username_name = Prompt.ask("Enter your trainer name")
        player = self.game_engine.login_player(username_name)
        if not player:
            console.print("❌ Player not found! Please create a new account.", style="red")
            return
        console.print(f"🎮 Welcome back, Trainer {username_name}!", style="green")
        self.current_player = player
        
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
            self._attempt_catch(player_obj, wild_species)
        elif action == "fight":
            # The _fight_monster method does not exist, so simulate battle with first monster
            monsters = self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id == player_obj.id).all()
            if not monsters:
                console.print("❌ You have no monsters to fight with!", style="red")
                return
            chosen_monster = monsters[0]
            battle_result = self.game_engine.battle_wild_monster(chosen_monster)
            self._display_battle_result(battle_result)
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

            #checking for achievements##
        new_achievements = self.game_engine.check_achievements(player_obj.id)
        for achievement in new_achievements:
            console.print(f"🏆 New achievement unlocked: {achievement.name}!", style="bold magenta")
            console.print(f"💰 Received ${achievement.reward_money}!", style="yellow")

        else:
            console.print(f"❌ Failed to catch {wild_species.name}.", style="red")
            console.print("💡Tip: Higher level trainers have a better catch rate!", style="dim yellow")
    
    
    
    def handle_collection(self, Player:str):
        """Display the player's monster collection."""
        player_obj = self.game_engine.login_player(Player)
        if not player_obj:
            console.print("❌ Trainer not found! Please create a new account.", style="red")
            return
        ##checking all the monsters##
        monsters= self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id==player_obj.id).all()
        if not monsters:
            console.print("📭Your collection is empty! Go explore to catch some monsters!.", style="yellow")
            return

        self._display_collection(player_obj, monsters)
    def _display_collection(self, player:str, monsters: list):
        """Display the player's monster collection."""
        console.print(f"\n📚 {player.username}'s Monster Collection:", style="bold magenta")
        console.print("=" * 60, style="magenta")

        ##lets create a table to show the monsters##
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("Type", justify="center")
        table.add_column("Level", justify="right")
        table.add_column("HP", justify="center")
        table.add_column("Attack", justify="center")
        table.add_column("Defence", justify="center")
        table.add_column("Speed", justify="center")
        table.add_column("Rarity", style="yellow")

             ##lets add the monsters to the table##

        for monster in monsters:
          hp_display= f"{monster.hp}/{monster.max_hp}"
          table.add_row(
              str(monster.id),
              monster.species.name,
              monster.species.type,
              str(monster.level),
              hp_display,
              str(monster.attack),
              str(monster.defense),
              str(monster.speed),
              monster.species.rarity
          )
        console.print(table)
        console.print(f"\n📊 Total monsters: {len(monsters)}", style="blue")
    def handle_battle(self, player_name: str):
        """Start a battle with a wild monster."""
        player_obj = self.game_engine.login_player(player_name)
        if not player_obj:
            console.print("❌ Trainer not found! Please create a new account.", style="red")
            return
        
        ##get the player's monsters##
        monsters= self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id == player_obj.id).all()
        for m in monsters:
            console.print(f"Monster {m.species.name} HP: {m.hp}/{m.max_hp}")
        healthy_monsters = [m for m in monsters if m.hp > m.max_hp*0.1]
        if not healthy_monsters:
            console.print("💔 You have no healthy monsters to battle with!", style="red")
            console.print(f"🏥 use 'heal' command to restore your monsters!", style="yellow")

            return  
        
        #lets enable the player to choose a monster to battle with##
        chosen_monster=self._select_battle_monster(player_obj, healthy_monsters)
        if not chosen_monster:
           
            return  
        console.print("\n🥊🥊 ${chosen_monster.species.name} enters the battle arena!", style="green")

        ##now lets find a wild monster to battle with##start the battle##
        battle_result=self.game_engine.battle_wild_monster(chosen_monster)
        #lets show now what happens in thebattle##
        self._display_battle_result(battle_result,)
        ##check for new archivements##
        new_archivement = self.game_engine.check_achievements(player_obj.id)
        for achievement in new_archivement:
            console.print(f"🏆 New achievement unlocked: {achievement.name}!", style="bold magenta")
            console.print(f"💰 Received ${achievement.reward_money}!", style="yellow")
    
    def _select_battle_monster(self, player: Player, monsters: list) -> Optional[PlayerMonster]:
        """lets make the player choose a monster to battle with."""
        console.print(f"\n🗡️{player} enters the battle arena!", style="bold green")
        console.print(f"\n🦸‍♂️ {player.username}, choose a monster to battle with:", style="bold cyan")


         #show the player their monsters in a table##

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Choice", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("Type", style="cyan")
        table.add_column("Level", justify="center")
        table.add_column("HP", justify="center")
        table.add_column("Status")

        for i, monster in enumerate(monsters,1):
            hp_percent=monster.hp/monster.max_hp 
            satus="Excellent" if hp_percent > 0.7 else "Good" if hp_percent > 0.4 else "Injured"
            status_style = "green" if hp_percent  > 0.7 else "yellow" if hp_percent > 0.4 else "red"
            table.add_row(
                str(i),
                monster.species.name,
                monster.species.type,
                str(monster.level),
                f"{monster.hp}/{monster.max_hp}",
                f"[{status_style}]{satus}[/{status_style}]"
            )
        console.print(table)

        ##let them get their choice##
        try:
            choice = int(Prompt.ask("Enter the number of your choice")) - 1
            if  choice < 0 or choice >= len(monsters):
                console.print("❌ Invalid choice! Please try again.", style="red")
                return None
            return monsters[choice]
        except ValueError:
            console.print("❌ Invalid input! Please enter a valid number.", style="red")
            return None
    def _display_battle_result(self, battle_result: dict):
        ##show what hapened in the battle like riplay of the battle##
        console.print("\n"  + "=" * 60, style="bold")
        console.print("⚔️ BATTLE LOG ⚔️", style="bold red", justify="left")
        console.print("=" * 60, style="bold")
        #show each line of the buttle##
        for log_entry in battle_result.get('battle_log', []):
            if "victory" in log_entry:
                console.print(f"🏆 {log_entry}", style="bold green")
            elif "defeat" in log_entry:
                console.print(f"💔 {log_entry}", style="bold red")
            elif "Level Up" in log_entry:
                console.print(f"🎉 {log_entry}", style="bold yellow")
            elif "Turn" in log_entry:
                console.print(f"🔄 {log_entry}", style="bold cyan")
            elif "HP" in log_entry:
                console.print(f"💥 {log_entry}", style="bold magenta")
            else:
                console.print(f"📝 {log_entry}", style="dim")
        
        if battle_result.get('can_catch'):
            self.offer_catch_oppotunity(battle_result)

    def offer_catch_oppotunity(self, battle_result: dict):
        """Offer the player a chance to catch the wild monster after battle."""
        console.print("\n💫 The wild monster is weakened and ready to be caught!", style="bold yellow")
        if Confirm.ask("Do you want to attempt to catch it?"):
            wild_species = self.game_engine.db.query(MonsterSpecies).filter(MonsterSpecies.id == battle_result['wild_monster_id']).first()
            if not wild_species:
                console.print("🎯 Throwing Monsterball!", style="red")
                success=self.game_engine.attempt_catch(battle_result['player_id'], wild_species)
                if success:
                    console.print(f"🎉 You caught {wild_species.name}!", style="green")

                else:
                    console.print(f"❌ {wild_species.name} escaped!.", style="red")
                    
    #new player  vs player battle##

    def handle_pvp_battle(self, player_name:str,player2_name:str):
        """Start a player vs player battle."""
        player1 = self.game_engine.login_player(player_name)
        player2 = self.game_engine.login_player(player2_name)

        if not player1 or not player2:
            console.print("❌ One or both trainers not found! Please check the names.", style="red")
            return

       
        if player1.id == player2.id:
            console.print("❌ You cannot battle yourself! Please choose another trainer.", style="red")
            return
        
        p1_monsters=[m for m in player1.monsters if m.hp > m.max_hp * 0.1]
        p2_monsters=[m for m in player2.monsters if m.hp > m.max_hp * 0.1]
        if not p1_monsters or not p2_monsters:
            console.print("💔 One or both trainers have no healthy monsters to battle with!", style="red")
            return
        console.print(f"\n🤼‍♂️ {player1.username} vs {player2.username}!", style="bold cyan")


                 ##player 1 choose their monster##
        console.print(f"\n{player1.username}, choose your monster:", style="bold green")
        p1_choice= self._select_battle_monster(player1, p1_monsters)
        if not p1_choice:
            
            return 
        #player 2 choose their monster##
        console.print(f"\n{player2.username}, choose your monster:", style="bold green")
        p2_choice = self._select_battle_monster(player2, p2_monsters)
        if not p2_choice:
            return
        
        ###buttle coce now##
        # The GameEngine class does not have a pvp_battle method, so we need to implement or fix this call
        # For now, let's just simulate a simple battle result dictionary to avoid error
        battle_result = {
            'battle_log': [
                f"{p1_choice.species.name} attacks {p2_choice.species.name}!",
                f"{p2_choice.species.name} attacks {p1_choice.species.name}!",
                "Battle ended in a draw (simulation)."
            ],
            'can_catch': False
        }
        self._display_battle_result(battle_result)
        
    def handle_heal(self, player: str):   
        """Heal a player's monsters.""" 
        player_obj = self.game_engine.login_player(player)
        if not player_obj:
            console.print("❌ Trainer not found!", style="red")
            return

       
##lets see if they have enough money    ##
        if player_obj.money < HEAL_COST:
            console.print(f"💰 Insufficient funds! Healing costs ${HEAL_COST} but you only have ${player_obj.money}.", style="red")
            return
        



            ##take their money and heal monsters"##
        player_obj.money -= HEAL_COST
        self.game_engine.db.commit()

        self.game_engine.heal_all_monsters(player_obj.id)
        console.print(f"🏥 All your monsters have been healed to full HP!", style="green")
        console.print(f"💰 Paid ${HEAL_COST}. Remaining money: ${player_obj.money}",style="yellow")


    def handle_profile( self, player: str):
        """Display the player's profile."""
        player_obj = self.game_engine.login_player(player)
        if not player_obj:
            console.print("❌ Trainer not found! Please create a new account.", style="red")
            return
        # let's get all stats##
        stats=self.game_engine.get_player_stats(player_obj.id)

        ##profile card now##
        self._display_profile(stats)

        self._display_achievements(player_obj.id)
    def _display_profile(self, stats: dict):
        ##lets how a prety profile card##
        profile_content = f"""
        🆔Trainer: {stats['player'].username}
        📊Level:{stats['player'].level}
        ⭐Experience: {stats['player'].experience}/{stats['player'].next_level_experience}
        💰Money: ${stats['player'].money}
        📅Joined:{stats['player'].created_at.strftime('%Y-%m-%d')}
        📈Batle statistics
        🐾Monster Cought:{stats['total_monster']}
        ⚔️Total Battles:{stats['total_battles']}
        🏆Battles Won:{stats['wins']}
        📊Win Rate:{stats['win_rate']:.1f}%
        🎖️Archivements: {stats['archivements_count']}
        """
  


  ##Put it in a fancy box##
        profile=Panel(profile_content, title="🐉 Trainer Profile", border_style="bold blue", expand=False)
        console.print(Panel)
  
    def _display_achievements(self, player_obj: Player): 
        ##show  new archivements##
        from models import Achievement

        ##give 3 most archivements##
        recent_achievements = self.game_engine.db.query(Achievement).filter(Achievement.player_id == player_obj.id).order_by(Achievement.created_at.desc()).limit(3).all()
        if not recent_achievements:
            console.print("\n🏆Recent Achievements!", style="Bold yellow")
            for achievement in recent_achievements:
                console.print(f"  . {achievement.name} - {achievement.description}", style="Yellow")

    def handle_achievements(self, player: str):
        """Display the player's achievements."""
        player_obj = self.game_engine.login_player(player)
        if not player_obj:
            console.print("❌ Trainer not found! Please create a new account.", style="red")
            return
        
        from models import Achievement
        # get all the achievement men#
        all_achievements = self.game_engine.db.query(Achievement).all()
        # lets get the ones it already has##
        unlocked_ids=[pa.achievement_id for pa in player_obj.achievements]
        console.print(f"\n🏆Achievements progress for {player}:", style="bold yellow")
        console.print("=" * 60, style="yellow")

        # lets make a table to show the achievements##
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Achievement.id", style="dim")
        table.add_column("Description")
        table.add_column("Reward", justify="center")
        table.add_column("Status", justify="center")

        for achievement in all_achievements:
            # lets see if they have it##
            status = "✅Unlocked" if achievement.id in unlocked_ids else "🔒Locked"
            status_style = "green" if achievement.id in unlocked_ids else "red"
            table.add_row(
                achievement.name, 
                achievement.description, 
                f"${achievement.reward_money}",
                f"[{status_style}]{status}[/{status_style}]"
            )
        console.print(table)

        unlocked_count = len(unlocked_ids)
        total_count = len(all_achievements)
        progress = (unlocked_count / total_count * 100) if total_count > 0 else 0
        console.print(f"\n📊 progress: {unlocked_count}/{total_count} ({progress:.1f}%)", style="blue")

    def handle_trade(self, from_player: str, to_player: str):
        #handle trading monsters between players
        """Trade monsters between players."""
        from models import Trade
        # let's check if both players exist##
        player1 = self.game_engine.db.query(Player).filter(Player.username == from_player).first()
        player2 = self.game_engine.db.query(Player).filter(Player.username == to_player).first()
        if not player1:
            console.print(f"❌ Trainer '{from_player}' not found!.", style="red")
            return
        if not player2:
            console.print(f"❌ Trainer '{to_player}' not found!.", style="red")
            return
        
        if player1.id == player2.id:
            console.print("❌ You cannot trade with yourself! Please choose another trainer.", style="red")
            return
        
        # do the trading process##
        self.execute_trade(player1, player2)
    def execute_trade(self, player1: Player, player2: Player):
        #get both players' monsters##
        your_monsters = self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id == player1.id).all()
        their_monsters = self.game_engine.db.query(PlayerMonster).filter(PlayerMonster.player_id == player2.id).all()
        if not your_monsters or not their_monsters:
            console.print("❌ One or both trainers have no monsters to trade!", style="red")
            return
        
        if not their_monsters:
            console.print(f"❌ {player2.username} has no monsters to trade!", style="red")
            return
        
        console.print(f"\n🔄Proposing trade: {player1.username} ↔️ {player2.username}", style="bold cyan")
         
         #show both collections##
        self._display_trade_collections(your_monsters, their_monsters, player1.username, player2.username)
        ##handle actual trade##
        self._handle_trade_selection(player1, player2, your_monsters, their_monsters)
    def _display_trade_collections(self, your_monsters: list, their_monsters: list, player1_name: str, player2_name: str):
        """Display both players' monster collections for trading."""
        console.print(f"\n📦 {player1_name}'s Monsters:", style="bold green")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("ID", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("Type", style="cyan")
        table.add_column("Level", justify="center")
        table.add_column("Rarity", style="yellow")

        for monster in your_monsters:
            table.add_row(
                str(monster.id),
                monster.species.name,
                monster.species.type,
                str(monster.level),
                monster.species.rarity
            )
        console.print(table)

        console.print(f"\n📦 {player2_name}'s Monsters:", style="bold green")

        table2 = Table(show_header=True, header_style="bold green")
        table2.add_column("ID", style="dim")
        table2.add_column("Name", style="bold")
        table2.add_column("Type", justify="center")
        table2.add_column("Level", justify="right")
        table2.add_column("Rarity", justify="center")

        for monster in their_monsters:
            table2.add_row(
                str(monster.id),
                monster.species.name,
                monster.species.type,
                str(monster.level),
                monster.species.rarity
            )
        console.print(table2)

    def _handle_trade_selection(self, player1: Player, player2: Player, your_monsters: list, their_monsters: list):
        """Let the player select a monster to trade."""
        console.print(f"\n💡 In this demo,we will simulate an instant trade!", style="dim yellow")
         
        try:
            offered_id=int(Prompt.ask("Enter ID of monster you want to offer "))
            requested_id=int(Prompt.ask("Enter ID of monster you want to request"))

            #check if the monster exists and belong to the right players##
            offered_Monster=self.game_engine.db.query(PlayerMonster).filter(
                PlayerMonster.id==offered_id,
                PlayerMonster.player_id==player1.id
            ).first()

            requested_Monster = self.game_engine.db.query(PlayerMonster).filter(
                PlayerMonster.id==requested_id,
                PlayerMonster.player_id==player2.id
                ).first()
            
            if offered_Monster is None:
                console.print("❌ Invalid Monster ID from your collection!", style="red")
                return
            if requested_Monster is None:
                console.print("❌ Invalid Monster ID from their collection!", style="red")
                return
              


              #Simulate the other player response
            
            self._simulate_trade_response(player1,player2,offered_Monster,requested_Monster)
        except ValueError:
            console.print("❌ Invalid ID. Please enter a valid MOnster  IDs.", style="red")

    def _simulate_trade_response(self, player1: Player, player2: Player, offered_Monster: PlayerMonster, requested_monster: PlayerMonster):
        """Simulate the other player response.""" 
        console.print(f"\n🎲 Simulating {player2.username}'s response...", style="dim yellow")
        
        if random.random()<0.7:
            offered_Monster.player_id=player2.id
            requested_monster.player_id=player1.id

            #SAVE TRDE  IN DATA BASE##
            from models import Trade
            from datetime import datetime

            trade_record = Trade(from_player_id=player1.id,
                                to_player_id=player2.id,
                                offered_monster_id=offered_Monster.id,
                                requested_monster_id=requested_monster.id,
                                status="completed",
                                completed_at=datetime.utcnow()
                                )
            self.game_engine.db.add(trade_record)
            self.game_engine.db.commit()

            console.print("🎉 Trade successful!", style="bold green")
            console.print(f"📤 You gave: {offered_Monster.species.name} (Level {offered_Monster.level})", style="cyan")
            console.print(f"📥 You received: {requested_monster.species.name} (Level {requested_monster.level})", style="cyan")
        else:
            console.print(f"💔 {player2.username} declined the trade offer.", style="red")

    def handle_leaderboard(self):
        #show the to[ players##
        top_players=self.game_engine.db.query(Player).order_by(Player.level.desc(), Player.experience.desc()).limit(10).all()
        if not top_players:
            console.print("📭 No trainers found!", style="yellow")
            return
        
        console.print("\n🏆 Top Trainers Leaderboard", style="bold yellow")
        console.print("═" * 60, style="yellow")
        
        # Make a leaderboard table
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Rank", justify="center", style="bold")
        table.add_column("Trainer", style="bold cyan")
        table.add_column("Level", justify="center")
        table.add_column("Experience", justify="center")
        table.add_column("Monsters", justify="center")
        table.add_column("Battles Won", justify="center")
        
        from models import Battle
        
        for i, player in enumerate(top_players, 1):
            monster_count = len(player.monsters)
            battle_wins = self.game_engine.db.query(Battle).filter(Battle.winner_id == player.id).count()
            
            # Make top 3 players special colors
            rank_style = "gold" if i == 1 else "silver" if i == 2 else "orange" if i == 3 else "white"
            rank_symbol = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else str(i)
            
            table.add_row(
                f"[{rank_style}]{rank_symbol}[/{rank_style}]",
                player.username,
                str(player.level),
                str(player.experience),
                str(monster_count),
                str(battle_wins)
            )
        
        console.print(table)