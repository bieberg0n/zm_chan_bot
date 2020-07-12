#!/usr/bin/env python3

import requests
import json
import time
import importlib
import threading
import config
from utils import info, log


def import_plugins(plugin_str_list):
    info(plugin_str_list)
    plugin_str_list = ['plugins.' + p for p in plugin_str_list]
    plugins = [importlib.import_module(plugin_str) for plugin_str in plugin_str_list]
    return plugins


def msg_from_result(result, clear=False):
    msg = result['message'].get('text')
    if clear:
        msg = msg.replace('@zm_chan_bot', '').strip(' ')
    return msg


def allow_reply(result, cond=None):
    msg = msg_from_result(result)
    if msg and ('@zm_chan_bot' in msg) or (result['message']['chat']['type'] == 'private'):
        msg = msg_from_result(result, clear=True)
        if cond:
            return cond(msg)
        else:
            return True

    else:
        return False


class Bot:
    def __init__(self, config):
        self.s = requests.session()
        self.s.proxies = {'http': 'socks5h://127.0.0.1:{}'.format(config.proxy_port),
                          'https': 'socks5h://127.0.0.1:{}'.format(config.proxy_port)}

        self.token = config.token
        self.plugins = import_plugins(config.plugins)
        self.offset = 0

    def send(self, chat_room, send_msg):
        p = {'chat_id': chat_room, 'text': send_msg}
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.token)
        r = self.s.get(url, params=p)
        return r.text

    def handle(self, result):
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
        history = json.loads(json_)
        return history

    def get_msg_handle(self):
        history = self.get_updates()

        result_list = history['result']
        for result in result_list:
            if result['update_id'] > self.offset and result.get('message'):
                info(result)
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
    bot = Bot(config)
    bot.start()
