from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Item, Monster, Quest, Player

# Create an engine and session
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables
Base.metadata.create_all(engine)

# Function to populate the database with initial data
def seed_database():
    # Create and insert player records
    players = [
        Player(name='Warrior', char_class='Warrior'),
        Player(name='Mage', char_class='Mage'),
        Player(name='Rogue', char_class='Rogue')
    ]
    session.add_all(players)
    session.commit()

# Call the seed function
seed_database()

# Seed the items
items_data = [
    Item(name="Sword of Strength", attack_inc=10),
    Item(name="Shield of Defense", defense_inc=5),
    Item(name="Health Potion", hp_inc=20),
    Item(name="Staff of Fire", attack_inc=15),
    Item(name="Robe of Protection", defense_inc=3),
    Item(name="Mana Potion", hp_inc=30),
    Item(name="Dagger of Agility", attack_inc=12),
    Item(name="Cloak of Shadows", defense_inc=2),
    Item(name="Evasion Potion", evasion_inc=10),
]

for item_data in items_data:
    session.add(item_data)

# Seed the monsters
monsters_data = [
    Monster(name="Dragon", max_hp=200, hp=200, attack=50, defense=10),
    Monster(name="Goblin", max_hp=50, hp=50, attack=20, defense=5),
    Monster(name="Skeleton", max_hp=30, hp=30, attack=15, defense=2),
    Monster(name="Troll", max_hp=100, hp=100, attack=30, defense=8),
    Monster(name="Witch", max_hp=80, hp=80, attack=25, defense=5),
]

for monster_data in monsters_data:
    session.add(monster_data)

# Seed the quests
quest_names = [
    "The Lost Artifact",
    "The Dark Forest",
    "Caverns of Despair",
    "The Forbidden Tower",
    "The Enchanted Ruins",
]

for quest_name in quest_names:
    quest = Quest(name=quest_name)
    quest.monsters.append(Monster(name="Dragon", max_hp=200, hp=200, attack=50, defense=10))
    session.add(quest)

# Commit the changes
session.commit()

# Close the session
session.close()