import zm_chan_bot
import asyncio
import requests
import json

_cfg = zm_chan_bot.get_cfg()
TOKEN = _cfg.get('token')
S = requests.session()
S.proxies = {'http': 'socks5://127.0.0.1:1080',
             'https': 'socks5://127.0.0.1:1080'}


# def push(s, token, id, msg):
#     zm_chan_bot.send(S, )


def str_to_dict(string):
    # try:
    dict_ = json.loads(string)
    return dict_


async def handle(reader_c, writer_c):
    try:
        req_bytes = b''
        while True:
            buf = await reader_c.read(1024*16)
            if not buf:
                break
            else:
                req_bytes += buf
    except ConnectionResetError as e:
        print(e)

    req_json = req_bytes.decode()
    req = str_to_dict(req_json)

    if req:
        id, msg = req['id'], req['message']
        print(msg)
        print(zm_chan_bot.send(S, TOKEN, id, msg))
    else:
        return


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    core = asyncio.start_server(handle, '0.0.0.0', 8800, loop=loop)
    server = loop.run_until_complete(core)
    loop.run_forever()