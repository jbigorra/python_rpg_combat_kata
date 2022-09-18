class Character:
    def __init__(self, level: int, health: int):
        self.level = level
        self.health = health

    def is_alive(self):
        return self.health > 0

    def damage(self, character: "Character", damage: int):
        character.health = character.health - damage