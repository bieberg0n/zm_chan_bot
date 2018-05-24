import requests
import json
# import socket
import sys
import pprint
import time
import glob
import importlib
import threading
# from queue import Queue


def log(*args):
    if len(args) == 1:
        pprint.pprint(args[0])
    else:
        print(*args)


def import_plugins():
    plugin_str_list_ = [plugin.replace('/', '.') for plugin in glob.glob('plugins/*.py') if '/__' not in plugin]
    print(plugin_str_list_)
    plugin_str_list = [plugin.replace('.py', '') for plugin in plugin_str_list_]
    plugins = [importlib.import_module(plugin_str) for plugin_str in plugin_str_list]
    return plugins


def allow_reply(result):
    msg = result['message'].get('text')
    if msg:
        return (
                '@zm_chan_bot' in msg or '米酱' in msg and
                result['message']['chat']['type'] == 'supergroup'
        ) or\
        (
            result['message']['chat']['type'] == 'private'# and
            # result['message']['from'].get('username') == 'bjong'
        )
    # :
    #         return True
    #     else:
    #         return False

    else:
        return False


class Bot:
    def __init__(self, token):
        self.s = requests.session()
        self.s.proxies = {'http': 'socks5h://127.0.0.1:1080',
                          'https': 'socks5h://127.0.0.1:1080'}

        self.token = token
        self.plugins = import_plugins()
        self.offset = 0

    def send(self, chat_room, send_msg):
        url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
        r = self.s.get(url.format(self.token, chat_room, send_msg))
        return r.text

    def handle(self, result):
        # msg = result['message'].get('text')
        chat_room = result['message']['chat']['id']

        reply_text_list_ = [plugin.reply(result) for plugin in self.plugins]
        reply_text_list = [text for text in reply_text_list_ if text]
        if reply_text_list:
            reply_text = reply_text_list[0]
        else:
            reply_text = None
        if reply_text:
            print(reply_text)
            self.send(chat_room, reply_text)
        else:
            pass

    def get_updates(self):
        url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
        r = self.s.get(url.format(token, self.offset))
        json_ = r.content.decode()
        try:
            history = json.loads(json_)
        except ValueError:
            return self.get_updates(self.offset)
        else:
            return history

    def get_msg_handle(self):
        # offset = self.offset_
        history = self.get_updates()

        result_list = history['result']
        for result in result_list:
            if result['update_id'] > self.offset and result.get('message'):
                pprint.pprint(result)
                if allow_reply(result):
                    self.handle(result)

        self.offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
        # self.offset_queue.put(offset)

    def loop(self):
        # handle = get_handle_func(s, token)
        # offset_queue = Queue()
        # self.offset_queue.put(offset)
        while True:
            time.sleep(1.5)
            t = threading.Thread(target=self.get_msg_handle)
            t.start()
            t.join()

    def start(self):
        history = self.get_updates()
        log(history)
        offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
        log(offset)
        self.offset = offset
        self.loop()


# def get_cfg():
#     with open('update_id.json') as f:
#         cfg = json.loads(f.read())
#         return cfg


if __name__ == '__main__':
    token = sys.argv[1]
    # log(token)
    bot = Bot(token)
    bot.start()
