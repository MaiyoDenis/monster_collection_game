"""
Database Setup and Monster Creation - Partner A's Big Job!
This file creates the database and fills it with all the monsters.
Like creating the entire Pokedex!
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, MonsterSpecies, Achievement
from config import DATABASE_URL

# Create the database connection
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Initialize database with tables and seed data - Partner A's main function!"""
    # Create all the tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have monsters (don't create duplicates)
    if db.query(MonsterSpecies).count() > 0:
        db.close()
        return
    
    # Create all the monsters! (Partner A's creative work)
    _seed_monster_species(db)
    
    # Create all the achievements
    _seed_achievements(db)
    
    # Save everything
    db.commit()
    db.close()

def _seed_monster_species(db):
    """
    Create all the monster species - Partner A's creative work!
    This is like filling out the Pokedex with all possible monsters.
    """
    species_data = [
        # ========== STARTER MONSTERS (Given to new players) ==========
        {
            "name": "Flamewyrm", 
            "type": "Fire", 
            "base_hp": 45, 
            "base_attack": 55, 
            "base_defense": 40, 
            "base_speed": 50, 
            "rarity": "Uncommon", 
            "catch_rate": 0.8,
            "description": "A fierce dragon with burning spirit. Its flames never go out!"
        },
        {
            "name": "Aquafin", 
            "type": "Water", 
            "base_hp": 50, 
            "base_attack": 45,
            "base_defense": 50, 
            "base_speed": 45, 
            "rarity": "Uncommon", 
            "catch_rate": 0.8,
            "description": "A graceful sea creature with healing powers. Can purify any water."
        },
        {
            "name": "Vinewhip", 
            "type": "Grass", 
            "base_hp": 55, 
            "base_attack": 40,
            "base_defense": 55, 
            "base_speed": 40, 
            "rarity": "Uncommon", 
            "catch_rate": 0.8,
            "description": "A nature spirit that controls plants. Makes flowers bloom instantly."
        },
        
        # ========== COMMON MONSTERS (Easy to find) ==========
        {
            "name": "Sparkbolt", 
            "type": "Electric", 
            "base_hp": 35, 
            "base_attack": 60,
            "base_defense": 30, 
            "base_speed": 65, 
            "rarity": "Common", 
            "catch_rate": 0.7,
            "description": "A quick electric creature that stores lightning in its fur."
        },
        {
            "name": "Rockgrinder", 
            "type": "Rock", 
            "base_hp": 70, 
            "base_attack": 50,
            "base_defense": 70, 
            "base_speed": 20, 
            "rarity": "Common", 
            "catch_rate": 0.6,
            "description": "A sturdy rock creature that can crush boulders with its fists."
        },
        {
            "name": "Windsoar", 
            "type": "Flying", 
            "base_hp": 40, 
            "base_attack": 50,
            "base_defense": 35, 
            "base_speed": 75, 
            "rarity": "Common", 
            "catch_rate": 0.65,
            "description": "A swift flying monster that rides the wind currents."
        },
        {
            "name": "Magmacrawl", 
            "type": "Fire", 
            "base_hp": 60, 
            "base_attack": 70,
            "base_defense": 50, 
            "base_speed": 30, 
            "rarity": "Common", 
            "catch_rate": 0.6,
            "description": "A slow but powerful lava creature. Leaves molten footprints."
        },
        {
            "name": "Frostbite", 
            "type": "Water", 
            "base_hp": 55, 
            "base_attack": 45,
            "base_defense": 60, 
            "base_speed": 35, 
            "rarity": "Common", 
            "catch_rate": 0.65,
            "description": "An icy water monster that can freeze anything it touches."
        },
        {
            "name": "Petalstorm", 
            "type": "Grass", 
            "base_hp": 50, 
            "base_attack": 55,
            "base_defense": 45, 
            "base_speed": 40, 
            "rarity": "Common", 
            "catch_rate": 0.65,
            "description": "Creates beautiful but dangerous petal tornadoes."
        },
        
        # ========== UNCOMMON MONSTERS (Harder to find) ==========
        {
            "name": "Thunderwing", 
            "type": "Electric", 
            "base_hp": 50, 
            "base_attack": 75,
            "base_defense": 45, 
            "base_speed": 80, 
            "rarity": "Uncommon", 
            "catch_rate": 0.4,
            "description": "Lightning-fast electric flyer that strikes like thunder."
        },
        {
            "name": "Ironshield", 
            "type": "Rock", 
            "base_hp": 85, 
            "base_attack": 60,
            "base_defense": 90, 
            "base_speed": 25, 
            "rarity": "Uncommon", 
            "catch_rate": 0.35,
            "description": "Nearly impenetrable defense. Its shell can deflect cannonballs."
        },
        {
            "name": "Leafstorm", 
            "type": "Grass", 
            "base_hp": 65, 
            "base_attack": 70,
            "base_defense": 60, 
            "base_speed": 55, 
            "rarity": "Uncommon", 
            "catch_rate": 0.4,
            "description": "Controls nature's fury. Can summon entire forests."
        },
        {
            "name": "Skyripper", 
            "type": "Flying", 
            "base_hp": 60, 
            "base_attack": 80,
            "base_defense": 50, 
            "base_speed": 85, 
            "rarity": "Uncommon", 
            "catch_rate": 0.4,
            "description": "Tears through the sky at incredible speeds."
        },
        
        # ========== RARE MONSTERS (Very hard to find) ==========
        {
            "name": "Voltdragon", 
            "type": "Electric", 
            "base_hp": 75, 
            "base_attack": 95,
            "base_defense": 70, 
            "base_speed": 90, 
            "rarity": "Rare", 
            "catch_rate": 0.2,
            "description": "A legendary electric dragon that commands all lightning."
        },
        {
            "name": "Crystalwing", 
            "type": "Rock", 
            "base_hp": 80, 
            "base_attack": 85,
            "base_defense": 100, 
            "base_speed": 45, 
            "rarity": "Rare", 
            "catch_rate": 0.15,
            "description": "Beautiful crystalline flying rock that refracts rainbows."
        },
        {
            "name": "Infernotail", 
            "type": "Fire", 
            "base_hp": 90, 
            "base_attack": 110,
            "base_defense": 60, 
            "base_speed": 70, 
            "rarity": "Rare", 
            "catch_rate": 0.18,
            "description": "Leaves trails of fire wherever it goes. Its tail burns hotter than lava."
        },
        {
            "name": "Tsunamicrest", 
            "type": "Water", 
            "base_hp": 85, 
            "base_attack": 95,
            "base_defense": 75, 
            "base_speed": 65, 
            "rarity": "Rare", 
            "catch_rate": 0.18,
            "description": "Can create massive tidal waves with a single roar."
        },
        
        # ========== EPIC MONSTERS (Extremely rare) ==========
        {
            "name": "Stormking", 
            "type": "Flying", 
            "base_hp": 100, 
            "base_attack": 120,
            "base_defense": 80, 
            "base_speed": 110, 
            "rarity": "Epic", 
            "catch_rate": 0.1,
            "description": "Ruler of the skies. Commands all weather and wind."
        },
        {
            "name": "Oceanlord", 
            "type": "Water", 
            "base_hp": 120, 
            "base_attack": 100,
            "base_defense": 100, 
            "base_speed": 80, 
            "rarity": "Epic", 
            "catch_rate": 0.08,
            "description": "Master of all waters. Can control every drop in the ocean."
        },
        {
            "name": "Forestsage", 
            "type": "Grass", 
            "base_hp": 110, 
            "base_attack": 90,
            "base_defense": 110, 
            "base_speed": 70, 
            "rarity": "Epic", 
            "catch_rate": 0.09,
            "description": "Ancient guardian of nature. Older than the oldest trees."
        },
        
        # ========== LEGENDARY MONSTERS (Almost impossible to find!) ==========
        {
            "name": "Megabolt", 
            "type": "Electric", 
            "base_hp": 120, 
            "base_attack": 140,
            "base_defense": 90, 
            "base_speed": 130, 
            "rarity": "Legendary", 
            "catch_rate": 0.05,
            "description": "The ultimate electric being. Said to have created lightning itself."
        },
        {
            "name": "Prismatic", 
            "type": "Rock", 
            "base_hp": 140, 
            "base_attack": 110,
            "base_defense": 150, 
            "base_speed": 60, 
            "rarity": "Legendary", 
            "catch_rate": 0.03,
            "description": "Reflects all colors of light. Its body contains every gem known to exist."
        },
    ]
    
    # Create each monster species and add to database
    for data in species_data:
        species = MonsterSpecies(**data)
        db.add(species)

def _seed_achievements(db):
    """Create all the achievements players can unlock"""
    achievements_data = [
        # Catching achievements
        {
            "name": "First Catch", 
            "description": "Catch your first monster",
            "requirement_type": "catch_count", 
            "requirement_value": 1, 
            "reward_money": 100
        },
        {
            "name": "Collector", 
            "description": "Catch 5 monsters",
            "requirement_type": "catch_count", 
            "requirement_value": 5, 
            "reward_money": 250
        },
        {
            "name": "Monster Master", 
            "description": "Catch 10 monsters",
            "requirement_type": "catch_count", 
            "requirement_value": 10, 
            "reward_money": 500
        },
        {
            "name": "Legendary Hunter", 
            "description": "Catch 20 monsters",
            "requirement_type": "catch_count", 
            "requirement_value": 20, 
            "reward_money": 1000
        },
        
        # Battle achievements
        {
            "name": "First Victory", 
            "description": "Win your first battle",
            "requirement_type": "battle_wins", 
            "requirement_value": 1, 
            "reward_money": 150
        },
        {
            "name": "Battle Veteran", 
            "description": "Win 10 battles",
            "requirement_type": "battle_wins", 
            "requirement_value": 10, 
            "reward_money": 300
        },
        {
            "name": "Champion", 
            "description": "Win 25 battles",
            "requirement_type": "battle_wins", 
            "requirement_value": 25, 
            "reward_money": 750
        },
        {
            "name": "Battle Master", 
            "description": "Win 50 battles",
            "requirement_type": "battle_wins", 
            "requirement_value": 50, 
            "reward_money": 1500
        },
        
        # Level achievements
        {
            "name": "Rising Star", 
            "description": "Reach level 5",
            "requirement_type": "player_level", 
            "requirement_value": 5, 
            "reward_money": 200
        },
        {
            "name": "Expert Trainer", 
            "description": "Reach level 10",
            "requirement_type": "player_level", 
            "requirement_value": 10, 
            "reward_money": 500
        },
        {
            "name": "Elite Trainer", 
            "description": "Reach level 15",
            "requirement_type": "player_level", 
            "requirement_value": 15, 
            "reward_money": 1000
        },
    ]
    
    # Create each achievement and add to database
    for data in achievements_data:
        achievement = Achievement(**data)
        db.add(achievement)

def get_db():
    """Get a database session (used by other parts of the game)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()