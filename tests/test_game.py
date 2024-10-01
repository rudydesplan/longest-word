from longest_word.game import Game
import string

class TestGame:
    def test_game_initialization(self):
            # setup
            new_game = Game()

            # exercise
            grid = new_game.grid

            # verify
            assert isinstance(grid, list)
            assert len(grid) == 9
            for letter in grid:
                assert letter in string.ascii_uppercase

    def test_empty_word_is_invalid(self):
        # setup
        new_game = Game()
        # verify
        assert new_game.is_valid('') is False

    def test_is_valid(self):
        # setup
        new_game = Game()
        test_grid = 'KWEUEAKRZ'
        test_word = 'EUREKA'
        # exercice
        new_game.grid = list(test_grid) # Force the grid to a test case
        # verify
        assert new_game.is_valid(test_word) is True
        # teardown
        assert new_game.grid == list(test_grid) # Make sure the grid remained untouched

    def test_is_invalid(self):
        # setup
        new_game = Game()
        test_grid = 'KWEUEAKRZ'
        test_word = 'SANDWICH'
        # exerice
        new_game.grid = list(test_grid) # Force the grid to a test case
        # verify
        assert new_game.is_valid(test_word) is False
        # teardown
        assert new_game.grid == list(test_grid) # Make sure the grid remained untouched

    def test_case_sensitivity(self):
        new_game = Game()
        test_grid = 'abcdefg'
        test_word = 'ABC'
        new_game.grid = list(test_grid.upper())  # Convert grid to uppercase
        assert new_game.is_valid(test_word.upper()) is True

    def test_repeated_letters(self):
        new_game = Game()
        test_grid = 'AABCC'
        test_word = 'AAC'
        new_game.grid = list(test_grid)
        assert new_game.is_valid(test_word) is True  # Should work as 'A' repeats

        test_word = 'AAA'
        assert new_game.is_valid(test_word) is False  # Should fail due to insufficient 'A's

    def test_word_longer_than_grid(self):
        new_game = Game()
        test_word = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        assert len(test_word) > len(new_game.grid)  # Ensure the word is longer
        assert new_game.is_valid(test_word) is False

    def test_refresh_grid(self):
        new_game = Game()
        original_grid = new_game.grid.copy()
        new_game.refresh_grid()
        assert new_game.grid != original_grid  # Grid should mostly change
        assert all(letter in string.ascii_uppercase for letter in new_game.grid)

    def test_non_ascii_characters(self):
        new_game = Game()
        non_ascii_word = 'Café'
        assert new_game.is_valid(non_ascii_word) is False

    def test_empty_grid(self):
        new_game = Game()
        new_game.grid = []  # Manually empty the grid
        test_word = 'TEST'
        assert new_game.is_valid(test_word) is False
