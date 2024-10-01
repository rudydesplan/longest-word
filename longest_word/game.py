# Module docstring explaining the purpose of this module
"""
This module defines a simple game class that generates a random grid of uppercase
letters and checks if a given word can be formed with those letters.
"""

import string
import random

class Game:
    """
    Game class to generate a grid of random letters and check the validity of words.
    """

    def __init__(self) -> list:
        """
        Initializes a new game instance by populating a 3x3 grid with random uppercase letters.
        """
        self.grid = [random.choice(string.ascii_uppercase) for _ in range(9)]

    def is_valid(self, word: str) -> bool:
        """
        Validates if the provided word can be formed with the letters in the current grid.

        Args:
        word (str): The word to check.

        Returns:
        bool: True if the word can be formed, False otherwise.
        """
        if not word:
            return False
        letters = self.grid.copy()
        for letter in word:
            if letter in letters:
                letters.remove(letter)
            else:
                return False
        return True

    def refresh_grid(self) -> list:
        """
        Refreshes the grid with new random letters.
        """
        self.grid = [random.choice(string.ascii_uppercase) for _ in range(9)]
