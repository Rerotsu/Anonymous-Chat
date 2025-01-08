
from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.users.models import User


class UserDAO(BaseDAO):
    model = User
