import requests
import json
import socket
import pprint
import time
import glob
# from reply import reply
import importlib


def import_plugins():
    plugin_str_list_ = [plugin.replace('/', '.') for plugin in glob.glob('plugins/*.py') if '/__' not in plugin]
    print(plugin_str_list_)
    plugin_str_list = [plugin.replace('.py', '') for plugin in plugin_str_list_]
    plugins = [importlib.import_module(plugin_str) for plugin_str in plugin_str_list]
    # print([plugin.reply('翻译two') for plugin in plugins])
    return plugins


def get_handle_func():
    plugins = import_plugins()

    def handle_(msg, chat_room, s, token):
        reply_text_list_ = [plugin.reply(msg) for plugin in plugins]
        reply_text_list = [text for text in reply_text_list_ if text]
        if reply_text_list:
            reply_text = reply_text_list[0]
        else:
            reply_text = None
            # reply_text = reply_text_ if reply_text_ else None
        if reply_text:
            print(reply_text)
            url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
            s.get(url.format(token, chat_room, reply_text))
        else:
            pass

    return handle_


def get_updates(s, offset, token):
    url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'
    r = s.get(url.format(token, offset))
    json_ = r.content.decode()
    history = json.loads(json_)
    return history


def allow_reply(result):
    msg = result['message'].get('text')
    if msg:
        if (
                '@zm_chan_bot' in msg or '米酱' in msg and
                result['message']['chat']['type'] == 'supergroup'
        ) or\
        (
            result['message']['chat']['type'] == 'private' and
            result['message']['from'].get('username') == 'bjong'
        ):
            return True
        else:
            return False

    else:
        return False


def loop(s, offset, token, handle):
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
    handle = get_handle_func()
    loop(s, offset, token, handle)


def get_cfg():
    with open('update_id.json') as f:
        cfg = json.loads(f.read())
        return cfg


if __name__ == '__main__':
    zm_chan_bot_start(get_cfg())
