# one_chat/one_chat.py

from .message_sender import MessageSender
from .broadcast_sender import BroadcastSender
from .location_sender import LocationSender

class OneChat:
    def __init__(self, authorization_token):
        self.message_sender = MessageSender(authorization_token)
        self.broadcast_sender = BroadcastSender(authorization_token)
        self.location_sender = LocationSender(authorization_token)

    def send_message(self, to, bot_id, message, custom_notification=None):
        return self.message_sender.send_message(to, bot_id, message, custom_notification)

    def broadcast_message(self, bot_id, to, message):
        return self.broadcast_sender.broadcast_message(bot_id, to, message)

    def send_location(self, to, bot_id, latitude, longitude, address, custom_notification=None):
        return self.location_sender.send_location(to, bot_id, latitude, longitude, address, custom_notification)