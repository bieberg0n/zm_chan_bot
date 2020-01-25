import influxdb
from utils import log
from zm_chan_bot import allow_reply
import config

dbcfg = config.influxdb
client = influxdb.InfluxDBClient(dbcfg['host'], dbcfg['port'], dbcfg['username'],
                                 dbcfg['password'], dbcfg['database'])


def reply(result):
    m = result['message']
    chat_id = m['chat']['id']

    msg = result['message'].get('text')
    msg = msg.replace('@zm_chan_bot', '').replace(' ', '')
    if allow_reply(result) and msg.startswith('~/') and msg.endswith('/'):
        result = client.query('select * from \"{}\" where msg={}'.format(chat_id, msg))
        his_msgs = list(result.get_points())
        his_msg_list = ['{} {}: {}'.format(i['time'], i['from'], i['msg']) for i in his_msgs]
        return '\n'.join(his_msg_list)

    msg = m.get('text', m.get('caption'))
    if chat_id in config.need_save_chat_ids and msg:
        log('need save:', chat_id)
        time = m['date']
        msg_from = m['from']['first_name']
        point = {
            'measurement': chat_id,
            'tags': {
                'from': msg_from,
            },
            'fields': {
                'time': time,
                'msg': msg,
            }
        }
        client.write_points([point])




