from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from character_creation import Hero
import json
import os
from dotenv import load_dotenv

API_KEY = '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'
MODEL_NAME = 'llama3-70b-8192'

class StoryGenerator:
    def __init__(self, api_key: str, model_name: str):
        self.chat = ChatGroq(temperature=0.3, groq_api_key=api_key, model_name=model_name)

    def generate_story(self, conversation_history: str, current_story_state: str,hero: Hero,inventory: str) -> str:
        story_prompt = ChatPromptTemplate.from_template(
            template="""
            You are an AI Dungeon Master in a text-based RPG game. 
            The current state is as follows:

            Conversation history: {conversation_history}
            Current story state: {current_story_state}
            The current Hero is this:
            {hero_details}
            
            Hero inventory:
            {inventory}

            Always follow these rules:
            1. If the player acquires a new item, always say: "New Item acquired!"
            2. If the player loses or uses an item, always say: "Item removed from inventory: item name, the item name should be exactly the name in the inventory"
            3. If the player's health changes, say: "The player recovers (number) health" or "The player loses (number) health."
            4. If combat starts, always say: "Starting Combat!"
            5. Do not make choices for the player, only suggest options.
            6. Do not say what i have in the inventory nor what i'm equiped with in this story

            Respond to the player's actions based on the current state and conversation history.
            """
        )
        prompt = story_prompt
        hero_details= str(hero)
        inventory=str([item.name for item in hero.inventory.items])
        chain = (
            {"conversation_history": RunnablePassthrough(), "current_story_state": RunnablePassthrough(),"hero_details":RunnablePassthrough(),"inventory":RunnablePassthrough()} 
            | prompt
            | self.chat
            | StrOutputParser()
        )
        response = chain.invoke({
            "conversation_history": conversation_history,
            "current_story_state": current_story_state,
            "hero_details": hero_details,
            "inventory": inventory
        })
        print(inventory,"inventory debug")
        return response

class EnemyGenerator:
    def __init__(self, api_key: str, model_name: str):
        self.chat = ChatGroq(temperature=0, groq_api_key=api_key, model_name=model_name)

    def generate_enemy_details(self, current_story_state: str, hero: Hero) -> dict:
        story_prompt = ChatPromptTemplate.from_template(
            template="""
            You are an AI Dungeon Master in a text-based RPG game. The current story state is as follows:
            {current_story_state}

            The current Hero is this:
            {hero_details}
            when generating the enemy balance it accordinly to the hero, don't make it easy, but also not that hard
            

            Generate an enemy character with the following details:
            - Name
            - Health
            - Base damage
            - Base defense
            - Job
            - Weapon
            - Shield

            and pass it in a valid json format and nothing more
            example:"name": "Gorthok the Unyielding",
              "health": 25,
                "base_damage": 8, 
                "base_defense": 4,
                  "job": "Goblin Warrior",
                    "weapon": "Crude Spear", 
                    "shield": "Rusty Buckler"
            aways use this format

            """
        )
        hero_details= str(hero)
        chain = (
            {"current_story_state": RunnablePassthrough(),"hero_details":RunnablePassthrough()}
            | story_prompt
            | self.chat
            | StrOutputParser()
        )

        generated_details = chain.invoke({"current_story_state": current_story_state,"hero_details":hero_details})
        print(generated_details)
        return json.loads(generated_details)



# class ItemGenerator:
#     def __init__(self, api_key: str, model_name: str):
#         self.chat = ChatGroq(temperature=0.6, groq_api_key=api_key, model_name=model_name)

#     def generate_item_details(self, current_story_state: str, hero: Hero) -> dict:
#         story_prompt = ChatPromptTemplate.from_template(
#             template="""
#             You are an AI Dungeon Master in a text-based RPG game. The current story state is as follows:
#             {current_story_state}

#             The current Hero is this:
#             {hero_details}

#             Generate an item with the following details:
#             - Name
#             - Type (e.g., Weapon, Shield, Potion, etc.)
            
#             - Attributes (Damage, Defense)

#             and pass it in a valid json format and nothing more
#             example: 
#               "name": "Elven Sword",
#               "type": "Weapon",
#               "damage": 10
              
#             always use this format
#             """
#         )
#         hero_details = str(hero)
#         chain = (
#             {"current_story_state": RunnablePassthrough(), "hero_details": RunnablePassthrough()}
#             | story_prompt
#             | self.chat
#             | StrOutputParser()
#         )

#         generated_details = chain.invoke({"current_story_state": current_story_state, "hero_details": hero_details})
#         print(generated_details)
#         return json.loads(generated_details)


# class ItemGenerator:
#     def __init__(self, api_key: str, model_name: str):
#         self.chat = ChatGroq(temperature=0.6, groq_api_key=api_key, model_name=model_name)

#     def generate_item_details(self, current_story_state: str) -> dict:
#         item_prompt = ChatPromptTemplate.from_template(
#             template="""
#             You are an AI Dungeon Master in a text-based RPG game. The current story state is as follows:
#             {current_story_state}

#             Generate an item with the following details:
#             - Name
#             - Type (e.g., Weapon, Shield, Misc)
#             - Additional attributes (e.g., Damage for Weapon, Defense for Shield)
#             - Description (for items without specific attributes)

#             Return in JSON format and nothing more.
#             Example for Weapon: {"name": "Magic Sword", "item_type": "Weapon", "damage": 10, "type": "Sharp"}
#             Example for Shield: {"name": "Iron Shield", "item_type": "Shield", "defense": 5}
#             Example for Misc: {"name": "Torch", "item_type": "Misc", "description": "A basic torch for light"}
#             """
#         )
#         chain = (
#             {"current_story_state": RunnablePassthrough()}
#             | item_prompt
#             | self.chat
#             | StrOutputParser()
#         )
#         item_details = chain.invoke({"current_story_state": current_story_state})
#         return json.loads(item_details)

#     def generate_item_from_story(self, current_story_state: str) -> Item:
#         item_details = self.generate_item_details(current_story_state)
#         item_type = item_details.get("item_type")
        
#         if item_type == "Weapon":
#             return Weapon(
#                 name=item_details["name"], 
#                 damage=item_details["damage"], 
#                 type=item_details["type"]
#             )
#         elif item_type == "Shield":
#             return Shield(
#                 name=item_details["name"], 
#                 defense=item_details["defense"]
#             )
#         elif item_type == "Misc":
#             # Handle other types of items (e.g., potions, torches)
#             return Item(
#                 name=item_details["name"], 
#                 item_type=item_type
#             )
#         return None












# if __name__ == "__main__":
#     story_generator = StoryGenerator(API_KEY, MODEL_NAME)
#     enemy_generator = EnemyGenerator(API_KEY, MODEL_NAME)

#     conversation_history = "Player enters the forest..."
#     current_story_state = "It is dark and foggy. The player hears strange noises."

#     story_continuation = story_generator.generate_story(conversation_history, current_story_state)
#     print(story_continuation)

#     enemy_details = enemy_generator.generate_enemy_details(current_story_state)
#     print(enemy_details)
