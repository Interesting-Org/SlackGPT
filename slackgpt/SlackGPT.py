from Logger import *
from OpenAI import OpenAIBotThread
from ChatGPTAPI import ChatGPTAPI
from ChatBotThread import ChatBotThread
from flask import Flask
from slack_sdk import WebClient
from QuestionHandler import QuestionHandler


class SlackGPT:
    def __init__(self, token, secret, app: Flask, prefix="!", model: str = "chatgpt", debug: bool =False, headless: bool =False, browser: str ="firefox"):
        self.token = token
        self.secret = secret
        self.prefix = prefix
        self.debug = debug
        self.headless = headless
        self.browser = browser
        self.client = WebClient(token)
        self.model = model
        self.client = WebClient(token)
        self.handler = QuestionHandler(self.client)
        self.lg: Logger = Logger("SlackGPT", level=Level.DEBUG if debug else Level.INFO, formatter=Logger.minecraft_formatter, handlers=[FileHandler.latest_file_handler(Logger.minecraft_formatter), FileHandler.error_file_handler(Logger.minecraft_formatter), main_file_handler])
        self.app = app
        self.happy_mode = False

    def start(self):
        self.lg.info("Starting SlackGPT")
        self.lg.debug(self.model)
        self.chatbot = self.get_chatbot(self.model)
        self.chatbot.start()
        self.app.run(debug=self.debug)

    def get_chatbot(self, model: str) -> ChatBotThread:
        if model == "chatgpt":
            return ChatGPTAPI(self.handler, self.browser, self.prefix, self.headless)
        elif model in ["text-davinci-003", "text-davinci-002", "text-davinci-001"]:
            return OpenAIBotThread(self.handler, self.browser, self.prefix, self.headless)
        else:
            raise ValueError(f"Invalid model {model}")
