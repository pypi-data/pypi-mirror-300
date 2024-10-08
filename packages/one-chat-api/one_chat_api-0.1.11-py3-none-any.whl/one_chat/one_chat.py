# one_chat/one_chat.py

from .message_sender import MessageSender
from .broadcast_sender import BroadcastSender
from .location_sender import LocationSender
from .sticker_sender import StickerSender


class OneChat:
    def __init__(self, authorization_token, to=None, bot_id=None):
        self.token = authorization_token
        self.default_to = to
        self.default_bot_id = bot_id
        self.message_sender = MessageSender(authorization_token)
        self.broadcast_sender = BroadcastSender(authorization_token)
        self.location_sender = LocationSender(authorization_token)
        self.sticker_sender = StickerSender(authorization_token)

    def send_message(
        self, to=None, bot_id=None, message=None, custom_notification=None
    ):
        to = to or self.default_to
        bot_id = bot_id or self.default_bot_id
        return self.message_sender.send_message(
            to, bot_id, message, custom_notification
        )

    def broadcast_message(self, bot_id=None, to=None, message=None):
        bot_id = bot_id or self.default_bot_id
        to = to or self.default_to
        return self.broadcast_sender.broadcast_message(bot_id, to, message)

    def send_location(
        self,
        to=None,
        bot_id=None,
        latitude=None,
        longitude=None,
        address=None,
        custom_notification=None,
    ):
        to = to or self.default_to
        bot_id = bot_id or self.default_bot_id
        return self.location_sender.send_location(
            to, bot_id, latitude, longitude, address, custom_notification
        )

    def send_sticker(
        self, to=None, bot_id=None, sticker_id=None, custom_notification=None
    ):
        to = to or self.default_to
        bot_id = bot_id or self.default_bot_id
        return self.sticker_sender.send_sticker(
            to, bot_id, sticker_id, custom_notification
        )
