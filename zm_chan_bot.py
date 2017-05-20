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
    if reply_text:
        url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
        s.get(url.format(token, chat_room, reply_text))
    else:
        pass


def get_updates(s, offset, token):
    url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
    r = s.get(url.format(token, offset))
    json_ = r.content.decode()
    history = json.loads(json_)
    return history


def allow_reply(result):
    msg = result['message'].get('text')
    # i['message']['from'].get('username') == 'bjong' and\
    if msg:
        if ('@zm_chan_bot' in msg or msg.startswith('米酱')) or\
           (
               result['message']['chat']['type'] == 'private' and
               result['message']['from'].get('username') == 'bjong'
           ):
            return True
        else:
            return False

    else:
        return False


def loop(s, offset, token):
    while True:
        try:
            history = get_updates(s, offset, token)
        except requests.exceptions.ConnectionError:
            continue

        result = history['result']
        for i in result:
            if i['update_id'] > offset and i.get('message'):
                pprint.pprint(i)
                msg = i['message'].get('text')
                if allow_reply(i):
                    chat_room = i['message']['chat']['id']
                    handle(msg, chat_room, s, token)
                else:
                    pass
            else:
                pass

        offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
        time.sleep(1)


def zm_chan_bot_start(cfg):
    token = cfg['token']
    s = requests.session()
    s.proxies = {'http': 'socks5://127.0.0.1:1080',
                 'https': 'socks5://127.0.0.1:1080'}

    # r = s.get(url.format(token, offset))
    # json_ = r.content.decode()
    # history = json.loads(json_)
    history = get_updates(s, 0, token)
    pprint.pprint(history)
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
