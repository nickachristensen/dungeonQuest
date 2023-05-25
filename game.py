import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    char_class = Column(String)
    level = Column(Integer)
    experience = Column(Integer)
    gold = Column(Integer)
    hp = Column(Integer)
    max_hp = Column(Integer)

    quests = relationship('Quest', back_populates='player')




class Quest(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    monster = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))

    player = relationship('Player', back_populates='quests')


# Set up the database
engine = create_engine('sqlite:///game.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Quest generator function
def generate_quest():
    monsters = ['Dragon', 'Goblin', 'Skeleton', 'Troll', 'Witch']
    quest_names = ['The Lost Artifact', 'The Dark Forest', 'Caverns of Despair', 'The Forbidden Tower', 'The Enchanted Ruins']

    monster = random.choice(monsters)
    quest_name = random.choice(quest_names)

    return monster, quest_name


# Rest of the code...

def choose_class():
    char_class = input("Choose your class: (Warrior, Mage, Rogue) ")
    while char_class.lower() not in ["warrior", "mage", "rogue"]:
        char_class = input("Invalid class. Please choose again: (Warrior, Mage, Rogue) ")
    return char_class.capitalize()


def choose_quest(player):
    print("Available quests:")
    quests = session.query(Quest).filter_by(player_id=player.id).all()
    for i, quest in enumerate(quests):
        print(f"{i + 1}. {quest.name}")
    quest_choice = input("Enter the number of your choice: ")
    while quest_choice not in [str(i) for i in range(1, len(quests) + 1)]:
        quest_choice = input("Invalid choice. Please enter the number of your choice: ")
    return quests[int(quest_choice) - 1]

def battle(player, quest):
    monster = quest.monster
    print(f"A wild {monster} appears!")

    monster_stats = {
        'hp': random.randint(50, 100),
        'max_hp': random.randint(80, 120),
        'attack': random.randint(10, 20),
    }

    while True:
        print(f"Your HP: {player.hp}/{player.max_hp}\t{monster} HP: {monster_stats['hp']}/{monster_stats['max_hp']}")
        print("Actions:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Run")

        action = input("Choose an action: ")

        if action == "1":
            player_dmg = random.randint(1, player.attack)
            monster_stats['hp'] -= player_dmg
            print(f"You attack the {monster} and deal {player_dmg} damage!")
            if monster_stats['hp'] <= 0:
                print(f"You defeated the {monster}!")
                return True
            monster_dmg = random.randint(1, monster_stats['attack']) - player.defense
            if monster_dmg < 0:
                monster_dmg = 0
            player.hp -= monster_dmg
            print(f"The {monster} attacks you and deals {monster_dmg} damage!")
            if player.hp <= 0:
                print("You have been defeated!")
                return False
        elif action == "2":
            print(f"The {monster} attacks you but deals no damage!")
            player.defense //= 2
        elif action == "3":
            print("Inventory:")
            for i, item in enumerate(player.inventory):
                print(f"{i + 1}. {item}")
            item_choice = input("Enter the number of the item you want to use: ")
            while item_choice not in [str(i) for i in range(1, len(player.inventory) + 1)]:
                item_choice = input("Invalid choice. Please enter the number of the item you want to use: ")
            item = player.inventory.pop(int(item_choice) - 1)
            if item.lower() == "potion":
                player.hp += 10
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                print("You use a Potion and recover 10 HP!")
        elif action == "4":
            if random.random() < 0.5:
                print("You managed to escape!")
                return False
            else:
                print(f"The {monster} blocks your escape!")
                monster_dmg = random.randint(1, monster_stats['attack']) - player.defense
                if monster_dmg < 0:
                    monster_dmg = 0
                player.hp -= monster_dmg
                print(f"The {monster} attacks you and deals {monster_dmg} damage!")
                if player.hp <= 0:
                    print("You have been defeated!")
                    return False
        else:
            print("Invalid action. Please try again.")

def start_game():
    name = input("Welcome to the Fantasy Game! What is your name? ")
    char_class = choose_class()

    # Check if player of the chosen class already exists
    existing_player = session.query(Player).filter_by(char_class=char_class).first()
    if existing_player:
        print(f"A player of class {char_class} already exists.")
        return

    # Create a new player
    player = Player(name=name, char_class=char_class, level=1, experience=0, gold=50)
    session.add(player)
    session.commit()

    print(f"Welcome, {player.name} the {player.char_class}!")

    # Generate initial quests for the player
    num_initial_quests = 3
    for _ in range(num_initial_quests):
        monster, quest_name = generate_quest()
        new_quest = Quest(name=quest_name, monster=monster, player_id=player.id)
        session.add(new_quest)
    session.commit()

    while True:
        chosen_quest = choose_quest(player)
        print(f"You selected the {chosen_quest.name} quest - Defeat the {chosen_quest.monster}!")

        if battle(player, chosen_quest):
            print(f"You completed the {chosen_quest.name} quest and earned experience and gold!")
            # Update player's stats and handle level up
            # ...
        else:
            print("Game over.")
            break


start_game()
