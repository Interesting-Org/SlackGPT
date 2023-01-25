
class Message:
    def __init__(self, payload: dict) -> None:
        self.message = payload["event"]["text"]
        self.event_id = payload["event_id"]
        self.payload = payload