from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='static')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

rooms = ['room1', 'room2', 'room3']


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


@app.route('/api/v1/rooms/', methods=['GET'])
def get_rooms():
    return jsonify(rooms)


@socketio.on('msg_server')
def msg(json):
    emit("msg_client", json, room=json['room'])


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
