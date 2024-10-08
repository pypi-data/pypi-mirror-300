# one_chat/message_sender.py

import requests
import json

class MessageSender:
    def __init__(self, authorization_token):
        """
        Initialize the MessageSender with the authorization token.

        Args:
            authorization_token (str): The Bearer token for authorization.
        """
        self.base_url = "https://chat-api.one.th/message/api/v1/push_message"
        self.headers = {
            "Authorization": f"Bearer {authorization_token}",
            "Content-Type": "application/json"
        }

    def send_message(self, to, bot_id, message, custom_notification=None):
        """
        Send a message to a specified user or group.

        Args:
            to (str): User ID or Group ID to send the message to.
            bot_id (str): Unique identifier for the bot sending the message.
            message (str): The message content to send.
            custom_notification (str, optional): Custom notification text.

        Returns:
            dict: The response from the API or error information.
        """
        payload = {
            "to": to,
            "bot_id": bot_id,
            "type": "text",
            "message": message
        }
        if custom_notification:
            payload["custom_notification"] = custom_notification

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                return response.json()  # Successful response
            else:
                return self._handle_error(response)
        except requests.exceptions.RequestException as e:
            return {
                "status": "fail",
                "message": f"Request failed: {str(e)}"
            }

    def _handle_error(self, response):
        """
        Handle errors returned by the API.

        Args:
            response (requests.Response): The response object from the failed request.

        Returns:
            dict: A dictionary with error information.
        """
        try:
            error_response = response.json()
            return {
                "status": error_response.get("status", "fail"),
                "message": error_response.get("message", "Unknown error occurred.")
            }
        except json.JSONDecodeError:
            return {
                "status": "fail",
                "message": "Invalid response from the server."
            }