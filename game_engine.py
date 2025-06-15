import random
import json
from datetime import datetime
from typing import List, Dict, Optional,Tuple
from sqlalchemy.orm import Session
from models import Player, MonsterSpecies, PlayerMonster, Battle, Trade, Achievement, PlayerAchievement
from config import TYPE_EFFECTIVENESS, RARITY_WEIGHTS, BASE_CATCH_RATE_BONUS, BATTLE_EXP_MULTIPLIER, BATTLE_MONEY_MULTIPLIER

from database import SessionLocal
class GameEngine:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.current_player: Optional[Player] = None

     ##player management##
    def __delattr__(self):
        if hasattr(self, 'db'):
            self.db.close() 
    def create_player(self, username: str) -> Player:
     #create a new player account

        player=Player(username=username)
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
     #give a starter a monster
        self.give_starter_monster(player.id)
        return player
    def login_player(self, username: str) -> Optional[PlayerMonster]:
        player = self.db.query(Player).filter(Player.username == username).first()
        if player:
            self.current_player = player
            return player
        return player
    def give_starter_monster(self, player_id: int) -> PlayerMonster:
        ##give player their first monster##
        starter_species = self.db.query(MonsterSpecies).filter(MonsterSpecies.name.in_(["Flamewyrn", "Aquafin", "Vinewhip"])).all() 
        if starter_species:
            chosen=random.choice(starter_species)
            self.create_player_monster(player_id, chosen.id, level=5,)

            # monster managment
    def create_player_monster(self, player_id: int, species_id: int, level: int =  1) -> PlayerMonster:
        species= self.db.query(MonsterSpecies).filter(MonsterSpecies.id == species_id).first()
        if not species:
            raise None
        level_multiplier = 1 + (level - 1) * 0.1
        max_hp = int(species.base_hp * level_multiplier)
        attack= int(species.base_attack * level_multiplier)
        defense = int(species.base_defense * level_multiplier)
        speed = int(species.base_speed * level_multiplier)
        monster = PlayerMonster(
            player_id=player_id,
            species_id=species_id,
            level=level,
            max_hp=max_hp,
            attack=attack,
            defense=defense,
            speed=speed,
            experience=0,
            hp=max_hp,  # Initialize current HP to max HP
        )
        self.db.add(monster)
        self.db.commit()
        self.db.refresh(monster)
        return monster
    def encounter_wild_monster(self) -> MonsterSpecies:
        #encounter a wild monster
        all_species = self.db.query(MonsterSpecies).all()
        weigheted_species = []
        for species in all_species:
            weight = RARITY_WEIGHTS.get(species.rarity, 1)
            weigheted_species.extend([species] * weight)
        return random.choice(weigheted_species)
    
    def attempt_catch(self, player_id: int, species) -> bool:
        """Attempt to catch a wild monster"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        
        # If species is an int (species id), fetch the MonsterSpecies object
        if isinstance(species, int):
            species = self.db.query(MonsterSpecies).filter(MonsterSpecies.id == species).first()
            if not species:
                return False
        
        # Calculate catch rate based on species rarity and player level
        base_rate = species.catch_rate
        level_bonus = player.level * BASE_CATCH_RATE_BONUS
        final_rate = min(base_rate + level_bonus, 0.95)
        
        success = random.random() < final_rate
        
        if success:
            # Create the monster for the player
            wild_level = max(1, player.level + random.randint(-2, 3))
            self.create_player_monster(player_id, species.id, wild_level)
            
            # Award experience and check achievements
            self.award_experience(player_id, 50)
            self.check_achievements(player_id)
        
        return success
    
    # Battle System
    def calculate_damage(self, attacker: PlayerMonster, defender_stats: Dict, move_power: int = 40) -> int:
        """Calculate battle damage"""
        # Base damage calculation
        attack_stat = attacker.attack
        defense_stat = defender_stats.get('defense', 30)
        level_factor = attacker.level / 50.0
        
        base_damage = ((2 * attacker.level + 10) / 250.0) * (attack_stat / defense_stat) * move_power + 2
        
        # Type effectiveness
        attacker_type = attacker.species.type
        defender_type = defender_stats.get('type', 'Normal')
        effectiveness = TYPE_EFFECTIVENESS.get(attacker_type, {}).get(defender_type, 1.0)
        
        # Random factor
        random_factor = random.uniform(0.85, 1.0)
        
        final_damage = int(base_damage * effectiveness * random_factor * level_factor)
        return max(1, final_damage)
    
    def battle_wild_monster(self, player_monster: PlayerMonster) -> Dict:
        """Battle against a wild monster"""
        wild_species = self.encounter_wild_monster()
        wild_level = max(1, player_monster.level + random.randint(-2, 2))
        
        # Create temporary wild monster stats
        level_multiplier = 1 + (wild_level - 1) * 0.1
        wild_stats = {
            'name': wild_species.name,
            'type': wild_species.type,
            'level': wild_level,
            'hp': int(wild_species.base_hp * level_multiplier),
            'max_hp': int(wild_species.base_hp * level_multiplier),
            'attack': int(wild_species.base_attack * level_multiplier),
            'defense': int(wild_species.base_defense * level_multiplier),
            'speed': int(wild_species.base_speed * level_multiplier),
        }
        
        battle_log = []
        battle_log.append(f"A wild {wild_species.name} (Level {wild_level}) appears!")
        
        player_hp = player_monster.hp
        wild_hp = wild_stats['hp']
        
        turn = 1
        while player_hp > 0 and wild_hp > 0:
            battle_log.append(f"\n--- Turn {turn} ---")
            
            # Determine turn order based on speed
            if player_monster.speed >= wild_stats['speed']:
                # Player goes first
                damage = self.calculate_damage(player_monster, wild_stats)
                wild_hp -= damage
                battle_log.append(f"{player_monster.species.name} attacks for {damage} damage!")
                
                if wild_hp > 0:
                    # Wild monster counter-attacks
                    damage = random.randint(10, 25)  # Simplified wild monster damage
                    player_hp -= damage
                    battle_log.append(f"Wild {wild_species.name} attacks for {damage} damage!")
            else:
                # Wild monster goes first
                damage = random.randint(10, 25)
                player_hp -= damage
                battle_log.append(f"Wild {wild_species.name} attacks for {damage} damage!")
                
                if player_hp > 0:
                    damage = self.calculate_damage(player_monster, wild_stats)
                    wild_hp -= damage
                    battle_log.append(f"{player_monster.species.name} attacks for {damage} damage!")
            
            battle_log.append(f"{player_monster.species.name} HP: {max(0, player_hp)}/{player_monster.max_hp}")
            battle_log.append(f"Wild {wild_species.name} HP: {max(0, wild_hp)}/{wild_stats['max_hp']}")
            
            turn += 1
            
            # Prevent infinite battles
            if turn > 20:
                battle_log.append("The battle lasted too long and both monsters retreated!")
                break
        
        # Determine winner and rewards
        won = player_hp > 0 and wild_hp <= 0
        
        if won:
            exp_gained = wild_level * BATTLE_EXP_MULTIPLIER + random.randint(10, 30)
            money_gained = wild_level * BATTLE_MONEY_MULTIPLIER + random.randint(5, 15)
            
            battle_log.append(f"\n🎉 Victory! You defeated the wild {wild_species.name}!")
            battle_log.append(f"Gained {exp_gained} experience and ${money_gained}!")
            
            # Award experience to monster and player
            player_monster.experience += exp_gained
            self.award_experience(player_monster.player_id, exp_gained // 2)
            self.award_money(player_monster.player_id, money_gained)
            
            # Check for level up
            if self.check_monster_level_up(player_monster):
                battle_log.append(f"🆙 {player_monster.species.name} leveled up to {player_monster.level}!")
            
            # Update monster HP
            player_monster.hp = max(1, player_hp)
            
            # Record battle
            self.record_battle(player_monster.player_id, None, player_monster.player_id, "wild", 
                             exp_gained, money_gained, json.dumps(wild_stats))
        else:
            battle_log.append(f"\n💔 Defeat! {player_monster.species.name} was defeated!")
            player_monster.hp = 1  # Don't let monsters faint completely
            
            # Record battle
            self.record_battle(player_monster.player_id, None, None, "wild", 0, 0, json.dumps(wild_stats))
        
        self.db.commit()
        
        return {
            'won': won,
            'battle_log': battle_log,
            'wild_monster': wild_stats,
            'can_catch': won and random.random() < 0.3  # 30% chance to catch after winning
        }
    
    def record_battle(self, player1_id: int, player2_id: Optional[int], winner_id: Optional[int], 
                     battle_type: str, exp_gained: int, money_gained: int, battle_data: str):
        """Record battle in database"""
        battle = Battle(
            player1_id=player1_id,
            player2_id=player2_id,
            winner_id=winner_id,
            battle_type=battle_type,
            experience_gained=exp_gained,
            money_gained=money_gained,
            battle_data=battle_data
        )
        self.db.add(battle)
        self.db.commit()
    
    # Progression System
    def check_monster_level_up(self, monster: PlayerMonster) -> bool:
        """Check if monster should level up"""
        exp_needed = monster.level * 100
        
        if monster.experience >= exp_needed:
            monster.level += 1
            monster.experience -= exp_needed
            
            # Increase stats
            stat_increase = random.randint(2, 5)
            monster.max_hp += stat_increase
            monster.hp += stat_increase  # Heal when leveling up
            monster.attack += random.randint(1, 3)
            monster.defense += random.randint(1, 3)
            monster.speed += random.randint(1, 3)
            
            # Check for evolution after level up
            self.check_monster_evolution(monster)
            
            return True
        return False

    def check_monster_evolution(self, monster: PlayerMonster):
        """Check if the monster can evolve at its current level"""
        # Define evolution levels and evolved species mapping
        evolution_map = {
            "Flamewyrm": {"level": 10, "evolves_to": "Flarelord"},
            "Aquafin": {"level": 10, "evolves_to": "Aquarion"},
            "Vinewhip": {"level": 10, "evolves_to": "Vinetitan"},
            # Add more species evolutions as needed
        }
        species_name = monster.species.name
        if species_name in evolution_map:
            evo_info = evolution_map[species_name]
            if monster.level >= evo_info["level"]:
                # Evolve monster
                new_species = self.db.query(MonsterSpecies).filter(MonsterSpecies.name == evo_info["evolves_to"]).first()
                if new_species:
                    monster.species_id = new_species.id
                    monster.species = new_species
                    # Update stats to new species base stats scaled by level
                    level_multiplier = 1 + (monster.level - 1) * 0.1
                    monster.max_hp = int(new_species.base_hp * level_multiplier)
                    monster.hp = monster.max_hp
                    monster.attack = int(new_species.base_attack * level_multiplier)
                    monster.defense = int(new_species.base_defense * level_multiplier)
                    monster.speed = int(new_species.base_speed * level_multiplier)
                    self.db.commit()
                    print(f"{species_name} evolved into {new_species.name}!")
    
    def export_collection_to_json(self, player_id: int, filepath: str) -> bool:
        """Export player's monster collection to a JSON file"""
        import json
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if not player:
            return False
        collection = []
        for monster in player.monsters:
            collection.append({
                "id": monster.id,
                "species": monster.species.name,
                "nickname": monster.nickname,
                "level": monster.level,
                "hp": monster.hp,
                "max_hp": monster.max_hp,
                "attack": monster.attack,
                "defense": monster.defense,
                "speed": monster.speed,
                "caught_at": monster.caught_at.isoformat()
            })
        try:
            with open(filepath, "w") as f:
                json.dump(collection, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting collection: {e}")
            return False
    
    def award_experience(self, player_id: int, amount: int):
        """Award experience to player"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        player.experience += amount
        
        # Check for player level up
        exp_needed = player.level * 200
        if player.experience >= exp_needed:
            player.level += 1
            player.experience -= exp_needed
        
        self.db.commit()
    
    def award_money(self, player_id: int, amount: int):
        """Award money to player"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        player.money += amount
        self.db.commit()
    
    def heal_all_monsters(self, player_id: int):
        """Heal all of player's monsters to full HP"""
        monsters = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == player_id).all()
        for monster in monsters:
            monster.hp = monster.max_hp
        self.db.commit()
    
    # Achievement System
    def check_achievements(self, player_id: int) -> List[Achievement]:
        """Check and unlock achievements, return newly unlocked ones"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        unlocked_achievements = [pa.achievement_id for pa in player.achievements]
        
        achievements = self.db.query(Achievement).all()
        newly_unlocked = []
        
        for achievement in achievements:
            if achievement.id in unlocked_achievements:
                continue
            
            should_unlock = False
            
            if achievement.requirement_type == "catch_count":
                catch_count = len(player.monsters)
                should_unlock = catch_count >= achievement.requirement_value
            elif achievement.requirement_type == "battle_wins":
                wins = self.db.query(Battle).filter(Battle.winner_id == player_id).count()
                should_unlock = wins >= achievement.requirement_value
            elif achievement.requirement_type == "player_level":
                should_unlock = player.level >= achievement.requirement_value
            
            if should_unlock:
                # Unlock achievement
                player_achievement = PlayerAchievement(
                    player_id=player_id,
                    achievement_id=achievement.id
                )
                self.db.add(player_achievement)
                
                # Award money
                player.money += achievement.reward_money
                newly_unlocked.append(achievement)
        
        self.db.commit()
        return newly_unlocked
    
    # Statistics and Data
    def get_player_stats(self, player_id: int) -> Dict:
        """Get comprehensive player statistics"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        
        total_monsters = len(player.monsters)
        total_battles = self.db.query(Battle).filter(
            (Battle.player1_id == player_id) | (Battle.player2_id == player_id)
        ).count()
        
        wins = self.db.query(Battle).filter(Battle.winner_id == player_id).count()
        win_rate = (wins / total_battles * 100) if total_battles > 0 else 0
        
        achievements_count = len(player.achievements)
        
        return {
            'player': player,
            'total_monsters': total_monsters,
            'total_battles': total_battles,
            'wins': wins,
            'win_rate': win_rate,
            'achievements_count': achievements_count
        }
    
    # Trading System
    def propose_trade(self, from_player_id: int, to_player_id: int, 
                     offered_monster_id: int, requested_monster_id: int) -> Trade:
        """Propose a trade between players"""
        trade = Trade(
            from_player_id=from_player_id,
            to_player_id=to_player_id,
            offered_monster_id=offered_monster_id,
            requested_monster_id=requested_monster_id,
            status="pending"
        )
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade
    
    def execute_trade(self, trade_id: int) -> bool:
        """Execute a completed trade"""
        trade = self.db.query(Trade).filter(Trade.id == trade_id).first()
        if not trade or trade.status != "accepted":
            return False
        
        # Get the monsters
        offered_monster = self.db.query(PlayerMonster).filter(
            PlayerMonster.id == trade.offered_monster_id
        ).first()
        requested_monster = self.db.query(PlayerMonster).filter(
            PlayerMonster.id == trade.requested_monster_id
        ).first()
        
        if not offered_monster or not requested_monster:
            return False
        
        # Swap ownership
        offered_monster.player_id = trade.to_player_id
        requested_monster.player_id = trade.from_player_id
        
        # Update trade status
        trade.status = "completed"
        trade.completed_at = datetime.utcnow()
        
        self.db.commit()
        return True