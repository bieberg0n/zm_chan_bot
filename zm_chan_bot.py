#!/usr/bin/env python3

import requests
import json
# import sys
# import pprint
import time
import glob
import importlib
import threading
import config
from utils import info, log


def import_plugins(plugin_str_list):
    # plugin_str_list_ = [plugin.replace('/', '.') for plugin in glob.glob('plugins/*.py') if '/__' not in plugin]
    info(plugin_str_list)
    plugin_str_list = ['plugins.' + p for p in plugin_str_list]
    plugins = [importlib.import_module(plugin_str) for plugin_str in plugin_str_list]
    return plugins


def allow_reply(result):
    msg = result['message'].get('text')
    if msg:
        return (
                '@zm_chan_bot' in msg
                # and
                # result['message']['chat']['type'] == 'supergroup'
        ) or (
            result['message']['chat']['type'] == 'private'
        )

    else:
        return False


class Bot:
    def __init__(self, config):
        self.s = requests.session()
        self.s.proxies = {'http': 'socks5h://127.0.0.1:1080',
                          'https': 'socks5h://127.0.0.1:1080'}

        self.token = config.token
        self.plugins = import_plugins(config.plugins)
        self.offset = 0

    def send(self, chat_room, send_msg):
        url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
        r = self.s.get(url.format(self.token, chat_room, send_msg))
        return r.text

    def handle(self, result):
        # info(result)
        chat_room = result['message']['chat']['id']

        reply_text_list = [plugin.reply(result) for plugin in self.plugins]
        log('reply text list:', reply_text_list)
        reply_text_list = [text for text in reply_text_list if text]
        if reply_text_list:
            reply_text, *_ = reply_text_list
            info(reply_text)
            self.send(chat_room, reply_text)

    def get_updates(self):
        url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
        r = self.s.get(url.format(self.token, self.offset))
        json_ = r.content.decode()
        # try:
        history = json.loads(json_)
        # except ValueError:
        #     return self.get_updates()
        # else:
        return history

    def get_msg_handle(self):
        history = self.get_updates()

        result_list = history['result']
        for result in result_list:
            if result['update_id'] > self.offset and result.get('message'):
                info(result)
                # and allow_reply(result):
                self.handle(result)

        self.offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0

    def loop(self):
        while True:
            time.sleep(1.5)
            t = threading.Thread(target=self.get_msg_handle)
            t.start()
            t.join()

    def start(self):
        history = self.get_updates()
        self.offset = history['result'][-1]['update_id'] if len(history['result']) >= 1 else 0
        info(history)
        info(self.offset)
        self.loop()


if __name__ == '__main__':
    # token = sys.argv[1]
    # cfg = config.token
    bot = Bot(config)
    bot.start()
