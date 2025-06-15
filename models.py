"""
Database Models - Partner A's Main Job!
This file defines what our monsters, players, and other game objects look like.
Think of this like creating the blueprint for Pokemon cards!
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# This is like the master template for all our database tables
Base = declarative_base()

class Player(Base):
    """
    This represents a trainer/player in our game.
    Like Ash Ketchum's trainer card!
    """
    __tablename__ = "players"
    
    # Basic player info
    id = Column(Integer, primary_key=True, index=True)  # Unique player ID
    username = Column(String, unique=True, index=True)  # Trainer name
    level = Column(Integer, default=1)                  # Trainer level
    experience = Column(Integer, default=0)             # Experience points
    money = Column(Integer, default=500)                # Starting money
    created_at = Column(DateTime, default=datetime.utcnow)  # When they joined
    
    # Relationships (connections to other tables)
    monsters = relationship("PlayerMonster", back_populates="owner")  # Their monsters
    battles_as_player1 = relationship("Battle", foreign_keys="Battle.player1_id", back_populates="player1")
    battles_as_player2 = relationship("Battle", foreign_keys="Battle.player2_id", back_populates="player2")
    trades_sent = relationship("Trade", foreign_keys="Trade.from_player_id", back_populates="from_player")
    trades_received = relationship("Trade", foreign_keys="Trade.to_player_id", back_populates="to_player")
    achievements = relationship("PlayerAchievement", back_populates="player")

    def __repr__(self):
        return f"<Player(username='{self.username}', level={self.level})>"

class MonsterSpecies(Base):
    """
    This is like the Pokedex entry for each monster type.
    It defines what a Pikachu or Charizard is like in general.
    """
    __tablename__ = "monster_species"
    
    # Basic species info
    id = Column(Integer, primary_key=True, index=True)   # Unique species ID
    name = Column(String, unique=True)                   # Monster name (like "Pikachu")
    type = Column(String)                                # Element type (Fire, Water, etc.)
    
    # Base stats (these are like the species' natural abilities)
    base_hp = Column(Integer)        # Health points
    base_attack = Column(Integer)    # Attack power
    base_defense = Column(Integer)   # Defense power
    base_speed = Column(Integer)     # Speed stat
    
    # Rarity and catching info
    rarity = Column(String)          # How rare this monster is
    description = Column(Text)       # Description of the monster
    catch_rate = Column(Float)       # How easy it is to catch (0.0 to 1.0)
    
    # Relationships
    player_monsters = relationship("PlayerMonster", back_populates="species")

    def __repr__(self):
        return f"<MonsterSpecies(name='{self.name}', type='{self.type}', rarity='{self.rarity}')>"

class PlayerMonster(Base):
    """
    This represents an individual monster that a player owns.
    Like YOUR specific Pikachu that you caught and trained.
    """
    __tablename__ = "player_monsters"
    
    # Basic monster info
    id = Column(Integer, primary_key=True, index=True)          # Unique monster ID
    player_id = Column(Integer, ForeignKey("players.id"))      # Who owns this monster
    species_id = Column(Integer, ForeignKey("monster_species.id"))  # What type of monster
    nickname = Column(String)                                   # Custom name (optional)
    level = Column(Integer, default=1)                          # Current level
    experience = Column(Integer, default=0)                     # Experience points
    
    # Current stats (these grow as the monster levels up)
    hp = Column(Integer)             # Current health
    max_hp = Column(Integer)         # Maximum health
    attack = Column(Integer)         # Current attack stat
    defense = Column(Integer)        # Current defense stat
    speed = Column(Integer)          # Current speed stat
    
    caught_at = Column(DateTime, default=datetime.utcnow)  # When you caught it
    
    # Relationships
    owner = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="player_monsters")

    def __repr__(self):
        return f"<PlayerMonster(species='{self.species.name}', level={self.level}, owner='{self.owner.username}')>"

# The rest of the tables (Battle, Trade, Achievement, etc.) are shared between both partners
# But Partner A focuses on the monster-related ones above

class Battle(Base):
    """Battle history tracking"""
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=True)  # Null for wild battles
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    battle_type = Column(String)  # "wild", "player", "gym"
    battle_data = Column(Text)    # JSON data about the battle
    experience_gained = Column(Integer, default=0)
    money_gained = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="battles_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="battles_as_player2")

    def __repr__(self):
        return f"<Battle(type='{self.battle_type}', winner_id={self.winner_id})>"

class Trade(Base):
    """Trading system between players"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    from_player_id = Column(Integer, ForeignKey("players.id"))
    to_player_id = Column(Integer, ForeignKey("players.id"))
    offered_monster_id = Column(Integer, ForeignKey("player_monsters.id"))
    requested_monster_id = Column(Integer, ForeignKey("player_monsters.id"))
    status = Column(String, default="pending")  # pending, accepted, rejected, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    from_player = relationship("Player", foreign_keys=[from_player_id], back_populates="trades_sent")
    to_player = relationship("Player", foreign_keys=[to_player_id], back_populates="trades_received")

    def __repr__(self):
        return f"<Trade(from={self.from_player.username}, to={self.to_player.username}, status='{self.status}')>"

class Achievement(Base):
    """Available achievements in the game"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    requirement_type = Column(String)  # "catch_count", "battle_wins", "collection_size", etc.
    requirement_value = Column(Integer)
    reward_money = Column(Integer, default=0)
    
    # Relationships
    player_achievements = relationship("PlayerAchievement", back_populates="achievement")

    def __repr__(self):
        return f"<Achievement(name='{self.name}', type='{self.requirement_type}')>"

class PlayerAchievement(Base):
    """Junction table for player achievements"""
    __tablename__ = "player_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="player_achievements")

    def __repr__(self):
        return f"<PlayerAchievement(player='{self.player.username}', achievement='{self.achievement.name}')>"