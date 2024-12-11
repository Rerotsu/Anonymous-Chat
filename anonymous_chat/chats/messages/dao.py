
from anonymous_chat.dao.base import base
from anonymous_chat.chats.messages.models import Messages


class MessagesDAO(base):
    model = Messages
