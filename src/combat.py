from character_creation import Hero, Enemy, Character
from skills import Skill
from item import mace, wooden_shield, sword

class DamageCalc:
    @staticmethod
    def calculate_damage(attacker: 'Character', target: 'Character', skill: 'Skill' = None) -> int:
        dmg = attacker.base_damage + attacker.weapon.damage
        dmg_dealt = dmg - target.total_defense
        if skill:
            target.health -= skill.power
            print(f"{attacker.name} dealt {skill.power} damage with {skill.name} to {target.name}")
        else:
            if dmg_dealt > 0:
                target.health -= dmg_dealt
            else:
                dmg_dealt = 0
            print(f"{attacker.name} dealt {dmg_dealt} damage to {target.name}")

        target.health = max(target.health, 0)

class Combat:
    def __init__(self, hero: 'Hero', enemy: 'Enemy') -> None:
        self.hero = hero
        self.enemy = enemy

    def start(self) -> None:
        print(self.hero)
        print(self.enemy)

        while self.hero.health > 0 and self.enemy.health > 0:
            self.display_health()
            match Combat.menu_combat().split():
                case ['1']:
                    self.fight_menu()
                    user_input = input('What is your choice?: ')
                    
                    match user_input:
                        case '0':
                            continue
                        
                        case '1':
                            DamageCalc.calculate_damage(self.hero, self.enemy)
                            if self.enemy.health > 0:
                                DamageCalc.calculate_damage(self.enemy, self.hero)
                        
                        case skills:
                            
                            if skills[0].isdigit():
                                skill_index = int(skills[0])
                            
                                if 2 <= skill_index < 2 + len(self.hero.skills):
                                    selected_skill = self.hero.skills[skill_index - 2]
                                    DamageCalc.calculate_damage(self.hero, self.enemy, selected_skill)
                            
                                    if self.enemy.health > 0:
                                        DamageCalc.calculate_damage(self.enemy, self.hero)
                            
                                else:
                                    print("Invalid Choice, that skill doesn't exist!")
                            else:
                                print('Invalid choice, please type only the option number!')
        return self.result()

    @staticmethod
    def menu_combat() -> str:
        print("""
            [1] - Fight    [3] - Open inventory
            [2] - Run    
        """)
        return input('What is your choice?: ')

    def fight_menu(self) -> None:
        Skills = ""
        for index, skill in enumerate(self.hero.skills, start=2):
            Skills += f'            [{index}] - {skill.name}\n' 
        print(f"""
            [0] - Menu
            [1] - Attack    
{Skills}     
        """)

    def display_health(self) -> None:
        print(f"Hero's health {self.hero.health}")
        print(f"Foe's health {self.enemy.health}")

    def result(self) -> None:
        if self.hero.health > 0:
            print(f'{self.hero.name} won the battle!')
            return True 
        else:
            print(f'The {self.enemy.name} won the battle')
            return False
        print(self.hero)

# if __name__ == "__main__":
#     hero = Hero(name='Fabio', health=40, base_damage=1, base_defense=2, job='monk')
#     hero.equip(sword)
#     hero.equip(mace)
#     smite = Skill(name="Smite", power=10, description="Deals holy damage.")
#     bash = Skill(name="Bash", power=10, description="Hits the enemy with full force and has a chance to stun him.")
#     hero.add_skill(smite)
#     hero.add_skill(bash)
#     hero.equip(wooden_shield)

#     enemy = Enemy(name='Goblin', health=30, base_damage=3, base_defense=1, job='warrior', weapon=sword, shield=wooden_shield)

#     combat = Combat(hero, enemy)
#     combat.start()
