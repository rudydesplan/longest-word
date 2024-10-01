# Module docstring explaining the purpose of this module
"""
This module defines a simple game class that generates a random grid of uppercase
letters and checks if a given word can be formed with those letters.
"""

import string
import random
import requests

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
        Validates if the provided word can be formed with the letters in the current grid
        and exists in the dictionary.

        Args:
        word (str): The word to check.

        Returns:
        bool: True if the word can be formed and exists in the dictionary, False otherwise.
        """
        if not word:
            return False

        letters = self.grid.copy()  # Copy the grid to avoid modifying the original
        for letter in word:
            if letter in letters:
                print(f"Letter '{letter}' found in grid.")
                letters.remove(letter)  # Remove only one occurrence of the letter
                print(f"Remaining letters after removal: {letters}")
            else:
                print(f"Letter '{letter}' not found in grid.")
                return False  # Return False if there aren't enough occurrences of the letter

        return self.__check_dictionary(word)

    @staticmethod
    def __check_dictionary(word: str) -> bool:
        """
        Check if the word exists in the dictionary by calling the API.

        Args:
        word (str): The word to check.

        Returns:
        bool: True if the word exists in the dictionary, False otherwise.
        """
        try:
            response = requests.get(f"https://dictionary.lewagon.com/{word}")
            response.raise_for_status()  # Ensure the request was successful
            json_response = response.json()
            return json_response.get('found', False)
        except requests.exceptions.RequestException as e:
            print(f"Error checking dictionary: {e}")
            return False

    def refresh_grid(self) -> list:
        """
        Refreshes the grid with new random letters.
        """
        self.grid = [random.choice(string.ascii_uppercase) for _ in range(9)]
