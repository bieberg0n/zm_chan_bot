import requests
from threading import Timer
from zm_chan_bot import allow_reply
from utils import push_msg


def check(cmd):
    parts = cmd.split(' ', 1)
    if len(parts) != 2:
        return False

    cmd, msg = parts

    time_flags = ('s', 'm', 'h', 'd')

    if len(cmd) < 3:
        return False
    elif not cmd.startswith('+'):
        return False
    elif cmd[-1] not in time_flags:
        return False
    elif not cmd[1:-1].isdigit():
        return False

    else:
        return True


class Task:
    def __init__(self):
        self.seconds = 0
        self.msg = ''

    def parse(self, cmd):
        if not check(cmd):
            return False

        t, self.msg = cmd.split(' ', 1)
        m = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 3600 * 24,
        }
        self.seconds = int(t[1:-1]) * m[t[-1]]


def reply(result):
    if not allow_reply(result):
        return

    msg = result['message'].get('text').replace('@zm_chan_bot', '').strip(' ')
    if not msg.startswith('+'):
        return

    chat_id = result['message']['chat'].get('id')
    # data = {
    #     'id': chat_id,
    #     'cmd': msg,
    # }
    # requests.post('http://127.0.0.1:5000', json=data)
    task = Task()
    task.parse(msg)
    Timer(task.seconds, push_msg, (chat_id, task.msg,)).start()
