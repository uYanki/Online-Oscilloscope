from random import randint
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)

name_space = '/echo'

channels = ['ECG', 'EEG']


@app.route('/')
def index():
    return render_template('index.html', params={'channels': channels})


@app.route('/push')
def broadcast_msg():  # 广播数据
    event_name = 'append'
    broadcasted_data = {'data': [randint(-i*i, i*i) for i in range(200)]}
    socket.emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    return 'done!'


@socket.on('connect', namespace=name_space)
def client_connected():
    print('client connected.')
    socket.emit('echo', {'data': "hello!"}, broadcast=False, namespace=name_space)


@socket.on('disconnect', namespace=name_space)
def client_disconnect():
    print('client disconnected.')


if __name__ == "__main__":
    print('http://127.0.0.1:5000')
    socket.run(app, host='127.0.0.1', port=5000, debug=True)
