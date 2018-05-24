# coding=utf-8

import zm_chan_bot
import asyncio
# import requests
import sys
import json

# _cfg = zm_chan_bot.get_cfg()
# TOKEN = _cfg.get('token')
# S = requests.session()
# S.proxies = {'http': 'socks5://127.0.0.1:1080',
#              'https': 'socks5://127.0.0.1:1080'}


# def push(s, token, id, msg):
#     zm_chan_bot.send(S, )


def str_to_dict(string):
    try:
        dict_ = json.loads(string)
    except json.decoder.JSONDecodeError as e:
        print(e)
        return
    else:
        return dict_


class Handler:
    def __init__(self, token):
        self.bot = zm_chan_bot.Bot(token)

    async def handle(self, reader_c, writer_c):
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
            print(self.bot.send(id, msg))
        else:
            return


if __name__ == '__main__':
    token = sys.argv[1]
    # bot = zm_chan_bot.Bot(token)
    handler = Handler(token)

    loop = asyncio.get_event_loop()
    core = asyncio.start_server(handler.handle, '0.0.0.0', 8800, loop=loop)
    server = loop.run_until_complete(core)
    loop.run_forever()
