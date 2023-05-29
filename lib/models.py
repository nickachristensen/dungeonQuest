from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
import random

# Create the database engine and session
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    attack_inc = Column(Integer)
    defense_inc = Column(Integer)
    hp_inc = Column(Integer)
    evasion_inc = Column(Integer)


class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    max_hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    monster_id = Column(Integer, ForeignKey('monsters.id'))
    monster = relationship('Monster')


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    char_class = Column(String)
    level = Column(Integer)
    experience = Column(Integer)
    gold = Column(Integer)
    hp = Column(Integer)
    max_hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    inventory = relationship("Item")


def generate_quest():
    # Generate a random quest from the available quests in the database
    try:
        quests = session.query(Quest).all()
        quest = random.choice(quests)
        monster = quest.monster
        return monster, quest
    except NoResultFound:
        print("No quests found in the database.")


def choose_class():
    # Prompt the player to choose a character class
    char_classes = ["Warrior", "Mage", "Rogue"]

    while True:
        char_class = input(f"Choose a class ({', '.join(char_classes)}): ")

        if char_class.capitalize() in char_classes:
            return char_class.capitalize()

        print(f"Invalid class. Choose from {', '.join(char_classes)}.")


def choose_quest(player):
    # Display available quests and prompt the player to choose a quest
    available_quests = session.query(Quest).filter(Quest.player_id == player.id).all()
    print("\nAvailable Quests:")
    for i, quest in enumerate(available_quests, 1):
        print(f"{i}. {quest.name}")

    while True:
        quest_number = int(input("Choose a quest number: "))
        if 1 <= quest_number <= len(available_quests):
            return available_quests[quest_number - 1]

        print(f"Invalid choice. Choose a number between 1 and {len(available_quests)}.")


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
    name = input("Welcome to Dungeon Quest! What is your name? ")
    char_class = choose_class()

    try:
        player = session.query(Player).filter_by(name=name, char_class=char_class).one()
        print(f"Welcome back, {player.name} the {player.char_class}!")
    except NoResultFound:
        player = Player(
            name=name,
            char_class=char_class,
            level=1,
            experience=0,
            gold=50,
            hp=0,
            max_hp=0,
            attack=0,
            defense=0,
        )

        session.add(player)
        session.commit()

        print(f"Welcome, {player.name} the {player.char_class}!")

    while True:
        chosen_quest = choose_quest(player)
        print(f"You selected the quest '{chosen_quest.name}' to battle the {chosen_quest.monster.name}!")

        result = battle(player, chosen_quest)

        if result:
            print("Congratulations, you have completed the quest!")
            session.delete(chosen_quest)
            session.commit()
            player.experience += 100
            player.gold += 50
            level_up(player)
        else:
            print("Game Over!")
            break


def level_up(player):
    # Level up the player and increase their stats
    player.level += 1
    player.max_hp += 10
    player.hp = player.max_hp
    player.attack += 5
    player.defense += 3
    print(f"\n{player.name} leveled up to level {player.level}!")


start_game()
