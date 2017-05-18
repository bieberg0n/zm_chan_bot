import requests
import json
import socket
import pprint
import time
from reply import reply
# import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket


def handle(msg, chat_room, s, token):
    reply_text = reply(msg)
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
    s.get(url.format(token, chat_room, reply))


def get_updates(s, offset, token):
    url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
    r = s.get(url.format(token, offset))
    json_ = r.content.decode()
    history = json.loads(json_)
    return history


def loop(s, offset, token):
    while True:
        try:
            history = get_updates(s, offset, token)
        except requests.exceptions.ConnectionError:
            continue

        result = history['result']
        for i in result:
            if i['update_id'] > offset:
                print(i)
                msg = i['message'].get('text')
                if not msg:
                    continue
                chat_room = i['message']['chat']['id']
                handle(msg, chat_room, s, token)
            else:
                pass
        offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
        time.sleep(1)


def zm_chan_bot_start(cfg):
    offset, token = cfg['offset'], cfg['token']
    s = requests.session()
    s.proxies = {'http': 'socks5://127.0.0.1:1080',
                 'https': 'socks5://127.0.0.1:1080'}

    # r = s.get(url.format(token, offset))
    # json_ = r.content.decode()
    # history = json.loads(json_)
    history = get_updates(s, offset, token)
    print(history)
    offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
    # if len(history['result']) >= 1:
    #     offset = history['result'][-1]['update_id']
    # else:
    #     offset = 0
    print(offset)
    loop(s, offset, token)


def get_cfg():
    with open('update_id.json') as f:
        cfg = json.loads(f.read())
        return cfg


if __name__ == '__main__':
    zm_chan_bot_start(get_cfg())
