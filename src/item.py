
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import json
import os
from dotenv import load_dotenv

# class Item:
#     def __init__(self,
#                  name:str,
#                  item_type:str
#                  ) -> None:
#         """
#         Initialize an item with a name and its type.

#         Args:
#         - name (str): The name of the item.
#         - item_type (str): The type of the item (e.g., Weapon, Shield).
#         """

#         self.name=name
#         self.item_type=item_type

#     def __str__(self) -> str:
#         """
#         Return a string representation of the item.

#         Returns:
#         - str: String representation of the item.
#         """
#         return f'{self.name} ({self.item_type})'

# class Weapon(Item):
    
#     def __init__(self,
#                 name: str,
#                 damage: int,
#                 type: str
#                 ) -> None:
        
#         """
#         Initialize a weapon item with a name, damage value, and type.

#         Args:
#         - name (str): The name of the weapon.
#         - damage (int): The damage value of the weapon.
#         - type (str): The type of the weapon (e.g., Sharp, Blunt).
#         """
        
#         super().__init__(name, 'Weapon')
#         self.damage = damage
#         self.type = type

    
#     def __str__(self) -> str:
#         """
#         Return a string representation of the weapon.

#         Returns:
#         - str: String representation of the weapon.
#         """
#         return f'{self.name} (Weapon - Damage: {self.damage})'




# class Shield(Item):
#     def __init__(self,
#                 name: str,
#                 defense: int
#                 ) -> None:
#         """
#         Initialize a shield item with a name and defense value.

#         Args:
#         - name (str): The name of the shield.
#         - defense (int): The defense value of the shield.
#         """
        
#         super().__init__(name, 'Shield')
        
#         self.defense = defense

#     def __str__(self) -> str:
#         """
#         Return a string representation of the shield.

#         Returns:
#         - str: String representation of the shield.
#         """
#         return f'{self.name} (Shield - Defense: {self.defense})'

# wooden_shield= Shield(name='Wooden shield',defense=3)

class Item:
    def __init__(self,
                 name: str,
                 item_type: str,
                 description: str = None,  # Optional description for miscellaneous items
                 damage: int = None,        # Optional damage value for weapons
                 defense: int = None        # Optional defense value for shields
                 ) -> None:
        """
        Initialize an item with a name, type, and optional attributes.

        Args:
        - name (str): The name of the item.
        - item_type (str): The type of the item (e.g., Weapon, Shield, Other).
        - description (str, optional): Description for miscellaneous items.
        - damage (int, optional): Damage value for weapons.
        - defense (int, optional): Defense value for shields.
        """
        self.name = name
        self.item_type = item_type
        self.description = description
        self.damage = damage
        self.defense = defense

    def __str__(self) -> str:
        """
        Return a string representation of the item.

        Returns:
        - str: String representation of the item.
        """
        if self.item_type == 'Weapon':
            return f'{self.name} (Weapon - Damage: {self.damage})'
        elif self.item_type == 'Shield':
            return f'{self.name} (Shield - Defense: {self.defense})'
        elif self.item_type == 'Other':
            return f'{self.name} (Other - {self.description})'
        return f'{self.name} ({self.item_type})'

class Weapon(Item):
    def __init__(self,
                name: str,
                damage: int,
                type: str
                ) -> None:
        """
        Initialize a weapon item with a name, damage value, and type.

        Args:
        - name (str): The name of the weapon.
        - damage (int): The damage value of the weapon.
        - type (str): The type of the weapon (e.g., Sharp, Blunt).
        """
        super().__init__(name=name, item_type='Weapon', damage=damage)
        self.type = type

    def __str__(self) -> str:
        """
        Return a string representation of the weapon.

        Returns:
        - str: String representation of the weapon.
        """
        return f'{self.name} (Weapon - Damage: {self.damage}, Type: {self.type})'

class Shield(Item):
    def __init__(self,
                name: str,
                defense: int
                ) -> None:
        """
        Initialize a shield item with a name and defense value.

        Args:
        - name (str): The name of the shield.
        - defense (int): The defense value of the shield.
        """
        super().__init__(name=name, item_type='Shield', defense=defense)

    def __str__(self) -> str:
        """
        Return a string representation of the shield.

        Returns:
        - str: String representation of the shield.
        """
        return f'{self.name} (Shield - Defense: {self.defense})'



class ItemGenerator:
    def __init__(self, api_key: str, model_name: str):
        self.chat = ChatGroq(temperature=0.3, groq_api_key=api_key, model_name=model_name)

    def generate_item_details(self, current_story_state: str) -> dict:
        item_prompt = ChatPromptTemplate.from_template(
            template="""
            You are an AI Dungeon Master in a text-based RPG game. The current story state is as follows:
            {current_story_state}

            if the story says that the player found/got/aquired an item then generate it, for example if a player got a torch you generate the details for it

            Generate an item with the following details:
            - Name
            - Type (e.g., Weapon, Shield, Other)
            - Additional attributes (e.g., Damage for Weapon, Defense for Shield)
            - Description (for items without specific attributes)

            Return in JSON format and nothing more.
            Example for Weapon: "name": "Magic Sword", "item_type": "Weapon", "damage": 10, "type": "Sharp"
            Example for Shield: "name": "Iron Shield", "item_type": "Shield", "defense": 5
            Example for Other: "name": "Torch", "item_type": "Other", "description": "A basic torch for light"
            """
        )
        chain = (
            {"current_story_state": RunnablePassthrough()}
            | item_prompt
            | self.chat
            | StrOutputParser()
        )
        item_details = chain.invoke({"current_story_state": current_story_state})
        return json.loads(item_details)

    def generate_item_from_story(self, current_story_state: str) -> Item:
        item_details = self.generate_item_details(current_story_state)
        item_type = item_details.get("item_type")
        
        if item_type == "Weapon":
            return Weapon(
                name=item_details["name"], 
                damage=item_details["damage"], 
                type=item_details["type"]
            )
        elif item_type == "Shield":
            return Shield(
                name=item_details["name"], 
                defense=item_details["defense"]
            )
        elif item_type == "Other":
            # Handle other types of items (e.g., potions, torches)
            return Item(
                name=item_details["name"], 
                item_type=item_type
            )
        return None
    

sword =  Weapon(name='Sword',type='Sharp',damage=4)
mace =  Weapon(name='Mace',type='Blunt',damage=6)
dagger =  Weapon(name='Dagger',type='Sharp',damage=2)
fist =  Weapon(name='Fist',type='Blunt',damage=1)
wooden_shield= Shield(name='Wooden shield',defense=3)
