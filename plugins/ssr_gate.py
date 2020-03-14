import requests
from zm_chan_bot import allow_reply
import config


def reply(result):
    if not allow_reply(result):
        return

    msg = result['message'].get('text')
    msg = msg.replace('@zm_chan_bot', '').replace(' ', '')

    url = config.ssr_gate_url
    node = ''
    if msg == '当前节点':
        try:
            r = requests.get(url)
            node = r.text
        except:
            ...
        finally:
            return node

    elif msg == '下一个节点':
        try:
            requests.get(url + '/update')
        except:
            ...
