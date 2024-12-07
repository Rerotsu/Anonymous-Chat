from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
