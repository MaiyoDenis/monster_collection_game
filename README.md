# 🐉 Monster Collection CLI Game - Pair Programming Project

<div align="center">

[Python](https://img.shields.io/badge/Python-3.7+-blue.svg)(https://python.org)
[SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)(https://sqlalchemy.org)
[Rich](https://img.shields.io/badge/Rich-CLI-yellow.svg)(https://rich.readthedocs.io)
[License](https://img.shields.io/badge/License-Educational-purple.svg)(https://github.com)

**A comprehensive text-based monster collection game built through collaborative pair programming**

*Catch, Train, Battle, and Trade monsters in an immersive CLI experience*

**🎮 Quick Start: `python3 monster_game.py start`**

</div>

---

## 👥 **Meet the Development Team**

<table>
<tr>
<td align="center" width="50%">

### 🔧 **Partner A: Core Game Engine & Monster System**
**Nasra Mauli (Naasiro)**  
*"The Foundation Architect"*

[GitHub](https://img.shields.io/badge/GitHub-Nasra--Maulid-black?logo=github)(https://github.com/Nasra-Maulid)

**Repositories**: 114+ | **Focus**: Web Development & System Architecture

**Responsibilities:**
- 🗄️ Database architecture and ORM relationships
- 🐾 Monster species design and game balance  
- 📊 Collection management system
- 🎲 Catching mechanics and probability algorithms

</td>
<td align="center" width="50%">

### ⚔️ **Partner B: Battle System & Player Management**
**Denis Maiyo**  
*"The Experience Creator"*

[GitHub](https://img.shields.io/badge/GitHub-MaiyoDenis-black?logo=github)(https://github.com/MaiyoDenis)

**Repositories**: 61+ | **Focus**: AI & Full-Stack Development

**Responsibilities:**
- 🥊 Battle system and combat mechanics
- 👥 Player management and progression
- 🎨 CLI interface and user experience
- 🔄 Trading system and social features

</td>
</tr>
</table>

---

## 🎯 **Project Overview**

This Monster Collection CLI Game is a fully-featured text-based game inspired by Pokemon, built using pair programming methodology. Players can catch wild monsters, engage in turn-based battles, level up their creatures, trade with other players, and unlock achievements—all through a beautiful command-line interface.

---

## 🚀 **Quick Start Guide**

### **Installation**
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd monster_collection_game

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start your adventure!
python3 monster_game.py start
```

### **First Steps**
```bash
# Create your trainer account
python3 monster_game.py start

# Explore the wild for monsters
python3 monster_game.py explore --player nasra

# View your growing collection
python3 monster_game.py collection --player nasra

# Battle to gain experience
python3 monster_game.py battle --player nasra

# Check the leaderboard
python3 monster_game.py leaderboard
```

---

## 🎮 **Complete Command Reference**

### **Account Management**
```bash
python3 monster_game.py start                       # Create account or login
python3 monster_game.py profile --player nasra      # View trainer profile
python3 monster_game.py leaderboard                 # View top trainers
```

### **Monster Management** *(Nasra's Features)*
```bash
python3 monster_game.py explore --player nasra      # Encounter wild monsters
python3 monster_game.py collection --player nasra   # View monster collection
python3 monster_game.py heal --player nasra         # Heal all monsters ($50)
python3 monster_game.py achievements --player nasra # View achievement progress
```

### **Battle System** *(Denis's Features)*
```bash
python3 monster_game.py battle --player nasra                      # Fight wild monsters
python3 monster_game.py pvp --player1 nasra --player2 denis        # Player vs Player battles
```

### **Social Features** *(Denis's Features)*
```bash
python3 monster_game.py trade --from_player nasra --to_player denis # Trade monsters
```

---

## 🏗️ **Development Architecture**

### **File Structure & Ownership**
```
monster_collection_game/
├── 🔧 Core Foundation (Partner A - Nasra)
│   ├── models.py              # Database models & relationships
│   ├── database.py            # Setup & monster species creation
│   ├── config.py              # Game balance & type effectiveness
│   └── requirements.txt       # Project dependencies
│
├── ⚔️ User Experience (Partner B - Denis)
│   ├── cli.py                 # Rich CLI interface & interactions
│   ├── monster_game.py        # Main entry point & Click commands
│   └── game_engine.py         # Battle system & player management
│
├── 📚 Documentation (Collaborative)
│   └── README.md              # Comprehensive project documentation
│
└── 🗄️ Generated Files
    └── monster_game.db        # SQLite database (auto-created)
```

---

## 👩‍💻 **Partner A: Nasra Mauli's Contributions**

### **🔧 Core Game Engine & Monster System**

<table>
<tr>
<td width="30%">

**📁 Primary Files:**
- `models.py`
- `database.py` 
- `config.py`
- Part of `game_engine.py`

</td>
<td width="70%">

**🎯 Key Responsibilities:**
- ✨ **20+ Unique Monster Species** with balanced stats and rarities
- ⚖️ **Type Effectiveness System** (Fire > Grass > Water > Fire)
- 🎲 **Sophisticated Rarity System** (Common → Legendary)
- 🏗️ **Database Architecture** with 7 properly normalized tables

</td>
</tr>
</table>

#### **🔑 Nasra's Key Functions:**
```python
def catch_monster(player_id, species_id) -> bool
def level_up_monster(monster_id) -> dict
def get_player_collection(player_id) -> list
def calculate_catch_rate(species_rarity, player_level) -> float
def encounter_wild_monster() -> MonsterSpecies
def create_player_monster(player_id, species_id, level) -> PlayerMonster
```

#### **🎨 Nasra's Creative Design:**
- **Monster Species Creation**: 20+ unique creatures with lore and balanced stats
- **Rarity Distribution**: Common (50%) → Uncommon (30%) → Rare (15%) → Epic (4%) → Legendary (1%)
- **Type Chart Design**: 6 elemental types with strategic interactions
- **Economic Balance**: Catch rates, experience curves, and progression systems

---

## 👨‍💻 **Partner B: Denis Maiyo's Contributions**

### **⚔️ Battle System & Player Management**

<table>
<tr>
<td width="30%">

**📁 Primary Files:**
- `cli.py`
- `monster_game.py`
- Part of `game_engine.py`

</td>
<td width="70%">

**🎯 Key Responsibilities:**
- ⚔️ **Advanced Turn-based Combat** with speed calculations
- 🆚 **Player vs Player Battles** (bonus innovation)
- 🎨 **Rich CLI Interface** with colorful tables and animations
- 📊 **Player Statistics** and leaderboard systems

</td>
</tr>
</table>

#### **🔑 Denis's Key Functions:**
```python
def create_battle(player1_id, player2_id, monster_teams) -> dict
def execute_turn(battle_id, attacker_monster, defender_monster, move) -> dict
def calculate_damage(attacker_stats, defender_stats, move_power, type_effectiveness) -> int
def battle_players(player1_monster, player2_monster) -> dict
def propose_trade(from_player, to_player, offered_monsters, requested_monsters)
def get_player_stats(player_id) -> dict
```

#### **🚀 Denis's Innovations:**
- **Combat Mechanics**: Sophisticated damage calculations with type effectiveness
- **User Experience**: Rich CLI with progress bars, colored output, and intuitive navigation
- **Social Features**: Trading system and competitive leaderboards
- **PvP System**: Real-time player vs player battle mechanics

---

## 🗄️ **Database Design Excellence**

### **Schema Overview (7 Tables)**
```sql
players              # Player accounts and progression (Nasra)
monster_species      # Monster templates and base stats (Nasra)
player_monsters      # Individual monster instances (Nasra)
battles              # Battle history and results (Denis)
trades               # Trading system between players (Denis)
achievements         # Available achievements (Collaborative)
player_achievements  # Player achievement progress (Collaborative)
```

### **Database Diagram**
Copy this into [dbdiagram.io](https://dbdiagram.io) to visualize:

```sql
Table players {
  id integer [pk, increment]
  username varchar [unique, not null]
  level integer [default: 1]
  experience integer [default: 0]
  money integer [default: 500]
  created_at timestamp [default: 'now()']
}

Table monster_species {
  id integer [pk, increment]
  name varchar [unique, not null]
  type varchar [not null]
  base_hp integer [not null]
  base_attack integer [not null]
  base_defense integer [not null]
  base_speed integer [not null]
  rarity varchar [not null]
  description text
  catch_rate float
}

Table player_monsters {
  id integer [pk, increment]
  player_id integer [ref: > players.id, not null]
  species_id integer [ref: > monster_species.id, not null]
  nickname varchar
  level integer [default: 1]
  experience integer [default: 0]
  hp integer [not null]
  max_hp integer [not null]
  attack integer [not null]
  defense integer [not null]
  speed integer [not null]
  caught_at timestamp [default: 'now()']
}

// Additional tables for battles, trades, achievements...
```

---

## 🎨 **Monster Species Showcase**

### **Starter Monsters** *(Nasra's Design)*
<table>
<tr>
<th>Monster</th>
<th>Type</th>
<th>Rarity</th>
<th>Description</th>
<th>Stats (HP/ATK/DEF/SPD)</th>
</tr>
<tr>
<td>🔥 Flamewyrm</td>
<td>Fire</td>
<td>Uncommon</td>
<td>A fierce dragon with burning spirit</td>
<td>45/55/40/50</td>
</tr>
<tr>
<td>💧 Aquafin</td>
<td>Water</td>
<td>Uncommon</td>
<td>A graceful sea creature with healing powers</td>
<td>50/45/50/45</td>
</tr>
<tr>
<td>🌿 Vinewhip</td>
<td>Grass</td>
<td>Uncommon</td>
<td>A nature spirit that controls plants</td>
<td>55/40/55/40</td>
</tr>
</table>

### **Type Effectiveness Chart** *(Nasra's Balance Design)*
```
🔥 Fire    →  🌿 Grass   (2x damage) | ← 💧 Water   (0.5x damage)
💧 Water   →  🔥 Fire    (2x damage) | ← 🌿 Grass   (0.5x damage)
🌿 Grass   →  💧 Water   (2x damage) | ← 🔥 Fire    (0.5x damage)
⚡ Electric →  💧 Water, 🪶 Flying (2x) | ← 🌿 Grass   (0.5x damage)
🪨 Rock    →  🔥 Fire, 🪶 Flying (2x) | ← 💧 Water   (0.5x damage)
🪶 Flying  →  🌿 Grass   (2x damage) | ← ⚡ Electric, 🪨 Rock (0.5x)
```

---

## 🎪 **Gameplay Demonstration**

### **Demo Script for Evaluation (5-10 minutes)**

#### **Phase 1: Setup (1 minute)**
```bash
# Create two trainer accounts
python3 monster_game.py start
> Choose: new | Trainer name: nasra

python3 monster_game.py start  
> Choose: new | Trainer name: denis
```

#### **Phase 2: Collection (2 minutes)**
```bash
# Nasra catches multiple monsters
python3 monster_game.py explore --player nasra
# Repeat 3+ times for variety

# Show collection with Rich table formatting
python3 monster_game.py collection --player nasra
```

#### **Phase 3: Battle System (2 minutes)**
```bash
# Wild monster battle (demonstrates Denis's combat system)
python3 monster_game.py battle --player nasra

# Player vs Player battle (Denis's bonus feature)
python3 monster_game.py pvp --player1 nasra --player2 denis
```

#### **Phase 4: Trading & Social (1 minute)**
```bash
# Execute monster trade (Denis's trading system)
python3 monster_game.py trade --from_player nasra --to_player denis
```

#### **Phase 5: Progress Systems (1 minute)**
```bash
# Show comprehensive stats and achievements
python3 monster_game.py profile --player nasra
python3 monster_game.py achievements --player nasra
python3 monster_game.py leaderboard
```

---

## 🏆 **Achievement System**

### **Catching Achievements** *(Nasra's Domain)*
- 🥉 **First Catch** - Catch your first monster → *$100*
- 🥈 **Collector** - Catch 5 monsters → *$250*
- 🥇 **Monster Master** - Catch 10 monsters → *$500*
- 👑 **Legendary Hunter** - Catch 20 monsters → *$1000*

### **Battle Achievements** *(Denis's Domain)*
- ⚔️ **First Victory** - Win your first battle → *$150*
- 🛡️ **Battle Veteran** - Win 10 battles → *$300*
- 🏆 **Champion** - Win 25 battles → *$750*
- 👑 **Battle Master** - Win 50 battles → *$1500*

### **Progression Achievements** *(Collaborative)*
- ⭐ **Rising Star** - Reach level 5 → *$200*
- 🌟 **Expert Trainer** - Reach level 10 → *$500*
- ✨ **Elite Trainer** - Reach level 15 → *$1000*

---

## 🧪 **Testing Checklist**

| Feature | Status | Partner | Test Command |
|---------|--------|---------|--------------|
| ✅ Player creation and login | Working | Denis | `python3 monster_game.py start` |
| ✅ Monster catching mechanics | Working | Nasra | `python3 monster_game.py explore --player nasra` |
| ✅ Battle system (turns, damage, types) | Working | Denis | `python3 monster_game.py battle --player nasra` |
| ✅ Trading between players | Working | Denis | `python3 monster_game.py trade --from_player nasra --to_player denis` |
| ✅ Achievement tracking | Working | Both | `python3 monster_game.py achievements --player nasra` |
| ✅ Data persistence (database) | Working | Nasra | Check `monster_game.db` creation |
| ✅ CLI commands and navigation | Working | Denis | All commands with `--help` |
| ✅ Error handling | Working | Both | Invalid inputs handled gracefully |

---

## 🔧 **Technical Deep Dive**

### **Nasra's Technical Excellence (Partner A)**
```python
# Sophisticated catch rate calculation
def calculate_catch_rate(species_rarity: str, player_level: int) -> float:
    base_rates = {
        "Common": 0.7, "Uncommon": 0.5, "Rare": 0.3, 
        "Epic": 0.15, "Legendary": 0.05
    }
    level_bonus = player_level * 0.02  # 2% per level
    return min(base_rates[species_rarity] + level_bonus, 0.95)

# Dynamic monster stat generation
def create_player_monster(self, player_id: int, species_id: int, level: int):
    level_multiplier = 1 + (level - 1) * 0.1
    stats = {
        'hp': int(species.base_hp * level_multiplier),
        'attack': int(species.base_attack * level_multiplier),
        # ... sophisticated stat scaling
    }
```

### **Denis's Technical Innovation (Partner B)**
```python
# Advanced battle damage calculation
def calculate_damage(self, attacker: Monster, defender_stats: Dict) -> int:
    base_damage = ((2 * attacker.level + 10) / 250.0) * \
                  (attacker.attack / defender_stats['defense']) * move_power + 2
    
    # Type effectiveness integration
    effectiveness = TYPE_EFFECTIVENESS.get(attacker.species.type, {}) \
                   .get(defender_stats['type'], 1.0)
    
    return int(base_damage * effectiveness * random_factor)

# Rich CLI with real-time feedback
def _display_battle_results(self, battle_result: dict):
    for log_entry in battle_result['battle_log']:
        if "Victory!" in log_entry:
            console.print(log_entry, style="bold green")
        elif "Turn" in log_entry:
            console.print(log_entry, style="bold blue")
```

---

## 🌟 **Collaboration Highlights**

### **Perfect Role Division**
- **Nasra (Partner A)**: Built the game's foundation - monsters, database, core mechanics
- **Denis (Partner B)**: Created the player experience - battles, interface, social features

### **Seamless Integration**
- **Shared Interfaces**: Both partners' code works together through well-defined APIs
- **Complementary Skills**: Nasra's system architecture + Denis's user experience design
- **Balanced Workload**: Equal complexity and responsibility distribution

### **Innovation Beyond Requirements**
- **Rich CLI Interface**: Professional-grade user experience (Denis)
- **Advanced Battle System**: PvP battles not in original spec (Denis)
- **Comprehensive Monster Design**: 20+ species with lore and balance (Nasra)
- **Economic System**: Money, healing costs, achievement rewards (Collaborative)

---

## 🚀 **Future Roadmap**

### **Potential Expansions**
- 🧬 **Monster Evolution** system with transformation chains
- 🥚 **Breeding Mechanics** for genetic combinations  
- 🏟️ **Gym Leader Battles** with themed challenges
- 🌍 **Multiple Regions** with unique monster species
- 📱 **Web Interface** adaptation
- 🌐 **Multiplayer Server** for real-time battles

### **Technical Roadmap**
- 🔄 **Real-time Trading** notifications
- 📊 **Advanced Analytics** dashboard
- 🎨 **ASCII Art** for monsters and battles
- 🎵 **Sound Effects** integration
- 📱 **Mobile-friendly** interface

---

## 🤝 **Development Team**

<div align="center">

### **🔧 Partner A: Nasra Mauli**
**Core Game Engine & Monster System**

[GitHub](https://img.shields.io/badge/GitHub-Nasra--Maulid-181717?logo=github)(https://github.com/Nasra-Maulid)

*Specialization: Database Architecture, Game Balance, System Design*

---

### **⚔️ Partner B: Denis Maiyo**  
**Battle System & Player Management**

[GitHub](https://img.shields.io/badge/GitHub-MaiyoDenis-181717?logo=github)(https://github.com/MaiyoDenis)

*Specialization: AI Development, Full-Stack Engineering, User Experience*

</div>

---

## 📜 **License & Educational Use**

This project is developed for educational purposes, demonstrating:
- ✅ **Advanced Python Programming** with object-oriented design
- ✅ **SQLAlchemy ORM Mastery** with complex relationships
- ✅ **Collaborative Software Development** with clear role separation
- ✅ **Professional CLI Application Design** with Rich library
- ✅ **Game Design Principles** and balance mechanics

---

<div align="center">

## 🐉 **Ready to Start Your Adventure?** 🐉

```bash
python3 monster_game.py start
```

*Built with ❤️ through exceptional pair programming collaboration*

[Python](https://img.shields.io/badge/Made%20with-Python-blue.svg?logo=python)(https://python.org)
[SQLAlchemy](https://img.shields.io/badge/Powered%20by-SQLAlchemy-green.svg?logo=sqlalchemy)(https://sqlalchemy.org)
[Rich](https://img.shields.io/badge/Enhanced%20with-Rich-yellow.svg?logo=rich)(https://rich.readthedocs.io)

**Happy Monster Collecting!** 🎮✨

</div>
