from src.character import Character


class TestCharacter:
    def test_character_initial_state(self):
        character = Character(level=1, health=1000)

        assert character.level == 1
        assert character.health == 1000
        assert character.is_alive() is True

    def test_character_damages_another_character(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=1000)

        character1.damage(character2, 100)

        assert character1.health == 1000
        assert character2.health == 900

    def test_character_dies_when_health_reaches_zero(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=100)

        character1.damage(character2, 100)

        assert character2.health == 0
        assert character2.is_alive() is False

    def test_character_heals_another_character(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=800)

        character1.heal(character2, 100)

        assert character2.health == 900

    def test_character_cannot_be_healed_above_maximum_health(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=950)

        character1.heal(character2, 100)

        assert character2.health == 1000

    def test_a_dead_character_cannot_be_healed(self):
        character1 = Character(level=1, health=1000)
        character2 = Character(level=1, health=0)

        character1.heal(character2, 100)

        assert character2.health == 0
        assert character2.is_alive() is False

    # # --- Iteration 2
    #
    # def test_a_character_cannot_damage_itself(self):
    #     character1 = Character(level=1, health=1000)
    #
    #     character1.damage(character1, 100)
    #
    #     assert character1.health == 1000
    #
    # def test_a_character_can_heal_itself(self):
    #     character1 = Character(level=1, health=900)
    #
    #     character1.heal(character1, 100)
    #
    #     assert character1.health == 1000
    #
    # def test_a_character_can_only_heal_itself(self):
    #     character1 = Character(level=1, health=1000)
    #     character2 = Character(level=1, health=900)
    #
    #     character1.heal(character2, 100)
    #
    #     assert character1.health == 900
    #
    # @pytest.mark.parametrize("level", [6, 7])
    # def test_damage_is_reduced_by_50_percent_when_target_is_5_levels_above(self, level):
    #     character1 = Character(level=1, health=1000)
    #     character2 = Character(level=level, health=1000)
    #
    #     character1.deal(character2, 100)
    #
    #     assert character1.health == 950
    #
    # @pytest.mark.parametrize("level", [6, 7])
    # def test_damage_is_increased_by_50_percent_when_target_is_5_levels_below(self, level):
    #     character1 = Character(level=level, health=1000)
    #     character2 = Character(level=1, health=1000)
    #
    #     character1.deal(character2, 100)
    #
    #     assert character1.health == 850
    #
    # # --- Iteration 3
    # @pytest.mark.parametrize("type", [CharacterType.MELEE, CharacterType.RANGED])
    # def test_character_initial_state(self, type: CharacterType):
    #     character = Character(level=1, health=1000, type=type)
    #
    #     assert character.level == 1
    #     assert character.health == 1000
    #     assert character.is_alive() is True
    #     assert character.type == type



