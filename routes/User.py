from app import app, db
from flask import request

from utils.http_errors import Errors
from utils.helper import validate_params, rest


# login by LOGIN and PASSWORD
# return token or error
# validation: login, password
@app.route('/api/v1/login/', methods=["POST"])
def login():
    data = request.json

    if not validate_params(data, 'login', 'password'):
        return rest('error', Errors.request_params_error)

    token = db.User.login(data['login'], data['password'])

    if not token:
        return rest('error', Errors.auth_error)

    # set token to user
    db.User.users[data['login']]['token'] = token

    return rest('success', {'token': token})


# return user data's by token
# validation: token
@app.route('/api/v1/user/', methods=["POST"])
def get_user():
    data = request.json

    if not validate_params(data, 'token'):
        return rest('error', Errors.request_params_error)

    for user in db.User.users.values():
        if user['token'] == data['token']:
            return rest('success', user)

    return rest('error', Errors.auth_error)
