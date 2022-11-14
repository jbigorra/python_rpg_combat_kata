import pytest

from src.character import Character, CharacterType, CharacterConfig
from tests.factories.character import CharacterFactory


class TestCharacter:
    def test_character_initial_state(self):
        character = Character(level=1, health=1000, position=1)

        assert character._level == CharacterConfig.LEVEL
        assert character._health == CharacterConfig.MAXIMUM_HEALTH
        assert character.position() == CharacterConfig.POSITION
        assert character.is_alive() is True

    def test_melee_character_initial_state(self):
        character = CharacterFactory().build()

        assert character._level == CharacterConfig.LEVEL
        assert character._health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character._max_attack_ranged == CharacterConfig.MELEE_MAX_ATTACK_RANGE
        assert character._type == CharacterType.MELEE

    def test_ranged_character_initial_state(self):
        character = CharacterFactory()\
            .setup_base_ranged_character()\
            .build()

        assert character._level == CharacterConfig.LEVEL
        assert character._health == CharacterConfig.MAXIMUM_HEALTH
        assert character.is_alive() is True
        assert character._max_attack_ranged == CharacterConfig.RANGED_MAX_ATTACK_RANGE
        assert character._type == CharacterType.RANGED

    def test_character_damages_another_character(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().build()

        character1.damage(character2, 100)

        assert character1._health == 1000
        assert character2._health == 900

    def test_character_dies_when_health_reaches_zero(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(100).build()

        character1.damage(character2, 100)

        assert character2._health == 0
        assert character2.is_alive() is False

    def test_character_cannot_be_healed_above_maximum_health(self):
        character = CharacterFactory().with_health(950).build()

        character.heal(character, 100)

        assert character._health == 1000

    def test_a_dead_character_cannot_be_healed(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(0).build()

        character1.heal(character2, 100)

        assert character2._health == 0
        assert character2.is_alive() is False

    # --- Iteration 2

    def test_a_character_cannot_damage_itself(self):
        character1 = CharacterFactory().build()

        character1.damage(character1, 100)

        assert character1._health == 1000

    def test_a_character_can_heal_itself(self):
        character1 = CharacterFactory().with_health(900).build()

        character1.heal(character1, 100)

        assert character1._health == 1000

    def test_a_character_can_only_heal_itself(self):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_health(900).build()

        character1.heal(character2, 100)

        assert character2._health == 900

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_reduced_by_50_percent_when_target_is_5_levels_above(self, level):
        character1 = CharacterFactory().build()
        character2 = CharacterFactory().with_level(level).build()

        character1.damage(character2, 100)

        assert character2._health == 950

    @pytest.mark.parametrize("level", [6, 7])
    def test_damage_is_increased_by_50_percent_when_target_is_5_levels_below(self, level):
        character1 = CharacterFactory().with_level(level).build()
        character2 = CharacterFactory().build()

        character1.damage(character2, 100)

        assert character2._health == 850

    # Iteration 3

    def test_melee_character_cannot_damage_another_character_out_of_range(self):
        melee_character = CharacterFactory().build()
        enemy_out_of_range = CharacterFactory().with_position(3).build()

        melee_character.damage(enemy_out_of_range, 100)

        assert enemy_out_of_range._health == 1000

    def test_ranged_character_cannot_damage_another_character_out_of_range(self):
        ranged_character = CharacterFactory().setup_base_ranged_character().build()
        enemy_out_ranged = CharacterFactory().with_position(21).build()

        ranged_character.damage(enemy_out_ranged, 100)

        assert enemy_out_ranged._health == 1000

    # Iteration 4

    def test_new_characters_belong_to_no_faction(self):
        character = CharacterFactory().build()

        assert len(character.factions()) == 0

    def test_a_character_can_join_one_faction(self):
        character = CharacterFactory().build()

        character.join_faction(['FACTION_1'])

        assert len(character.factions()) == 1
        assert character.factions()[0] == 'FACTION_1'

    def test_a_character_can_join_more_than_one_faction(self):
        character = CharacterFactory().with_factions(['FACTION_1']).build()

        character.join_faction(['FACTION_2'])

        assert len(character.factions()) == 2
        assert character.factions()[0] == 'FACTION_1'
        assert character.factions()[1] == 'FACTION_2'

    def test_a_character_can_leave_one_faction(self):
        character = CharacterFactory()\
            .with_factions(['FACTION_1', 'FACTION_2', 'FACTION_3'])\
            .build()

        character.leave_faction(['FACTION_2'])

        assert len(character.factions()) == 2
        assert character.factions()[0] == 'FACTION_1'
        assert character.factions()[1] == 'FACTION_3'
