from random import randint
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.jinja_options.update(
    # resolve the conflict between the template syntax of jinja2 and vuejs
    dict(
        variable_start_string='[[',
        variable_end_string=']]',
    )
)

socket = SocketIO(app)

name_space = '/echo'

channels = set(['ECG', 'EEG', 'unkonwn', 'adc0', 'adc1', 'adc2', 'stm632', 'es6p32',  'stm32', 'esp32', 'unko2nwn', 'adc02', 'adc21', 'adc22', 'stm322', 'esp232'])


@app.route('/')
@app.route('/oscilloscope')
def index():
    return render_template('index.html', params={'channels': channels})


@app.route('/oscilloscope/channels', methods=['get', 'post'])
def channel():
    return jsonify({'channels': list(channels)})


@app.route('/push')
def broadcast_msg():  # 广播数据
    event_name = 'append'
    broadcasted_data = {'data': {
        'ECG': [randint(-i*i, i*i) for i in range(100)],
        'EEG': [randint(i*2, i*3) for i in range(50)]
    }}
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
