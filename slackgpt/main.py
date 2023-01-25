import argparse
from SlackGPT import SlackGPT
from slackeventsapi import SlackEventAdapter
from flask import Flask, Response
from Message import Message
from Logger import *


def get_user(payload):
    event = payload["event"]
    user = slackgpt.client.users_info(user=event["user"]) # lookup the user id to get the username and profile picture
    username = user["user"]["profile"]["display_name"]
    if username == "":
        username = user["user"]["real_name"]

    return username


clg = Logger("CHAT", level=Level.WARNING, formatter=Logger.minecraft_formatter, handlers=[FileHandler(Level.LOG, Logger.minecraft_formatter, directory="./logs", generator=lambda directory, _: (directory + '/' if directory else '') + "chat.log"), main_file_handler])
def message(payload: dict):

    event = payload["event"]
    message = event["text"]

    if "bot_id" in event.keys():
        if not slackgpt.handler.is_unique_message(payload):
            return
        #if message == "I am thinking ...":
        #    slackgpt.handler.waiting_messages.append(event["ts"])
        return Response("OK", status=200)

    msg = Message(payload)
    slackgpt.handler.append_message(msg)

    username = get_user(payload)

    clg.log(f"[{event['channel']}] {username}: {event['text']}")

    if message.lower().startswith(slackgpt.prefix.lower()) or event["channel_type"] == "im":
        return slackgpt.handler.process_message(payload, username)

    elif msg.message.lower() == ".answer":
        prev_payload = slackgpt.handler.messages[-2].payload
        print(prev_payload)
        return slackgpt.handler.process_message(prev_payload, get_user(prev_payload))

    return Response("OK", status=200)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth_path", help="Specifies the path to a file containing first the Slack Bot token, then the Slack signing secret", required=False)
    parser.add_argument("--token", "-t", help="Manually specify the Slack token", required=False)
    parser.add_argument("--secret", "-s", help="Manually specify the Slack signing secret", required=False)
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging", required=False)
    parser.add_argument("--headless", action="store_true", help="Run chatgpt wrapper in headless mode", required=False)
    parser.add_argument("--browser", choices=["firefox", "chromium"], default="firefox", help="Specify the browser used by chatgpt wrapper (playwright install <browser>)", required=False)
    parser.add_argument("--prefix", default="!", help="Specify the prefix to trigger the bot", required=False)
    parser.add_argument("--model", "-m", help="The model for the slack bot to ask", choices=["text-davinci-003", "text-davinci-002", "text-davinci-001", "chatgpt"], default="chatgpt", required=False)

    args = parser.parse_args()

    if args.auth_path:
        token, secret = open(args.auth_path, "r").read().splitlines() 
    else:
        token, secret = args.token, args.secret

    
    app = Flask("SlackGPT")
    adapter = SlackEventAdapter(secret, "/slack/events", app)
    adapter.on("message")(message)
    slackgpt = SlackGPT(token=token, secret=secret, app=app, prefix=args.prefix, model=args.model, debug=args.debug, headless=args.headless, browser=args.browser)
    slackgpt.start()
    