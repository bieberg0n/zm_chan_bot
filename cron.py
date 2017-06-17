from datetime import datetime, timedelta
import requests
import zm_chan_bot
import time


def cron():
    # get_second = lambda: int(time.time())
    now = datetime.now()
    next_time = now.replace(hour=9, minute=0) + timedelta(days=1)
    print(next_time)
    while True:
        now = datetime.now()
        if now >= next_time:
            yield 'BJ记得打卡！'
            next_time = next_time + timedelta(days=1)
        else:
            yield


def cron_reply(s, token, chat_room, cron_gen):
    while True:
        msg = next(cron_gen)
        if msg:
            print(msg)
            zm_chan_bot.send(s, token, chat_room, msg)
        else:
            pass
        time.sleep(1)


if __name__ == '__main__':
    s = requests.session()
    s.proxies = {'http': 'socks5://127.0.0.1:1080',
                 'https': 'socks5://127.0.0.1:1080'}
    cfg = zm_chan_bot.get_cfg()
    token = cfg.get('token')

    cron_gen = cron()
    cron_reply(s, token, 228267026, cron_gen)
