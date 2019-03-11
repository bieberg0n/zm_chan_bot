import requests
import json
import re
# import sys
from zm_chan_bot import allow_reply


def translate(word):
    key = '716426270'
    key_from = 'wufeifei'
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom={keyfrom}&key={key}&type=data&doctype=json&version=1.1&q={word}'
    url = url.format(keyfrom=key_from,
                     key=key,
                     word=word)
    r = requests.get(url)
    c = None
    try:
        r_dict = json.loads(r.text)
    except ValueError:
        print(r.text)
        return None
    try:
        u = r_dict['basic']['us-phonetic']  # English
        e = r_dict['basic']['uk-phonetic']
    except KeyError:
        try:
            c = r_dict['basic']['phonetic']  # Chinese
        except KeyError:
            c = 'None'
        u = 'None'
        e = 'None'

    try:
        explains = r_dict['basic']['explains']
    except KeyError:
        explains = 'None'

    reply_text = '{} {} '.format(r_dict['query'], r_dict['translation'][0])
    if u != 'None':
        reply_text += '(U: {} E: {} )\n'.format(u, e)
    elif c != 'None':
        '(Pinyin: {} )\n'.format(c)
    else:
        pass

    if explains != 'None':
        for i in range(0, len(explains)):
            # print(explains[i])
            reply_text += (explains[i] + '\n')
    else:
        # print('Explains None')
        reply_text += 'Explains None'
    return reply_text


def reply(result):
    if allow_reply(result):
        msg = result['message'].get('text')
        msg = msg.replace('@zm_chan_bot', '').replace(' ', '')

        if '翻译' in msg or re.findall('^\\.[A-Za-z]+$', msg):
            re_result = re.findall('[A-Za-z]+$', msg)
            word = re_result[0] if len(re_result) >= 1 else None
            if word:
                reply_text = translate(word)
                return reply_text


# if __name__ == '__main__':
#     msg = sys.argv[1]
#     print(reply(msg), end='')
