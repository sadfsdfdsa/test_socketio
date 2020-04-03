from utils.helper import create_token


class User:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

        # todo delete
        self.users = {
            'login123': {
                'login': 'login123',
                'password': '123',
                'name': 'artem',
                'token': None
            }
        }

    # return token or False by login and password
    def login(self, login, password):
        if self.users[login]:
            if self.users[login]['password'] == password:
                return create_token(self.users[login])
        return False

    @staticmethod
    def serialize(one=None, many=None):
        if one is not None:
            return one  # todo
        elif many is not None:
            result = []
            for user in many:
                result.append(User.serialize(one=user))
        return None
