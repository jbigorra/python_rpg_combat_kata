from src.character import CharacterConfig, CharacterType, Character


class CharacterFactory:
    level: int = CharacterConfig.LEVEL
    health: int = CharacterConfig.MAXIMUM_HEALTH
    type: CharacterType = CharacterConfig.TYPE

    def _reset_state(self):
        self.level = CharacterConfig.LEVEL
        self.health = CharacterConfig.MAXIMUM_HEALTH
        self.type = CharacterConfig.TYPE

    def with_level(self, level: int) -> "CharacterFactory":
        self.level = level
        return self

    def with_health(self, health: int) -> "CharacterFactory":
        self.health = health
        return self

    def with_type(self, type: CharacterType) -> "CharacterFactory":
        self.type = type
        return self

    def build(self) -> "Character":
        character = Character(level=self.level, health=self.health, type=self.type)
        self._reset_state()
        return character

    def setup_base_ranged_character(self) -> "CharacterFactory":
        self.level = CharacterConfig.LEVEL
        self.health = CharacterConfig.MAXIMUM_HEALTH
        self.type = CharacterType.RANGED
        return self