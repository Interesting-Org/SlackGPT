from Handler import Handler
from Logger import *
from Question import Question
from chatgpt_wrapper import ChatGPT
import time
from ChatBotThread import ChatBotThread

class ChatGPTAPI(ChatBotThread):
    def __init__(self, handler: Handler, browser: str, prefix: str = "!", headless: bool = True):
        """Inherits from threading.Thread and is used to run ChatGPT in a separate thread

        Args:
            handler (Handler): The handler to use in the main thread
            browser (str): The browser playwright should use
            headless (bool, optional): Whether to run ChatGPT in headless mode. Defaults to True.
        """
        super().__init__(handler,
            browser, 
            prefix, 
            headless
        )
        self.create_bot = lambda: ChatGPT(browser=self.browser, headless=self.headless)

    def ask(self, question: Question):
        self.lg.log(f"Asking ChatGPT with prompt {question.text[(len(self.prefix) if not question.direct_message else 0):]}")
        if not question.user.conversation_id is None:
            self.bot.conversation_id = question.user.conversation_id
        start = time.time()
        question.answer(self.bot.ask(question.text[(len(self.prefix) if not question.direct_message else 0):]))
        self.lg.info(f"Answered {question.username} in {time.time() - start} seconds")
        question.user.conversation_id = self.bot.conversation_id
        