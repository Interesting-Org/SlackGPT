from QuestionHandler import QuestionHandler
from Logger import *
from Question import Question
from chatgpt_wrapper import ChatGPT
import time
from ChatBotThread import ChatBotThread

class ChatGPTAPI(ChatBotThread):
    def __init__(self, handler: QuestionHandler, browser: str, prefix: str = "!", headless: bool = True):
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
        self.lg.log(f"Asking ChatGPT with prompt {question.text}")
        if not question.user.conversation_id is None:
            self.bot.conversation_id = question.user.conversation_id
        start = time.time()
        question.answer(self.bot.ask(question.text))
        self.lg.info(f"Answered {question.username} in {time.time() - start} seconds")
        question.user.conversation_id = self.bot.conversation_id

    def fail_behaviour(self, question: Question, exception: Exception) -> None:
        if "Execution context was destroyed" in str(exception):
            self.handler.add_new_question(question, 0)
            question.user.conversation_id = None
            self.lg.warning(f"Execution context was destroyed. Reinserting question into queue")
        question.answer(f"An error occured while asking the ChatBot the question. Please try again later. \n{exception.with_traceback}")
        