from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Item

# Create an engine and session
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables
Base.metadata.create_all(engine)

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

# Commit the changes
session.commit()

# Close the session
session.close()
