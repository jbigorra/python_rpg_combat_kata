from enum import Enum


class CharacterType(Enum):
    RANGED = "RANGED"
    MELEE = "MELEE"


class CharacterConfig:
    LEVEL = 1
    MAXIMUM_HEALTH = 1000
    TYPE = CharacterType.MELEE
    RANGED_MAX_ATTACK_RANGE = 20
    MELEE_MAX_ATTACK_RANGE = 2


class Character:
    max_attack_ranged: float

    def __init__(self, level: int, health: int, type: "CharacterType" = CharacterType.MELEE):
        self.max_attack_ranged = (
            CharacterConfig.MELEE_MAX_ATTACK_RANGE
            if type == CharacterType.MELEE
            else CharacterConfig.RANGED_MAX_ATTACK_RANGE
        )
        self.type = type
        self.level = level
        self.health = health

    def is_alive(self):
        return self.health > 0

    def damage(self, target: "Character", amount: int, target_distance: float):
        damage = amount
        if self is target or target_distance > self.max_attack_ranged:
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

        if character.health > CharacterConfig.MAXIMUM_HEALTH:
            character.health = CharacterConfig.MAXIMUM_HEALTH
