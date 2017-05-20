import requests
import json
import re


def translate(word):
    key = '716426270'
    keyFrom = 'wufeifei'
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=wufeifei&key=716426270&type=data&doctype=json&version=1.1&q=' + word
    r = requests.get(url)
    r_dict = json.loads(r.text)
    try:
        u = r_dict['basic']['us-phonetic'] # English
        e = r_dict['basic']['uk-phonetic']
    except KeyError:
        try:
            c = r_dict['basic']['phonetic'] # Chinese
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
        # print()
        pass

    if explains != 'None':
        for i in range(0, len(explains)):
            # print(explains[i])
            reply_text += (explains[i] + '\n')
    else:
        # print('Explains None')
        reply_text += 'Explains None'
    return reply_text


def reply(msg):
    print(msg)

    # if '米酱' in msg:
    #     reply_text = '米酱爱你哦！'
    # else:
    #     reply_text = '哼！'
    if '翻译' in msg:
        re_result = re.findall('[A-Za-z]+$', msg)
        print(re_result)
        word = re_result[0] if len(re_result) >= 1 else None
        if word:
            reply_text = translate(word)
            return reply_text
        else:
            return
    else:
        return

    # return reply_text
