import pytest

from src.character import Character, CharacterType, CharacterConfig


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


class TestCharacter:
    def test_character_initial_state(self):
        character = Character(level=1, health=1000)

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True

    def test_melee_character_initial_state(self):
        character = Character(level=1, health=1000)

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character.max_attack_ranged == CharacterConfig.MELEE_MAX_ATTACK_RANGE
        assert character.type == CharacterType.MELEE

    def test_ranged_character_initial_state(self):
        character = Character(level=1, health=1000, type=CharacterType.RANGED)

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character.max_attack_ranged == CharacterConfig.RANGED_MAX_ATTACK_RANGE
        assert character.type == CharacterType.RANGED

    def test_character_damages_another_character(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=1000)

        character1.damage(character2, 100, 1)

        assert character1.health == 1000
        assert character2.health == 900

    def test_character_dies_when_health_reaches_zero(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=100)

        character1.damage(character2, 100, 1)

        assert character2.health == 0
        assert character2.is_alive() is False

    def test_character_cannot_be_healed_above_maximum_health(self):
        character = Character(level=1, health=950)

        character.heal(character, 100)

        assert character.health == 1000

    def test_a_dead_character_cannot_be_healed(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=0)

        character1.heal(character2, 100)

        assert character2.health == 0
        assert character2.is_alive() is False

    # --- Iteration 2

    def test_a_character_cannot_damage_itself(self):
        character1 = Character(level=1, health=1000)

        character1.damage(character1, 100, 1)

        assert character1.health == 1000

    def test_a_character_can_heal_itself(self):
        character1 = Character(level=1, health=900)

        character1.heal(character1, 100)

        assert character1.health == 1000

    def test_a_character_can_only_heal_itself(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=900)

        character1.heal(character2, 100)

        assert character2.health == 900

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_reduced_by_50_percent_when_target_is_5_levels_above(self, level):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=level, health=1000)

        character1.damage(character2, 100, 1)

        assert character2.health == 950

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_increased_by_50_percent_when_target_is_5_levels_below(self, level):
        character1 = Character(level=level, health=1000)
        character2 = Character(level=1, health=1000)

        character1.damage(character2, 100, 1)

        assert character2.health == 850

    # Iteration 3

    def test_melee_character_cannot_damage_another_character_out_of_range(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=1000)

        character1.damage(character2, 100, 3)

        assert character2.health == 1000

    def test_ranged_character_cannot_damage_another_character_out_of_range(self):
        character1 = Character(level=1, health=1000, type=CharacterType.RANGED)
        character2 = Character(level=1, health=1000, type=CharacterType.MELEE)

        character1.damage(character2, 100, 21)

        assert character2.health == 1000


