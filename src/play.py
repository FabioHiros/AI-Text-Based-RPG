from story import StoryGenerator, EnemyGenerator
from character_creation import Hero, Enemy
from combat import Combat
from item import sword, mace, dagger, wooden_shield, ItemGenerator
from skills import Skill
import re
import os
from dotenv import load_dotenv

class Play:
    def __init__(self, story_generator: StoryGenerator, enemy_generator: EnemyGenerator, item_generator: ItemGenerator) -> None:
        self.story_state = 'The game begins.'
        self.conversation_history = []
        self.hero = self.create_hero()
        self.story_generator = story_generator
        self.enemy_generator = enemy_generator
        self.item_generator = item_generator
        self.processed_items = set()  # Track processed items to avoid duplication
        self.processed_health_changes = set()
    
    def create_hero(self) -> Hero:
        print("Create your character!")
        name = input('Enter your name: ')
        hero = Hero(name=name, health=40, base_damage=2, base_defense=2)
        self.choose_weapon(hero)
        smite = Skill(name="Smite", power=10, description="Deals holy damage.")
        hero.add_skill(smite)
        print(hero)
        return hero

    @staticmethod
    def choose_weapon(hero: Hero) -> None:
        weapons = {
            '1': sword,
            '2': mace,
            '3': dagger
        }

        while True:
            print('''Choose your starting weapon:
                    [1] - Sword : Damage (4), Sharp
                    [2] - Mace  : Damage (6), Blunt
                    [3] - Dagger: Damage (2), Sharp''')
            starting_weapon = input(':')
            if starting_weapon in weapons:
                hero.inventory.add_item(weapons[starting_weapon])
                break
            else:
                print('Invalid choice, please enter only the option number!')

    def interact_with_story(self) -> None:
        while True:
            print(f"Current Story: {self.story_state}")
            self.process_health_changes(self.story_state)

            player_input = input('What do you want to do next? ')

            if "open inventory" in player_input.lower():
                self.inventory_display()
                continue

            self.conversation_history.append(f"Player: {player_input}")

            generated_story = self.story_generator.generate_story(
                conversation_history='\n'.join(self.conversation_history),
                current_story_state=self.story_state,hero=self.hero,inventory=self.hero.inventory.items
            )
            self.update_story(generated_story)

            if "Starting Combat!" in self.story_state:
                enemy = self.create_enemy_from_story()
                combat = Combat(self.hero, enemy)
                combat_result = combat.start()

                if not combat_result:
                    print('Game Over')
                    combat_outcome = f'{self.hero.name} was defeated by {enemy.name}.'
                    self.conversation_history.append(f'Combat outcome: {combat_outcome}.')
                    break

                else:
                    combat_outcome = f'{self.hero.name} won the battle against {enemy.name}.'
                    self.conversation_history.append(f'Combat outcome: {combat_outcome}.')
                    generated_story = self.story_generator.generate_story(
                        conversation_history='\n'.join(self.conversation_history),
                        current_story_state=self.story_state,hero=self.hero,inventory=self.hero.inventory.items
                    )
                    self.update_story(generated_story)
                    continue

            self.process_inventory_changes(self.story_state)

            if player_input.lower() in ['exit', 'quit']:
                print("Ending the game. Thank you for playing!")
                break

    def update_story(self, generated_story: str) -> None:
        self.conversation_history.append(f"AI: {generated_story}")
        self.story_state = generated_story

    def create_enemy_from_story(self) -> Enemy:
        enemy_details = self.enemy_generator.generate_enemy_details(self.story_state, self.hero)
        return Enemy(
            name=enemy_details['name'],
            health=enemy_details['health'],
            base_damage=enemy_details['base_damage'],
            base_defense=enemy_details['base_defense'],
            weapon=dagger,
            shield=wooden_shield
        )

    def inventory_display(self) -> None:
        while True:
            print("Your inventory contains:")
            for index, item in enumerate(self.hero.inventory.items):
                print(f"[{index}] - {item}")

            choice = input('''What do you want to do?: 
                            [0] go back
                            [1] equip item: ''')

            if choice == '0':
                print("Returning to the story...")
                break

            elif choice == '1':
                item_index = input("Enter the number of the item you want to equip: ")

                if item_index.isdigit():
                    item_index = int(item_index)

                    if 0 <= item_index < len(self.hero.inventory.items):
                        item = self.hero.inventory.items[item_index]
                        self.hero.equip(item)
                        break
                    else:
                        print("Invalid choice. That item number is not in your inventory.")
                else:
                    print("Invalid choice. Please enter a number.")

            else:
                print("Invalid choice. Please enter 0 or 1.")

    def process_health_changes(self, story_update: str) -> None:
        heal_pattern = re.compile(r"recovers (\d+) health", re.IGNORECASE)
        damage_pattern = re.compile(r"loses (\d+) health", re.IGNORECASE)

        heal_match = heal_pattern.search(story_update)
        damage_match = damage_pattern.search(story_update)

        if heal_match:
            heal_amount = int(heal_match.group(1))
            if f"heal_{heal_amount}" not in self.processed_health_changes:
                self.hero.health += heal_amount
                self.processed_health_changes.add(f"heal_{heal_amount}")
                print(f"The hero recovers {heal_amount} health. Current health: {self.hero.health}")

        if damage_match:
            damage_amount = int(damage_match.group(1))
            if f"damage_{damage_amount}" not in self.processed_health_changes:
                self.hero.health -= damage_amount
                self.processed_health_changes.add(f"damage_{damage_amount}")
                print(f"The hero loses {damage_amount} health. Current health: {self.hero.health}")

        self.hero.health = max(self.hero.health, 0)

        if self.hero.health <= 0:
            print("You have been defeated! Game over.")
            exit()

    def process_inventory_changes(self, story_update: str) -> None:
        # Patterns to match
        add_item_pattern = re.compile(r"New Item acquired!", re.IGNORECASE)
        remove_item_pattern = re.compile(r"Item removed from inventory: (.+)", re.IGNORECASE)

        # Find matches in the story update
        add_item_matches = add_item_pattern.findall(story_update)
        remove_item_matches = remove_item_pattern.findall(story_update)
        print(remove_item_matches,'remove_matches')
    
        # Handle adding new items
        for _ in add_item_matches:
            item = self.item_generator.generate_item_from_story(self.story_state)
            if item and item.name not in self.processed_items:
                self.hero.inventory.add_item(item)
                self.processed_items.add(item.name)
                print(f"{self.hero.name} finds a {item.name} and adds it to their inventory.")

        # Handle removing items
        for item_name in remove_item_matches:
            item_name = item_name.strip().replace('.','')
            print(item_name,'item name')
            item_to_remove = next((item for item in self.hero.inventory.items if item.name.lower() == item_name.lower()), None)
            if item_to_remove:
                self.hero.inventory.remove_item(item_to_remove)
            else:
                print(f"{item_name} not found in inventory, cannot remove.")

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv('GROQ_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME')
    story_gen = StoryGenerator(api_key=API_KEY, model_name=MODEL_NAME)
    enemy_gen = EnemyGenerator(api_key=API_KEY, model_name=MODEL_NAME)
    item_gen = ItemGenerator(api_key=API_KEY, model_name=MODEL_NAME)

    play_instance = Play(story_generator=story_gen, enemy_generator=enemy_gen, item_generator=item_gen)
    play_instance.interact_with_story()
