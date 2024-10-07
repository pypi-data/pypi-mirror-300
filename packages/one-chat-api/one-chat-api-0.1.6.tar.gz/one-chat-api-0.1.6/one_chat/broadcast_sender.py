# one_chat/broadcast_sender.py

import requests
import json

class BroadcastSender:
    def __init__(self, authorization_token):
        """
        Initialize the BroadcastSender with the authorization token.

        Args:
            authorization_token (str): The Bearer token for authorization.
        """
        self.base_url = "https://chat-api.one.th/bc_msg/api/v1/broadcast_group"
        self.headers = {
            "Authorization": f"Bearer {authorization_token}",
            "Content-Type": "application/json"
        }

    def broadcast_message(self, bot_id, to, message):
        """
        Send a broadcast message to multiple users.

        Args:
            bot_id (str): Unique identifier for the bot sending the message.
            to (list): List of user IDs to send the message to.
            message (str): The message content to send.

        Returns:
            dict: The response from the API or error information.
        """
        if len(to) > 100:
            return {
                "status": "fail",
                "message": "parameter to out of range."
            }

        payload = {
            "bot_id": bot_id,
            "to": to,
            "message": message
        }

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