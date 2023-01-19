import threading
from Handler import Handler
from Logger import *
from Question import Question
import time
from Bot import Bot

class ChatBotThread(threading.Thread):

    def __init__(self, handler: Handler, browser: str, prefix: str = "!", headless: bool = True):
        """Inherits from threading.Thread and is used to run ChatGPT in a separate thread

        Args:
            handler (Handler): The handler to use in the main thread
            browser (str): The browser playwright should use
            headless (bool, optional): Whether to run ChatGPT in headless mode. Defaults to True.
        """
        super().__init__()
        self.queue = handler.queue
        self.handler = handler
        self.lg = Logger("ChatBot", level=Level.INFO, formatter=Logger.minecraft_formatter, handlers=[FileHandler.latest_file_handler(Logger.minecraft_formatter), main_file_handler])
        self.browser = browser
        self.headless = headless
        self.prefix = prefix

    def create_bot(self) -> Bot:
        return None

    def run(self) -> None:
        """The method that is run when the thread is started
        """
        self.lg.info(f"Running ChatBot Thread {self.ident}")
        self.lg.info(f"Initializing Bot")
        start = time.time()
        self.bot = self.create_bot()
        self.lg.info(f"Initialized Bot. Took {time.time() - start} seconds")
        while True:
            if len(self.queue) > 0:
                try:
                    question: Question = self.queue.pop()
                    self.lg.info(f"Processing question by {question.user}: {question.text[:30]}")
                    self.ask(question)
                except Exception as e:
                    self.lg.error(e)
                    question.answer(f"An error occured while asking the ChatBot the question. Please try again later. \n{e.with_traceback}")

    def ask(self, question: Question) -> str:
        """Write logic for API in here

        Args:
            question (Question): The question as input

        Returns:
            str: The string answer provided by the api
        """
        return ""