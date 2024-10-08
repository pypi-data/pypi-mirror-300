# one_chat/__init__.py

from .one_chat import OneChat

one_chat_instance = None
default_to = None
default_bot_id = None


def init(authorization_token, to=None, bot_id=None):
    global one_chat_instance, default_to, default_bot_id
    one_chat_instance = OneChat(authorization_token)
    default_to = to
    default_bot_id = bot_id


def send_message(to=None, bot_id=None, message=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_message(to, bot_id, message, custom_notification)


def broadcast_message(bot_id=None, to=None, message=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.broadcast_message(bot_id, [to], message)


def send_location(to=None, bot_id=None, latitude=None, longitude=None, address=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_location(to, bot_id, latitude, longitude, address, custom_notification)


def send_sticker(to=None, bot_id=None, sticker_id=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_sticker(to, bot_id, sticker_id, custom_notification)

def get_friends_and_group(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.get_friends_and_group(bot_id)

def get_all_friends(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.get_all_friends(bot_id)

def get_one_id_of_friend(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.get_one_id_of_friend(bot_id)

def get_all_groups(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.get_all_groups(bot_id)

def get_group_id_of_group(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.get_group_id_of_group(bot_id)