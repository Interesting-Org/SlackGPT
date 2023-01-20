from slack_sdk.web import WebClient

class Question:
    def __init__(self, channel: str, username: str, text: str, user, ts: str, client: WebClient, direct_message: bool = False):
        """Represents a question asked by a user

        Args:
            channel (str): The channel id
            username (str): The username of the user
            text (str): The prompt for ChatGPT
        """
        self.channel = channel
        self.username = username
        self.text = text
        self.ts = ts
        self.client = client
        self.direct_message = direct_message
        self.answer_text = None # The field for the future answer by ChatGPT
        self.is_answered = False # Whether or not the question has been answered
        self.user = user # Get the user object from the handler

    def __str__(self):
        return f"Question({self.channel}, {self.username}, {self.text}, {self.ts}, {self.direct_message}, {self.is_answered}, {self.answer_text})"


    def __getitem__(self, index):
        return self

    def answer(self, answer_text: str):
        """Marks a question as answered

        Args:
            question (Question): The question to mark as answered
        """
        self.is_answered = True
        self.answer_text = answer_text
        self.send_answer()

    def answer_without_sending(self, answer_text: str):
        """Marks a question as answered without sending the answer to the user

        Args:
            question (Question): The question to mark as answered
        """
        self.is_answered = True
        self.answer_text = answer_text

    def send_answer(self) -> None:
        """Called by the handler to send the answer to the user

        Args:
            client (WebClient): The Slack WebClient
        """
        self.client.chat_postMessage(channel=self.channel, text=self.answer_text)

    def send_pre_answer(self) -> str:
        """Sent before the question is posed to ChatGPT to let the user know that the question is being processed

        Args:
            client (WebClient): The Slack WebClient

        Returns:
            str: The message id of the sent message
        """
        return ""