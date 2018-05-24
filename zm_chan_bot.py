import requests
import json
# import socket
import sys
import pprint
import time
import glob
import importlib
import threading
from queue import Queue


def log(*args):
    print(*args)


def import_plugins():
    plugin_str_list_ = [plugin.replace('/', '.') for plugin in glob.glob('plugins/*.py') if '/__' not in plugin]
    print(plugin_str_list_)
    plugin_str_list = [plugin.replace('.py', '') for plugin in plugin_str_list_]
    plugins = [importlib.import_module(plugin_str) for plugin_str in plugin_str_list]
    return plugins


def send(s, token, chat_room, send_msg):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
    r = s.get(url.format(token, chat_room, send_msg))
    return r.text


def get_handle_func(s, token):
    plugins = import_plugins()

    def handle(result):
        # msg = result['message'].get('text')
        chat_room = result['message']['chat']['id']

        reply_text_list_ = [plugin.reply(result) for plugin in plugins]
        reply_text_list = [text for text in reply_text_list_ if text]
        if reply_text_list:
            reply_text = reply_text_list[0]
        else:
            reply_text = None
        if reply_text:
            print(reply_text)
            send(s, token, chat_room, reply_text)
        else:
            pass

    return handle


def get_updates(s, offset, token):
    url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
    r = s.get(url.format(token, offset))
    json_ = r.content.decode()
    try:
        history = json.loads(json_)
    except ValueError:
        return get_updates(s, offset, token)
    else:
        return history


def allow_reply(result):
    msg = result['message'].get('text')
    if msg:
        if (
                '@zm_chan_bot' in msg or '米酱' in msg and
                result['message']['chat']['type'] == 'supergroup'
        ) or\
        (
            result['message']['chat']['type'] == 'private'# and
            # result['message']['from'].get('username') == 'bjong'
        ):
            return True
        else:
            return False

    else:
        return False


def get_msg_handle(s, offset_queue, token, handle):
    offset = offset_queue.get()
    history = get_updates(s, offset, token)

    result_list = history['result']
    for result in result_list:
        if result['update_id'] > offset and result.get('message'):
            pprint.pprint(result)
            if allow_reply(result):
                handle(result)

    offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
    offset_queue.put(offset)


def loop(s, offset, token):
    handle = get_handle_func(s, token)
    offset_queue = Queue()
    offset_queue.put(offset)

    while True:
        time.sleep(1.5)
        t = threading.Thread(target=get_msg_handle, args=(s, offset_queue, token, handle,))
        t.start()
        t.join()


def zm_chan_bot_start(token):
    # token = cfg['token']
    s = requests.session()
    s.proxies = {'http': 'socks5://127.0.0.1:1080',
                 'https': 'socks5://127.0.0.1:1080'}

    history = get_updates(s, 0, token)
    pprint.pprint(history)
    offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
    print(offset)
    loop(s, offset, token)


# def get_cfg():
#     with open('update_id.json') as f:
#         cfg = json.loads(f.read())
#         return cfg


if __name__ == '__main__':
    token = sys.argv[1]
    # log(token)
    zm_chan_bot_start(token)
