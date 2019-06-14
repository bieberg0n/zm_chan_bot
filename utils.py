import socket
import json
import pprint
import config


def info(*args):
    if len(args) == 1:
        pprint.pprint(args[0])
    else:
        print(*args)


def log(*args):
    if config.debug:
        info(*args)


def push_msg(room_id, msg):
    data = {
        'id': room_id,
        'message': msg,
    }
    s = socket.socket()
    s.connect(('d.bjong.me', 8800))
    s.sendall(json.dumps(data).encode())
    s.close()
