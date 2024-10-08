# one_chat/get_friends_and_groups.py

import requests
import json


class GetFriendsAndGroups:
    def __init__(self, authorization_token):
        self.base_url = "https://chat-api.one.th/manage/api/v1/getlistroom"
        self.headers = {
            "Authorization": f"Bearer {authorization_token}",
            "Content-Type": "application/json",
        }

    def get_friends_and_group(self, bot_id):
        payload = {"bot_id": bot_id}
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                return response.json()
            else:
                return self._handle_error(response)
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def get_all_friends(self, bot_id):
        try:
            response = self.get_friends_and_group(bot_id)
            if response.get("status") == "success":
                return response.get("list_friend", [])
            return []
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def get_one_id_of_friend(self, bot_id):
        try:
            response = self.get_friends_and_group(bot_id)
            if response.get("status") == "success":
                return [friend["one_id"] for friend in response.get("list_friend", [])]
            return []
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def get_all_groups(self, bot_id):
        try:
            response = self.get_friends_and_group(bot_id)
            if response.get("status") == "success":
                return response.get("list_group", [])
            return []
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def get_group_id_of_group(self, bot_id):
        try:
            response = self.get_friends_and_group(bot_id)
            if response.get("status") == "success":
                return [group["group_id"] for group in response.get("list_group", [])]
            return []
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def _handle_error(self, response):
        try:
            error_response = response.json()
            return {
                "status": error_response.get("status", "fail"),
                "message": error_response.get("message", "Unknown error occurred."),
            }
        except json.JSONDecodeError:
            return {"status": "fail", "message": "Invalid response from the server."}
