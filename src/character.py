class Character:
    def __init__(self, level: int, health: int):
        self.level = level
        self.health = health

    def is_alive(self):
        return self.health > 0

    def damage(self, character: "Character", amount: int):
        character.health -= amount

    def heal(self, character: "Character", amount: int):
        if not character.is_alive():
            return

        character.health += amount

        if character.health > 1000:
            character.health = 1000
