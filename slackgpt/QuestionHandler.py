from typing import List
from flask import Response
from User import User
from Queue import Queue
from Question import Question
from Logger import *
from slack_sdk import WebClient
from Message import Message

class QuestionHandler:
    def __init__(self, client: WebClient) -> None:
        """Represents a handler for the questions, users and queue
        """
        self.messages: List[Message] = []
        self.users: List[User] = []
        self.queue: Queue = Queue()
        self.client = client
        self.lg = Logger("QuestionHandler", level=Level.INFO, formatter=Logger.minecraft_formatter, handlers=[FileHandler.latest_file_handler(Logger.minecraft_formatter), main_file_handler])
        self.waiting_messages = []

    def append_message(self, message_id: str) -> None:
        self.messages.append(message_id)

    def get_user(self, username: str) -> User:
        """Returns either an existing user or a new user object

        Args:
            username (str): The username for the user object

        Returns:
            User: The user object
        """
        return [user for user in self.users if user.username == username][0] if username in [user.username for user in self.users] else User(username)

    def process_message(self, payload: dict, username) -> Response:
        """Handles the question from the user and replies to it

        Args:
            event (dict): The event extracted from the payload
            username (str): The username of the user

        Returns:
            Response: The response for the Slack API
        """	
        event = payload["event"]
        message = event["text"]
        user = self.get_user(username)
        try:
            question = Question(event["channel"], username, message, user, event["ts"], self.client, direct_message=event["channel_type"] == "im")
            question.send_pre_answer()
            self.add_new_question(question)
            self.lg.info(f"Added {username} to queue")
            return Response("OK", status=200)
        except Exception as e:
            self.lg.error(e)
            self.client.chat_postMessage(channel=event["channel"], text=f"An error occurred while processing your message. Please try again later. \n{e}")
            return Response("An error occurred. Please try again later.", status=500)

    def is_unique_message(self, payload: dict) -> bool:
        """Checks whether the message event has already been registered

        Args:
            payload (dict): The payload of the event

        Returns:
            bool: Whether the message event has already been registered
        """
        return not payload["event_id"] in [message.event_id for message in self.messages]

    def add_new_question(self, question: Question, index: int = None) -> None:
        """Adds a new question to the queue

        Args:
            question (Question): The question to add
            index (int, optional): The index to add the question to. Defaults to None.
        """
        if index:
            self.queue.insert(index, question)
        else:
            self.queue.push(question)

    def get_question(self) -> Question:
        """Returns the question of the user

        Args:
            username (str): The username of the user

        Returns:
            Question: The question of the user
        """
        return self.queue.pop()
