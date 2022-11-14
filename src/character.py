from enum import Enum


class CharacterType(Enum):
    RANGED = "RANGED"
    MELEE = "MELEE"


class CharacterConfig:
    POSITION = 1
    LEVEL = 1
    MAXIMUM_HEALTH = 1000
    TYPE = CharacterType.MELEE
    RANGED_MAX_ATTACK_RANGE = 20
    MELEE_MAX_ATTACK_RANGE = 2


class Character:
    _max_attack_ranged: float
    _factions: [str] = []

    def __init__(self, level: int, health: int, position: int, type: "CharacterType" = CharacterType.MELEE):
        self._position = position
        self._max_attack_ranged = (
            CharacterConfig.MELEE_MAX_ATTACK_RANGE
            if type == CharacterType.MELEE
            else CharacterConfig.RANGED_MAX_ATTACK_RANGE
        )
        self._type = type
        self._level = level
        self._health = health

    def is_alive(self) -> bool:
        return self._health > 0

    def damage(self, target: "Character", amount: int) -> None:
        damage = amount
        if self is target or target.position() > self._max_attack_ranged:
            return

        if (target._level - self._level) >= 5:
            damage = amount * 0.5
        elif (target._level - self._level) <= -5:
            damage = amount * 1.5

        target._health -= damage

    def heal(self, character: "Character", amount: int) -> None:
        if not character.is_alive() or character is not self:
            return

        character._health += amount

        if character._health > CharacterConfig.MAXIMUM_HEALTH:
            character._health = CharacterConfig.MAXIMUM_HEALTH

    def join_faction(self, new_faction: [str]):
        self._factions = new_faction

    def position(self) -> int:
        return self._position

    def factions(self) -> []:
        return self._factions
