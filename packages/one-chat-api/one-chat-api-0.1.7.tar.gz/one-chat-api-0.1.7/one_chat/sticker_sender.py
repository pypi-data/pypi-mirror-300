# one_chat/sticker_sender.py

import requests

class StickerSender:
    def __init__(self, bot_id, authorization_token):
        self.bot_id = bot_id
        self.authorization_token = authorization_token
        self.api_url = "https://chat-api.one.th/message/api/v1/push_message"

    def send_sticker(self, to, sticker_id, custom_notification=None):
        """Send a sticker to a specified user or group."""
        headers = {
            "Authorization": f"Bearer {self.authorization_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": to,
            "bot_id": self.bot_id,
            "type": "sticker",
            "sticker_id": sticker_id,
            "custom_notification": custom_notification
        }

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()  # Return the successful response
        else:
            # Handle errors accordingly
            return {
                "status": "fail",
                "message": response.json().get("message", "Error sending sticker.")
            }