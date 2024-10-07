# one_chat/one_chat.py

from .message_sender import MessageSender
from .broadcast_sender import BroadcastSender

class OneChat:
    def __init__(self, authorization_token):
        self.message_sender = MessageSender(authorization_token)
        self.broadcast_sender = BroadcastSender(authorization_token)

    def send_message(self, to, bot_id, message, custom_notification=None):
        return self.message_sender.send_message(to, bot_id, message, custom_notification)

    def broadcast_message(self, bot_id, to, message):
        return self.broadcast_sender.broadcast_message(bot_id, to, message)