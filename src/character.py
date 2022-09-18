from enum import Enum


class CharacterType(Enum):
    RANGED = "RANGED"
    MELEE = "MELEE"


class Character:
    max_attack_ranged: float

    def __init__(self, level: int, health: int, type: "CharacterType" = CharacterType.MELEE):
        self.max_attack_ranged = 2 if type == CharacterType.MELEE else 20
        self.type = type
        self.level = level
        self.health = health

    def is_alive(self):
        return self.health > 0

    def damage(self, target: "Character", amount: int, targetDistance: float):
        damage = amount
        if self is target or targetDistance > self.max_attack_ranged:
            return

        if (target.level - self.level) >= 5:
            damage = amount * 0.5
        elif (target.level - self.level) <= -5:
            damage = amount * 1.5

        target.health -= damage

    def heal(self, character: "Character", amount: int):
        if not character.is_alive() or character is not self:
            return

        character.health += amount

        if character.health > 1000:
            character.health = 1000
