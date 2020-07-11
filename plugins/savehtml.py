import requests
from zm_chan_bot import allow_reply, msg_from_result
from utils import log


def cond(msg):
    return msg.startswith('save') and len(msg) > 6


def save_html(url):
    r = requests.get('https://copy.dashao.me:2/copy_html?url=' + url)
    return r.status_code


def reply(result):
    if not allow_reply(result, cond):
        return

    msg = msg_from_result(result)
    key = 'save '
    url = msg[len(key):]
    log('url', url)
    code = save_html(url)
    return '{}{}'.format(key, code)


if __name__ == '__main__':
    url = 'https://www.hao123.com/'
    log(save_html(url))
