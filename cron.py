import time

def cron():
    get_second = lambda: int(time.time())
    next_time = get_second() + 180
    while True:
        now = get_second()
        if now >= next_time:
            yield '骚扰一下' + ' ' + time.ctime()
            next_time = now + 180
        else:
            yield
