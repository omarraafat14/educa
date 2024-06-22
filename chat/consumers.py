import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connections
        self.accept()

    def disconnect(self, close_code):
        # close connections
        pass

    # receive messages from websocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # send message to websocket
        self.send(text_data=json.dumps({"message": message}))
