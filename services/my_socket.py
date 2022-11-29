from flask_socketio import send, emit


def socket(socketio):
    @socketio.on('my event')
    def handle_message(data):
        print('Client: ' + str(data))
        emit('server_send', "Server send message ne !!", broadcast=True)

    @socketio.on('disconnect')
    def test_disconnect(data):
        print("Client disconnected !!")
    