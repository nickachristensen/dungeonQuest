import random  # Import the random module for generating random values
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table  # Import SQLAlchemy modules
from sqlalchemy.ext.declarative import declarative_base  # Import the declarative base class
from sqlalchemy.orm import sessionmaker, relationship  # Import sessionmaker and relationship from SQLAlchemy

Base = declarative_base()  # Create a base class for SQLAlchemy models


class Player(Base):  # Define the Player class, subclass of Base
    __tablename__ = "players"  # Define the table name for the Player model in the database

    # Define columns for the Player table
    id = Column(Integer, primary_key=True)  # Player ID column
    name = Column(String)  # Player name column
    char_class = Column(String)  # Player character class column
    level = Column(Integer)  # Player level column
    experience = Column(Integer)  # Player experience column
    gold = Column(Integer)  # Player gold column
    hp = Column(Integer)  # Player health points column
    max_hp = Column(Integer)  # Player maximum health points column
    attack = Column(Integer)  # Player attack power column
    defense = Column(Integer)  # Player defense power column
    inventory = relationship("Item", backref="player")  # Define a relationship with the Item model
    quests = relationship("Quest", back_populates="player")  # Define a relationship with the Quest model

    def __init__(self, name, char_class, level, experience, gold, hp, max_hp, attack, defense):
    # Initialize the Player object with provided values
        self.name = name  # Assign the 'name' parameter to the 'name' instance variable
        self.char_class = char_class  # Assign the 'char_class' parameter to the 'char_class' instance variable
        self.level = level  # Assign the 'level' parameter to the 'level' instance variable
        self.experience = experience  # Assign the 'experience' parameter to the 'experience' instance variable
        self.gold = gold  # Assign the 'gold' parameter to the 'gold' instance variable
        self.hp = hp  # Assign the 'hp' parameter to the 'hp' instance variable
        self.max_hp = max_hp  # Assign the 'max_hp' parameter to the 'max_hp' instance variable
        self.attack = attack  # Assign the 'attack' parameter to the 'attack' instance variable
        self.defense = defense  # Assign the 'defense' parameter to the 'defense' instance variable
        self.inventory = []  # Initialize the 'inventory' instance variable as an empty list

def __repr__(self):
    # Return a string representation of the Player object
    return f"Player(name='{self.name}', char_class='{self.char_class}', level={self.level}, hp={self.hp})"



class Item(Base):  # Define the Item class, subclass of Base
    __tablename__ = "items"  # Define the table name for the Item model in the database

    # Define columns for the Item table
    id = Column(Integer, primary_key=True)  # Item ID column
    name = Column(String)  # Item name column
    attack_inc = Column(Integer)  # Attack increment column
    defense_inc = Column(Integer)  # Defense increment column
    hp_inc = Column(Integer)  # Health points increment column
    mp_inc = Column(Integer)  # Mana points increment column
    evasion_inc = Column(Integer)  # Evasion increment column
    player_id = Column(Integer, ForeignKey("players.id"))  # Player ID foreign key column

def __init__(self, name, attack_inc=0, defense_inc=0, hp_inc=0, mp_inc=0, evasion_inc=0):
    # Initialize the Item object with provided values
    self.name = name  # Assign the 'name' parameter to the 'name' instance variable
    self.attack_inc = attack_inc  # Assign the 'attack_inc' parameter to the 'attack_inc' instance variable
    self.defense_inc = defense_inc  # Assign the 'defense_inc' parameter to the 'defense_inc' instance variable
    self.hp_inc = hp_inc  # Assign the 'hp_inc' parameter to the 'hp_inc' instance variable
    self.mp_inc = mp_inc  # Assign the 'mp_inc' parameter to the 'mp_inc' instance variable
    self.evasion_inc = evasion_inc  # Assign the 'evasion_inc' parameter to the 'evasion_inc' instance variable

    def __repr__(self):
        # Return a string representation of the Item object
        return f"Item(name='{self.name}')"

def apply_to_player(self, player):
    # Apply the effects of the item to the player
    player.attack += self.attack_inc  # Increase the player's attack by the 'attack_inc' value of the item
    player.defense += self.defense_inc  # Increase the player's defense by the 'defense_inc' value of the item
    player.hp += self.hp_inc  # Increase the player's HP by the 'hp_inc' value of the item
    player.max_hp += self.hp_inc  # Increase the player's max HP by the 'hp_inc' value of the item
    player.inventory.remove(self)  # Remove the item from the player's inventory


class Quest(Base):  # Define the Quest class, subclass of Base
    __tablename__ = "quests"  # Define the table name for the Quest model in the database
    id = Column(Integer, primary_key=True)  # Quest ID column
    name = Column(String)  # Quest name column
    monster = Column(String)  # Monster column
    player_id = Column(Integer, ForeignKey("players.id"))  # Player ID foreign key column
    player = relationship("Player", back_populates="quests")  # Define a relationship with the Player model
    items = relationship("Item", secondary="quest_item_association")  # Define a relationship with the Item model
    monsters = relationship("Monster", secondary="quest_monster_association")  # Define a relationship with the Monster model


class Monster(Base):  # Define the Monster class, subclass of Base
    __tablename__ = "monsters"  # Define the table name for the Monster model in the database
    id = Column(Integer, primary_key=True)  # Monster ID column
    name = Column(String)  # Monster name column
    hp = Column(Integer)  # Monster health points column
    max_hp = Column(Integer)  # Monster maximum health points column
    attack = Column(Integer)  # Monster attack power column
    defense = Column(Integer)  # Monster defense power column

def __init__(self, name, hp, max_hp, attack, defense):
    # Initialize the Monster object with provided values
    self.name = name  # Store the name of the monster
    self.hp = hp  # Store the current hit points of the monster
    self.max_hp = max_hp  # Store the maximum hit points of the monster
    self.attack = attack  # Store the attack power of the monster
    self.defense = defense  # Store the defense power of the monster


player_item_association = Table(
    "player_item_association",  # Define the name of the association table
    Base.metadata,  # Use the metadata from the declarative base
    Column("player_id", Integer, ForeignKey("players.id")),  # Define a column for player_id, referencing players.id
    Column("item_id", Integer, ForeignKey("items.id")),  # Define a column for item_id, referencing items.id
)

quest_item_association = Table(
    "quest_item_association",  # Define the name of the association table
    Base.metadata,  # Use the metadata from the declarative base
    Column("quest_id", Integer, ForeignKey("quests.id")),  # Define a column for quest_id, referencing quests.id
    Column("item_id", Integer, ForeignKey("items.id")),  # Define a column for item_id, referencing items.id
)

quest_monster_association = Table(
    "quest_monster_association",  # Define the name of the association table
    Base.metadata,  # Use the metadata from the declarative base
    Column("quest_id", Integer, ForeignKey("quests.id")),  # Define a column for quest_id, referencing quests.id
    Column("monster_id", Integer, ForeignKey("monsters.id")),  # Define a column for monster_id, referencing monsters.id
)


engine = create_engine("sqlite:///game.db")  # Create an SQLite database engine
Base.metadata.create_all(engine)  # Create the tables defined in the models

Session = sessionmaker(bind=engine)  # Create a session factory
session = Session()  # Create a session object


def generate_quest():
    # Generate a random quest and monster name from predefined lists

    monsters = ["Dragon", "Goblin", "Skeleton", "Troll", "Witch"]  # List of available monster names
    quest_names = [  # List of available quest names
        "The Lost Artifact",
        "The Dark Forest",
        "Caverns of Despair",
        "The Forbidden Tower",
        "The Enchanted Ruins",
    ]

    monster = random.choice(monsters)  # Select a random monster name from the list
    quest_name = random.choice(quest_names)  # Select a random quest name from the list

    return monster, quest_name  # Return the randomly generated monster name and quest name as a tuple


def choose_class():
    # Prompt the user to choose a character class

    char_class = input("Choose your class: (Warrior, Mage, Rogue) ")  # Prompt the user for input
    while char_class.lower() not in ["warrior", "mage", "rogue"]:  # Validate the input
        char_class = input("Invalid class. Please choose again: (Warrior, Mage, Rogue) ")
    return char_class.capitalize()  # Return the chosen character class


def choose_quest(player):
    # Display the available quests for the player and prompt for a quest choice

    print("Available quests:")
    quests = session.query(Quest).filter_by(player_id=player.id).all()  # Retrieve the quests for the player
    for i, quest in enumerate(quests):  # Iterate over the quests and display their names with corresponding numbers
        print(f"{i + 1}. {quest.name}")

    quest_choice = input("Enter the number of your choice: ")  # Prompt the user for quest choice
    while quest_choice not in [str(i) for i in range(1, len(quests) + 1)]:  # Validate the input
        quest_choice = input("Invalid choice. Please enter the number of your choice: ")

    return quests[int(quest_choice) - 1]  # Return the chosen quest



def battle(player, quest):
    # Simulate a battle between the player and a monster in a quest

    monster = quest.monster
    print(f"A wild {monster} appears!")  # Display the monster's name

    monster_stats = {
        "hp": random.randint(50, 100),  # Randomly generate the monster's HP
        "max_hp": random.randint(80, 120),  # Randomly generate the monster's maximum HP
        "attack": random.randint(10, 20),  # Randomly generate the monster's attack power
    }

    while True:
        # Print the current HP of the player and the monster, and display available actions

        print(f"Your HP: {player.hp}/{player.max_hp}\t{monster} HP: {monster_stats['hp']}/{monster_stats['max_hp']}")
        print("Actions:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Run")

        action = input("Choose an action: ")  # Prompt the player to choose an action

        if action == "1":
            # Player attacks the monster

            player_dmg = random.randint(1, player.attack)  # Calculate the player's damage
            monster_stats["hp"] -= player_dmg  # Reduce the monster's HP
            print(f"You attack the {monster} and deal {player_dmg} damage!")

            if monster_stats["hp"] <= 0:
                # Check if the monster is defeated
                print(f"You defeated the {monster}!")
                return True

            monster_dmg = random.randint(1, monster_stats["attack"]) - player.defense  # Calculate the monster's damage to the player

            if monster_dmg < 0:
                monster_dmg = 0

            player.hp -= monster_dmg  # Reduce the player's HP based on the monster's damage
            print(f"The {monster} attacks you and deals {monster_dmg} damage!")

            if player.hp <= 0:
                # Check if the player is defeated
                print("You have been defeated!")
                return False

        elif action == "2":
            # Player defends against the monster's attack

            print(f"The {monster} attacks you but deals no damage!")
            player.defense //= 2  # Halve the player's defense temporarily

        elif action == "3":
            # Player uses an item from their inventory

            if not player.inventory:  # Check if the inventory is empty
                print("Your inventory is empty.")
                continue  # Send the player back to the previous selection

            print("\nInventory:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item}")

            item_choice = int(input("Enter the number of the item you want to use: "))  # Prompt the player to choose an item

            if 1 <= item_choice <= len(player.inventory):
                # Validate the item choice

                chosen_item = player.inventory[item_choice - 1]  # Retrieve the chosen item from the inventory

                if chosen_item.name.lower() == "mana potion" or chosen_item.name.lower() == "health potion":
                    # Apply health restoration for health and mana potions
                    chosen_item.apply_to_player(player)
                    print(f"You use a {chosen_item.name} and recover {chosen_item.hp_inc} HP!")

                elif chosen_item.name.lower() not in ["mana potion", "health potion"]:
                    # Apply item effects for other items
                    chosen_item.apply_to_player(player)
                    print(f"You use a {chosen_item.name} and it has its effects applied!")
            else:
                print("Invalid item choice.")

        elif action == "4":
            # Attempt to run away from the battle

            if random.random() < 0.5:
                # Random chance of successfully escaping
                print("You managed to escape!")
                return False

            else:
                print(f"The {monster} blocks your escape!")
                monster_dmg = (
                    random.randint(1, monster_stats["attack"]) - player.defense
                )  # Calculate the monster's damage to the player during escape

                if monster_dmg < 0:
                    monster_dmg = 0

                player.hp -= monster_dmg  # Reduce the player's HP based on the monster's damage
                print(f"The {monster} attacks you and deals {monster_dmg} damage!")

                if player.hp <= 0:
                    # Check if the player is defeated during escape
                    print("You have been defeated!")
                    return False
        else:
            print("Invalid action. Please try again.")  # Display an error message for invalid actions



def start_game():
    # Start the game and prompt for player's name and class
    name = input("Welcome to Dungeon Quest! What is your name? ")
    char_class = choose_class()

    # Check if a player with the same name and class already exists
    existing_player = (
        session.query(Player).filter_by(name=name, char_class=char_class).first()
    )

    if existing_player:
        player = existing_player
        print(f"Welcome back, {player.name} the {player.char_class}!")

    else:
        # Create a new player
        player = Player(
            name=name,
            char_class=char_class,
            level=1,
            experience=0,
            gold=50,
            hp=0,
            max_hp=0,
            attack=0,
            defense=0,  # Initialize defense to 0
        )

        # Assign max_hp, hp, and attack based on the chosen class
        if char_class.lower() == "warrior":
            player.max_hp = 100
            player.hp = player.max_hp
            player.attack = 20
            player.defense = 10  # Set defense for warrior class
            player.inventory.extend(
                [
                    Item(name="Sword of Strength", attack_inc=10),
                    Item(name="Shield of Defense", defense_inc=5),
                    Item(name="Health Potion", hp_inc=20),
                ]
            )

        elif char_class.lower() == "mage":
            player.max_hp = 80
            player.hp = player.max_hp
            player.attack = 30
            player.defense = 5  # Set defense for mage class
            player.inventory.extend(
                [
                    Item(name="Staff of Fire", attack_inc=15),
                    Item(name="Robe of Protection", defense_inc=3),
                    Item(name="Mana Potion", hp_inc=30),
                ]
            )
        elif char_class.lower() == "rogue":
            player.max_hp = 60
            player.hp = player.max_hp
            player.attack = 40
            player.defense = 3  # Set defense for rogue class
            player.inventory.extend(
                [
                    Item(name="Dagger of Agility", attack_inc=12),
                    Item(name="Cloak of Shadows", defense_inc=2),
                    Item(name="Evasion Potion", evasion_inc=10),
                ]
            )
        else:
            player.max_hp = 100  # Default max_hp value
            player.hp = player.max_hp
            player.attack = 10  # Default attack value
            player.defense = 0  # Default defense value

        session.add(player)  # Add the player to the session
        session.commit()  # Commit the changes to the database

        print(f"Welcome, {player.name} the {player.char_class}!")

        # Generate initial quests for the player
        num_initial_quests = 3
        for _ in range(num_initial_quests):
            monster, quest_name = generate_quest()
            new_quest = Quest(name=quest_name, monster=monster, player_id=player.id)
            session.add(new_quest)  # Add the quest to the session
        session.commit()  # Commit the changes to the database

    while True:
        chosen_quest = choose_quest(player)  # Prompt for a quest choice
        print(
            f"You selected the quest '{chosen_quest.name}' to battle the {chosen_quest.monster}!"
        )

        result = battle(player, chosen_quest)  # Start the battle

        if result:
            print("Congratulations, you have completed the quest!")
            session.delete(chosen_quest)  # Remove the quest from the session
            session.commit()  # Commit the changes to the database
            player.experience += 100  # Increase player experience
            player.gold += 50  # Increase player gold
            level_up(player)  # Level up the player
        else:
            print("Game Over!")
            break


def level_up(player):
    # Level up the player if they have enough experience
    if player.experience >= 100:
        player.level += 1  # Increase the player's level by 1
        player.experience -= 100  # Subtract the required experience for leveling up from the player's current experience
        player.max_hp += 10  # Increase the player's maximum HP by 10
        player.hp = player.max_hp  # Set the player's current HP equal to their maximum HP
        player.attack += 5  # Increase the player's attack power by 5
        player.defense += 2  # Increase the player's defense power by 2
        print("Level up! You are now level", player.level)  # Display a message indicating that the player has leveled up and their new level
        print("Max HP increased to", player.max_hp)  # Display a message indicating that the player's maximum HP has increased
        print("Attack increased to", player.attack)  # Display a message indicating that the player's attack power has increased
        print("Defense increased to", player.defense)  # Display a message indicating that the player's defense power has increased

start_game()  # Start the game
