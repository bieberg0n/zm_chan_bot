from decimal import Decimal
import easyquotation
from zm_chan_bot import allow_reply


def pull():
    q = easyquotation.use('sina')
    r = q.stocks(['002007', '002422'])
    total = 16000
    d200 = Decimal(200)
    d300 = Decimal(300)
    cost = d200 * Decimal(str(35.485)) + d300 * Decimal(str(26.157))
    now = [r['002007']['now'], r['002422']['now']]
    # print(d200 * Decimal(now[0]), d300 * Decimal(now[1]))
    # exit()
    got = d200 * Decimal(str(now[0])) + d300 * Decimal(str(now[1])) - cost
    got_b = got / 16000 * 100
    # print(now, got, got_b)
    return '''华兰生物：{} 科伦药业：{}
盈亏情况：{} 收益率：{} %
    '''.format(now[0], now[1], got, got_b)


def reply(result):
    if not allow_reply(result):
        return

    msg = result['message'].get('text')
    msg = msg.replace('@zm_chan_bot', '').replace(' ', '')
    if msg == '破产清算':
        return pull()


if __name__ == '__main__':
    pull()
