import pytest

from src.character import Character, CharacterType, CharacterConfig
from tests.factories.character import CharacterFactory


class TestCharacter:
    def test_character_initial_state(self):
        character = Character(level=1, health=1000, position=1)

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.position() == CharacterConfig.POSITION
        assert character.is_alive() is True

    def test_melee_character_initial_state(self):
        character = CharacterFactory().build()

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character.max_attack_ranged == CharacterConfig.MELEE_MAX_ATTACK_RANGE
        assert character.type == CharacterType.MELEE

    def test_ranged_character_initial_state(self):
        character = CharacterFactory()\
            .setup_base_ranged_character()\
            .build()

        assert character.level == CharacterConfig.LEVEL
        assert character.health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character.max_attack_ranged == CharacterConfig.RANGED_MAX_ATTACK_RANGE
        assert character.type == CharacterType.RANGED

    def test_character_damages_another_character(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().build()

        character1.damage(character2, 100)

        assert character1.health == 1000
        assert character2.health == 900

    def test_character_dies_when_health_reaches_zero(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(100).build()

        character1.damage(character2, 100)

        assert character2.health == 0
        assert character2.is_alive() is False

    def test_character_cannot_be_healed_above_maximum_health(self):
        character = CharacterFactory().with_health(950).build()

        character.heal(character, 100)

        assert character.health == 1000

    def test_a_dead_character_cannot_be_healed(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(0).build()

        character1.heal(character2, 100)

        assert character2.health == 0
        assert character2.is_alive() is False

    # --- Iteration 2

    def test_a_character_cannot_damage_itself(self):
        character1 = CharacterFactory().build()

        character1.damage(character1, 100)

        assert character1.health == 1000

    def test_a_character_can_heal_itself(self):
        character1 = CharacterFactory().with_health(900).build()

        character1.heal(character1, 100)

        assert character1.health == 1000

    def test_a_character_can_only_heal_itself(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(900).build()

        character1.heal(character2, 100)

        assert character2.health == 900

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_reduced_by_50_percent_when_target_is_5_levels_above(self, level):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_level(level).build()

        character1.damage(character2, 100)

        assert character2.health == 950

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_increased_by_50_percent_when_target_is_5_levels_below(self, level):
        character1 = CharacterFactory().with_level(level).build()
        character2 = CharacterFactory().build()

        character1.damage(character2, 100)

        assert character2.health == 850

    # Iteration 3

    def test_melee_character_cannot_damage_another_character_out_of_range(self):
        melee_character = CharacterFactory().build()
        enemy_out_of_range = CharacterFactory().with_position(3).build()

        melee_character.damage(enemy_out_of_range, 100)

        assert enemy_out_of_range.health == 1000

    def test_ranged_character_cannot_damage_another_character_out_of_range(self):
        ranged_character = CharacterFactory().setup_base_ranged_character().build()
        enemy_out_ranged = CharacterFactory().with_position(21).build()

        ranged_character.damage(enemy_out_ranged, 100)

        assert enemy_out_ranged.health == 1000


