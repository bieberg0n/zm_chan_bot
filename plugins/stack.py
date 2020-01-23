from decimal import Decimal
import easyquotation
from zm_chan_bot import allow_reply


def log(*args):
    print(*args)


def pull():
    q = easyquotation.use('sina')
    r = q.stocks(['000333', '002422'])
    total = Decimal(16000 + 2647)  # 加注
    d200 = Decimal(200)
    d300 = Decimal(300)
    s1_cost = d200 * Decimal(str(55.535))
    s2_cost = d300 * Decimal(str(26.157))
    now = [r['000333']['now'], r['002422']['now']]
    s1_now = d200 * Decimal(str(now[0]))
    s2_now = d300 * Decimal(str(now[1]))
    s1_r = s1_now - s1_cost
    s1_rb = (s1_r / s1_cost * 100).quantize(Decimal("0.0000"))
    s2_r = s2_now - s2_cost
    s2_rb = (s2_r / s2_cost * 100).quantize(Decimal("0.0000"))

    now_all = s1_now + s2_now

    # got = total
    # got_b = got / total * 100
    all_b = ((now_all - total) / total * 100).quantize(Decimal("0.0000"))
    return '''美的集团：{} 盈亏情况：{} 收益率：{} %
科伦药业：{} 盈亏情况：{} 收益率：{} %
历史总收益率：{} %
'''.format(now[0], s1_r, s1_rb,
           now[1], s2_r, s2_rb,
           all_b)


def reply(result):
    if not allow_reply(result):
        return

    msg = result['message'].get('text')
    msg = msg.replace('@zm_chan_bot', '').replace(' ', '')
    if msg == '破产清算':
        return pull()


if __name__ == '__main__':
    log(pull())
