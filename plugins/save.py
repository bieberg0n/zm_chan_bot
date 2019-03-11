import influxdb
from utils import log
import config

dbcfg = config.influxdb
client = influxdb.InfluxDBClient(dbcfg['host'], dbcfg['port'], dbcfg['username'],
                                 dbcfg['password'], dbcfg['database'])


def reply(result):
    m = result['message']
    chat_id = m['chat']['id']
    time = m['date']
    msg = m.get('text')
    msg_from = m['from']['first_name']
    if chat_id in config.need_save_chat_ids and msg:
        log('need save:', chat_id)
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
