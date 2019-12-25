from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)
messages = [
    {'username': 'John', 'time': time.time(), 'text': 'Hello!'},
    {'username': 'Mary', 'time': time.time(), 'text': 'Hello, John!'}
]
password_storage = {

}

@app.route("/status")
def status_method():
    return {
        'status': True,
        'server_time': datetime.now().strftime('%H:%M:%S %d.%m.%Y'),
        'messages_count': len(messages),
        'users_count': len(password_storage)
    }

@app.route("/send", methods=['POST'])
def send_method():
    """
    JSON {"username":str, "text":str}
    username, text-непустые строки
    :return: {'ok':bool}
    """
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username not in password_storage:
        password_storage[username] = password

    if not isinstance(username, str) or len(username) == 0:
        return {'ok': False}
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}
    if password_storage[username] != password:
        return {'ok': False}
    # Save message
    messages.append({'username': username, 'time': time.time(), 'text': text})

    return {'ok': True}


@app.route("/messages")
def messages_method():
    """
    Param after
    :return: {'messages':[
        {'username':str, 'time':float, 'text':str},
        ...
    ]}
    """
    after = float(request.args['after'])
    filt_messages = [message for message in messages if message['time']>after]

    return {'messages': filt_messages}

app.run()