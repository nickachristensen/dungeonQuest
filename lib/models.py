import random

# Item class to represent items in the game
class Item:
    def __init__(self, name, attack_inc=0, defense_inc=0, hp_inc=0, evasion_inc=0):
        self.name = name
        self.attack_inc = attack_inc
        self.defense_inc = defense_inc
        self.hp_inc = hp_inc
        self.evasion_inc = evasion_inc

    def apply_to_player(self, player):
        # Apply the effects of the item to the player
        player.attack += self.attack_inc
        player.defense += self.defense_inc
        player.hp += self.hp_inc
        player.evasion += self.evasion_inc


# Monster class to represent monsters in the game
class Monster:
    def __init__(self, name, hp, max_hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense


# Player class to represent the player character
class Player:
    def __init__(self, name, char_class, level, experience, gold, hp, max_hp, attack, defense, evasion=0):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.experience = experience
        self.gold = gold
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.evasion = evasion
        self.inventory = []

    def level_up(self):
        # Increase player's level and attributes when leveling up
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        print(f"\n{self.name} leveled up to level {self.level}!")


def generate_quest():
    # Generate a random monster and quest name for the quest
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


def battle(player, monster):
    print(f"A wild {monster} appears!")

    # Initialize the stats for the monster
    monster_stats = {
        "hp": random.randint(50, 100),
        "max_hp": random.randint(80, 120),
        "attack": random.randint(20, 30),
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
            # Player attacks the monster
            player_dmg = random.randint(1, player.attack)
            monster_stats["hp"] -= player_dmg
            print(f"You attack the {monster} and deal {player_dmg} damage!")

            if monster_stats["hp"] <= 0:
                print(f"You defeated the {monster}!")
                return True

            # Monster attacks the player
            monster_dmg = random.randint(1, monster_stats["attack"]) - player.defense

            if monster_dmg < 0:
                monster_dmg = 0
            player.hp -= monster_dmg
            print(f"The {monster} attacks you and deals {monster_dmg} damage!")

            if player.hp <= 0:
                print("You have been defeated!")
                return False

        elif action == "2":
            # Player defends against the monster's attack
            print(f"The {monster} attacks you but deals no damage!")
            player.defense //= 2

        elif action == "3":
            # Player uses an item from their inventory
            if not player.inventory:
                print("Your inventory is empty.")
                continue

            print("\nInventory:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.name}")

            item_choice = int(input("Enter the number of the item you want to use: "))

            if 1 <= item_choice <= len(player.inventory):
                chosen_item = player.inventory[item_choice - 1]

                if chosen_item.name.lower() in ["mana potion", "health potion"]:
                    # Apply the effects of health or mana potion
                    if chosen_item.name.lower() == "mana potion":
                        player.mana += chosen_item.hp_inc
                        print(f"You use a {chosen_item.name} and recover {chosen_item.hp_inc} mana!")
                    elif chosen_item.name.lower() == "health potion":
                        player.hp += chosen_item.hp_inc
                        print(f"You use a {chosen_item.name} and recover {chosen_item.hp_inc} HP!")

                    # Remove the used item from the player's inventory
                    del player.inventory[item_choice - 1]

                elif chosen_item.name.lower() not in ["mana potion", "health potion"]:
                    # Apply the effects of the chosen item
                    chosen_item.apply_to_player(player)
                    print(f"You use a {chosen_item.name} and it has its effects applied!")

                    # Remove the used item from the player's inventory
                    del player.inventory[item_choice - 1]

                else:
                    # Handle other items that cannot be used during battle
                    print("This item cannot be used during battle.")
            else:
                print("Invalid item choice.")

        elif action == "4":
            # Player tries to escape from the battle
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


def level_up(player):
    # Check if the player has enough experience to level up
    if player.experience >= 100:
        player.level += 1
        player.experience -= 100
        player.max_hp += 10
        player.hp = player.max_hp
        player.attack += 5
        player.defense += 2
        print("Level up! You are now level", player.level)
        print("Max HP increased to", player.max_hp)
        print("Attack increased to", player.attack)
        print("Defense increased to", player.defense)


def start_game():
    # Get player's name and character class
    name = input("Welcome to Dungeon Quest! What is your name? ")
    char_class = input("Choose your class: (Warrior, Mage, Rogue) ")

    # Create a player object based on the chosen class
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

        # Refill the inventory with warrior-specific items
        player.inventory = [
            Item(name="Sword of Strength", attack_inc=10),
            Item(name="Shield of Defense", defense_inc=5),
            Item(name="Health Potion", hp_inc=20),
        ]

    elif char_class.lower() == "mage":
        player.max_hp = 80
        player.hp = player.max_hp
        player.attack = 30
        player.defense = 5  # Set defense for mage class

        # Refill the inventory with mage-specific items
        player.inventory = [
            Item(name="Staff of Fire", attack_inc=15),
            Item(name="Robe of Protection", defense_inc=3),
            Item(name="Mana Potion", hp_inc=30),
        ]

    elif char_class.lower() == "rogue":
        player.max_hp = 60
        player.hp = player.max_hp
        player.attack = 40
        player.defense = 3  # Set defense for rogue class

        # Refill the inventory with rogue-specific items
        player.inventory = [
            Item(name="Dagger of Agility", attack_inc=12),
            Item(name="Cloak of Shadows", defense_inc=2),
            Item(name="Evasion Potion", evasion_inc=10),
        ]

    else:
        player.max_hp = 100  # Default max_hp value
        player.hp = player.max_hp
        player.attack = 10  # Default attack value
        player.defense = 0  # Default defense value

        # Refill the inventory with default items
        player.inventory = [
            Item(name="Basic Sword", attack_inc=5),
            Item(name="Leather Armor", defense_inc=2),
        ]

    print(f"Welcome, {player.name} the {player.char_class}!")

    while True:
        monster, quest_name = generate_quest()
        print(f"You selected the quest '{quest_name}' to battle the {monster}!")

        # Resupply the player's inventory at the start of each new quest
        player.inventory.extend([
            Item(name="Health Potion", hp_inc=20),
            Item(name="Mana Potion", hp_inc=30),
        ])

        result = battle(player, monster)

        if result:
            print("Congratulations, you have completed the quest!")
            player.experience += 100
            player.gold += 50
            level_up(player)
        else:
            print("Game Over!")
            break

# Start the game
start_game()
