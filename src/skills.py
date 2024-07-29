class Skill:
    def __init__(self,
                name: str,
                power: int,
                description: str
                ) -> None:
        """
        Initialize a Skill object.

        Args:
        - name (str): The name of the skill.
        - power (int): The power level of the skill.
        - description (str): A brief description of the skill.
        """
        self.name = name
        self.power = power
        self.description = description

    def __str__(self) -> str:
        """
        Return a string representation of the Skill object.

        Returns:
        - str: String representation including skill's name, power, and description.
        """
        return f'{self.name} (Power: {self.power}): {self.description}'