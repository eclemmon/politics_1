import socketio


client = socketio.Client()


@client.on('client_connected')
def on_connect(message):
    print(message)


@client.on('handle_message')
def message(data):
    print("got data")
    print(data)


client.connect('http://127.0.0.1:5000/')
client.wait()
