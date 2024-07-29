from item import fist,mace, Item
from skills import Skill
class Character:
    def __init__(self,
                  name:str,
                  health:int,
                  base_damage:int,
                  base_defense:int,
                  weapon:str = fist,
                  shield:str= None,
                  job:str = None,
                  skills:list = []
                      ) -> None:
        """
        Initialize a Character object.

        Args:
        - name (str): The name of the character.
        - health (int): The initial health points of the character.
        - base_damage (int): The base attack points of the character.
        - base_defense (int): The base defense points of the character.
        - weapon (str, optional): The initial weapon equipped by the character. Defaults to fist.
        - shield (str, optional): The initial shield equipped by the character. Defaults to None.
        - job (str, optional): The job or role of the character. Defaults to None.
        """
        self.name = name
        self.health = health
        self.weapon = weapon
        self.shield = shield
        self.base_damage = base_damage
        if self.shield: self.total_defense = base_defense + self.shield.defense
        else: self.total_defense = base_defense
        self.total_damage = base_damage + self.weapon.damage
        self.base_defense = base_defense 
        self.job = job
        self.skills = skills
        self.inventory = Inventory()

    def is_alive(self) -> bool:
        return self.health > 0
    
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item) -> None:
        if item not in self.items:
            self.items.append(item)
            print(f'{item.name} added to inventory.')
        else:
            print(f'{item.name} is already in inventory.')

    def remove_item(self, item: Item) -> None:
        if item in self.items:
            self.items.remove(item)
            print(f'{item.name} removed from inventory.')
        else:
            print(f'{item.name} not found in inventory.')

    def __str__(self):
        return ', '.join([item.name for item in self.items])




    


class Hero(Character):

    # def __init__(self,
    #               name: str,
    #                 health: int,
    #                   base_damage: int,
    #                     base_defense: int,
    #                       weapon: str = fist,
    #                         job: str = None
    #                         ) -> None:
    #     super().__init__(name, health, base_damage, base_defense, weapon, job)

    def equip(self, item: Item) -> None:

        """
        Equip an item (weapon or shield) to the hero.

        Args:
        - item (Item): The item object to equip.
        """

        match item.item_type:
            
            case 'Weapon':
                self.weapon = item
                self.total_damage = self.base_damage + self.weapon.damage
                print(f'{self.name} equipped {item.name} as weapon!')
            
            case 'Shield':
                self.shield = item
                self.total_defense = self.base_defense + self.shield.defense
                print(f'{self.name} equipped {item.name} as shield!')
            
            case _:
                print(f'Cannot equip item of type {item.item_type}!')

    def add_skill(self, skill: 'Skill') -> None:
        """
        Add a new skill to the hero.

        Args:
        - skill (str): The skill to add.
        """
        if skill not in self.skills:
            self.skills.append(skill)
            print(f'{self.name} learned a new skill: {skill}!')
        else:
            print(f'{self.name} already knows the skill: {skill.name}!')

    
    def __str__(self) -> str:

        """
        Return a string representation of the Hero object.

        Returns:
        - str: String representation including hero's name, health, attack, defense, equipped weapon, and job.
        """
        shield_defense = f'+ {self.shield.defense}' if self.shield else ''
        
        return f'''
        Name: {self.name} 
        
         Health: {self.health} 
          
          Attack: {self.base_damage} + {self.weapon.damage}
           
           Defense: {self.base_defense} {shield_defense}
            
            Weapon: {self.weapon}
                Shield: {self.shield} 
             
             Job: {self.job}'''



class Enemy(Character):
    def __str__(self) -> str:

        """
        Return a string representation of the Enemy object.

        Returns:
        - str: String representation including enemy's name, health, attack, defense, equipped weapon, and job.
        """
        shield_defense = f'+ {self.shield.defense}' if self.shield else ''
        
        return f'''
        Name: {self.name} 
        
         Health: {self.health} 
          
          Attack: {self.base_damage} + {self.weapon.damage}
           
           Defense: {self.base_defense} {shield_defense}
            
            Weapon: {self.weapon} 
                Shield: {self.shield}
             
             Job: {self.job}'''
  
    # def __init__(self,
    #               name: str,
    #                 health: int,
    #                   base_damage: int,
    #                     base_defense: int,
    #                       weapon: str = fist,
    #                         job: str = None
    #                         ) -> None:
    #     super().__init__(name, health, base_damage, base_defense, weapon, job)

