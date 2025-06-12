import random
import json
from datetime import datetime
from typing import List, Dict, Optional,Tuple
from sqlalchemy.orm import Session
from models import player, MonsterSpecies,PlayerMonster, Battle, Trade, Archivement,PlayerAchivement
from config import TYPE_EFFECTIVENESS, RARITY_WEIGHTS,BASE_CATCH_RATE_BONUS,BATTLE_EXP_MULTIPLIER,BUTTLE_MONEY_MULTIPLIER

from database import SessionLocal
class GameEngine:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.current_player: Optional[player] = None

     ##player management##
    def __delattr__(self):
        if hasattr(self, 'db'):
            self.db.close() 
    def create_player(self, username: str) -> player:
     #create a new player account

        player=player(username=username)
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
     #give a starter a monster
        self.give_starter_monster(player.id)
        return player
    def login_player(self, username: str) -> Optional[PlayerMonster]:
        player = self.db.query(player).filter(player.username == username).first()
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
        mx_hp = int(species.base_hp * level_multiplier)
        attack= int(species.base_attack * level_multiplier)
        defense = int(species.base_defense * level_multiplier)
        speed = int(species.base_speed * level_multiplier)
        monster = PlayerMonster(
            player_id=player_id,
            species_id=species_id,
            level=level,
            max_hp=mx_hp,
            attack=attack,
            defense=defense,
            speed=speed,
            expirence=0,
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
    
    def attempt_catch(self, player_id: int, species_id: int) -> bool:
        