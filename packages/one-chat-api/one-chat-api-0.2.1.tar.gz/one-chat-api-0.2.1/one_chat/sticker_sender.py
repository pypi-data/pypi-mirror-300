# one_chat/sticker_sender.py

import requests

class StickerSender:
    def __init__(self, authorization_token):
        """Initialize StickerSender with the authorization token."""
        self.authorization_token = authorization_token
        self.api_url = "https://chat-api.one.th/message/api/v1/push_message"

    def send_sticker(self, to, bot_id, sticker_id, custom_notification=None):
        """Send a sticker to a specified user or group.

        Args:
            to (str): The user_id or group_id to send the sticker to.
            bot_id (str): The bot's unique ID.
            sticker_id (str): The ID of the sticker to send.
            custom_notification (str, optional): Custom notification message.

        Returns:
            dict: Response from the API call.
        """
        headers = {
            "Authorization": f"Bearer {self.authorization_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": to,
            "bot_id": bot_id,
            "type": "sticker",
            "sticker_id": sticker_id,
            "custom_notification": custom_notification
        }

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()  # Return the successful response
        else:
            # Return error response for handling
            return {
                "status": "fail",
                "message": response.json().get("message", "Error sending sticker.")
            }