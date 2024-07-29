from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from character_creation import Hero
import json

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














