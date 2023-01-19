from typing import List
from Question import Question

class User:
    def __init__(self, username: str):
        """Represents a user in the handler

        Args:
            username (str): The username of the user
        """
        self.username = username
        self.conversation_id = None # The conversation id from ChatGPT

    def __str__(self):
        return f"User({self.username}) -> {self.conversation_id}"
