import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


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
    inventory = relationship("Item", backref="player")

    def __init__(
        self, name, char_class, level, experience, gold, hp, max_hp, attack, defense
    ):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.experience = experience
        self.gold = gold
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.inventory = []  # Initialize inventory as an empty list

    def __repr__(self):
        return f"Player(name='{self.name}', char_class='{self.char_class}', level={self.level}, hp={self.hp})"

    quests = relationship("Quest", back_populates="player")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    attack_inc = Column(Integer)
    defense_inc = Column(Integer)
    hp_inc = Column(Integer)
    mp_inc = Column(Integer)
    evasion_inc = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"))  # Foreign key relationship

    def __init__(
        self, name, attack_inc=0, defense_inc=0, hp_inc=0, mp_inc=0, evasion_inc=0
    ):
        self.name = name
        self.attack_inc = attack_inc
        self.defense_inc = defense_inc
        self.hp_inc = hp_inc
        self.mp_inc = mp_inc
        self.evasion_inc = evasion_inc

    def __repr__(self):
        return f"Item(name='{self.name}')"

    def apply_to_player(self, player):
        player.attack += self.attack_inc
        player.defense += self.defense_inc
        player.hp += self.hp_inc
        player.max_hp += self.hp_inc
        # Update other player stats if needed

        player.inventory.remove(self)  # Remove the item from the player's inventory


class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    monster = Column(String)
    player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Player", back_populates="quests")


# Set up the database
engine = create_engine("sqlite:///game.db")
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Quest generator function
def generate_quest():
    monsters = ["Dragon", "Goblin", "Skeleton", "Troll", "Witch"]
    quest_names = [
        "The Lost Artifact",
        "The Dark Forest",
        "Caverns of Despair",
        "The Forbidden Tower",
        "The Enchanted Ruins",
    ]

    monster = random.choice(monsters)
    quest_name = random.choice(quest_names)

    return monster, quest_name


def choose_class():
    char_class = input("Choose your class: (Warrior, Mage, Rogue) ")
    while char_class.lower() not in ["warrior", "mage", "rogue"]:
        char_class = input(
            "Invalid class. Please choose again: (Warrior, Mage, Rogue) "
        )
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
        "hp": random.randint(50, 100),
        "max_hp": random.randint(80, 120),
        "attack": random.randint(10, 20),
    }

    while True:
        print(
            f"Your HP: {player.hp}/{player.max_hp}\t{monster} HP: {monster_stats['hp']}/{monster_stats['max_hp']}"
        )
        print("Actions:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Run")

        action = input("Choose an action: ")

        if action == "1":
            player_dmg = random.randint(1, player.attack)
            monster_stats["hp"] -= player_dmg
            print(f"You attack the {monster} and deal {player_dmg} damage!")

            if monster_stats["hp"] <= 0:
                print(f"You defeated the {monster}!")
                return True
            monster_dmg = random.randint(1, monster_stats["attack"]) - player.defense

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
            if not player.inventory:  # Check if the inventory is empty
                print("Your inventory is empty.")
                continue  # Send the player back to the previous selection

            print("\nInventory:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item}")
            item_choice = int(input("Enter the number of the item you want to use: "))

            if 1 <= item_choice <= len(player.inventory):
                chosen_item = player.inventory[item_choice - 1]

                if chosen_item.name.lower() == "mana potion" or chosen_item.name.lower() == "health potion":
                    chosen_item.apply_to_player(player)
                    print(f"You use a {chosen_item.name} and recover {chosen_item.hp_inc} HP!")

                elif chosen_item.name.lower() not in ["mana potion", "health potion"]:
                    chosen_item.apply_to_player(player)
                    print(f"You use a {chosen_item.name} and it has its effects applied!")
            else:
                print("Invalid item choice.")


        elif action == "4":
            if random.random() < 0.5:
                print("You managed to escape!")
                return False

            else:
                print(f"The {monster} blocks your escape!")
                monster_dmg = (
                    random.randint(1, monster_stats["attack"]) - player.defense
                )

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
        print(
            f"You selected the {chosen_quest.name} quest - Defeat the {chosen_quest.monster}!"
        )

        if battle(player, chosen_quest):
            print(
                f"You completed the {chosen_quest.name} quest and earned experience and gold!"
            )
            # Update player's stats and handle level up
            # ...
        else:
            print("Game over!")
            break


start_game()
