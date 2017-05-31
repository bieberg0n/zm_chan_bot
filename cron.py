from datetime import datetime, timedelta

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
