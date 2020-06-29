from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='static')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

rooms = ['room1', 'room2', 'room3']

games = []

system_rooms = ['games']


@app.route('/api/v1/games/', methods=['POST'])
def post_game():
    data = request.json
    if data['name'] not in [item['name'] for item in games]:
        tmp = {'name': data['name'], 'users': [], 'state': {'turns': [], 'again': 0, 'users_number': 2}}
        games.append(tmp)
        socketio.emit("new_game", tmp, broadcard=True)
        return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/api/v1/games/', methods=['GET'])
def get_games():
    return jsonify({'success': True, 'games': games})


# section join
@socketio.on('delete_game')
def delete_game(data):
    return 0


@socketio.on('join_game')
def join_game(data):
    if data['game'] in [item['name'] for item in games]:
        join_room(data['game'])
        for game in games:
            if game['name'] == data['game']:
                game['users'].append(data['username'])
            if len(game['users']) == game['state']['users_number']:
                emit("start_game", room=data['game'])
        emit("join_user", {'user': data['username'], 'game': data['game']}, broadcast=True)
        return
    return


@socketio.on('leave_game')
def leave_game(data):
    if data['game'] in [item['name'] for item in games]:
        leave_room(data['game'])
        for game in games:
            if game['name'] == data['game']:
                game['users'].remove(data['username'])
            if len(game['users']) == 0:
                games.remove(game)
                emit("delete_game", game['name'], broadcast=True)
            elif len(game['users']) < game['state']['users_number']:
                emit("unstart_game", room=data['game'])
        emit("leave_user", {'user': data['username'], 'game': data['game']}, broadcast=True)
        return
    return


# /section join

# section game
@socketio.on('turn')
def turn(data):
    for game in games:
        if game['name'] == data['game']:
            game['state']['turns'].append({'user': data['username'], 'value': data['turn']})
            emit("add_turn", {'user': data['username'], 'value': data['turn']}, room=data['game'])
            length = len(game['state']['turns'])
            arr = game['state']['turns']
            if length % 2 == 0:
                first = arr[length - 2]
                second = arr[length - 1]
                winner = None
                if first['value'] == 'ножницы' and second['value'] == 'бумага':
                    winner = first['user']
                elif first['value'] == 'бумага' and second['value'] == 'камень':
                    winner = first['user']
                elif first['value'] == 'камень' and second['value'] == 'ножницы':
                    winner = first['user']
                elif first['value'] == second['value']:
                    winner = "Ничья"
                else:
                    winner = second['user']
                emit("end_turn", {'winner': winner, 'turns': [first, second]}, room=data['game'])
            return


@socketio.on('play_again')
def play_again(data):
    for game in games:
        if game['name'] == data['game']:
            game['state']['again'] += 1
            if game['state']['again'] == game['state']['users_number']:
                emit("add_play_again", room=data['game'])
                emit("start_game", room=data['game'])
                game['state']['again'] = 0
                return
            emit("add_play_again", room=data['game'])
            return


################################################

@app.route('/api/v1/rooms/', methods=['GET'])
def get_rooms():
    return jsonify(rooms)


@socketio.on('join_room')
def join(data):
    if data['room'] in rooms:
        join_room(data['room'])
        emit("system_event", "User {0} has joined the room".format(data['user']), room=data['room'])
        # emit('system_event', 'You are join to room ' + data['room'])
        return
    emit('system_event', 'Error with joining a room')


@socketio.on('leave_room')
def join(data):
    if data['room'] in rooms:
        leave_room(data['room'])
        emit("system_event", "User {0} has leave from the room".format(data['user']), room=data['room'])
        # emit('system_event', 'You are leave from a room ' + data['room'])
        return
    emit('system_event', 'Error with leaving from a room')


@socketio.on('msg_server')
def msg(json):
    emit("msg_client", json, room=json['room'])


@app.route('/')
def index():
    return render_template('index.html')


# give all to vue router
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
