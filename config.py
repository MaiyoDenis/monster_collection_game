"""
Game Configuration - Partner A's Settings File
This contains all the rules for how the game works.
Like the rulebook for Pokemon!
"""

import os

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///monster_game.db')

# Game balance settings (Partner A decides these!)
STARTER_MONEY = 500                    # How much money new players start with
HEAL_COST = 50                        # How much it costs to heal monsters
BASE_CATCH_RATE_BONUS = 0.02          # Catch rate improves by 2% per player level
BATTLE_EXP_MULTIPLIER = 25            # Base experience from battles
BATTLE_MONEY_MULTIPLIER = 10          # Base money from battles


# This is like the Pokemon type chart - what beats what
TYPE_EFFECTIVENESS = {
    "Fire": {
        "Grass": 2.0,      # Fire does 2x damage to Grass
        "Water": 0.5,      # Fire does 0.5x damage to Water  
        "Fire": 0.5        # Fire does 0.5x damage to other Fire
    },
    "Water": {
        "Fire": 2.0,       # Water beats Fire
        "Grass": 0.5,      # Water weak to Grass
        "Water": 0.5       # Water resists Water
    },
    "Grass": {
        "Water": 2.0,      # Grass beats Water
        "Fire": 0.5,       # Grass weak to Fire
        "Grass": 0.5       # Grass resists Grass
    },
    "Electric": {
        "Water": 2.0,      # Electric beats Water
        "Flying": 2.0,     # Electric beats Flying
        "Electric": 0.5,   # Electric resists Electric
        "Grass": 0.5       # Electric weak to Grass
    },
    "Rock": {
        "Fire": 2.0,       # Rock beats Fire
        "Flying": 2.0,     # Rock beats Flying
        "Water": 0.5,      # Rock weak to Water
        "Grass": 2.0       # Rock beats Grass
    },
    "Flying": {
        "Grass": 2.0,      # Flying beats Grass
        "Electric": 0.5,   # Flying weak to Electric
        "Rock": 0.5        # Flying weak to Rock
    },
}

# Higher numbers = more common
RARITY_WEIGHTS = {
    "Common": 50,      # Very common monsters
    "Uncommon": 30,    # Somewhat rare
    "Rare": 15,        # Pretty rare
    "Epic": 4,         # Very rare
    "Legendary": 1     # Extremely rare!
}

# Monster level progression (Partner A designs this!)
EXP_PER_LEVEL = 100              
PLAYER_EXP_PER_LEVEL = 200       # How much exp players need to level up
STAT_GROWTH_PER_LEVEL = 0.1      # Stats grow by 10% per level