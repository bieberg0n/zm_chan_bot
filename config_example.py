proxy = '127.0.0.1:1080'

token = ''
debug = False

plugins = [
    'id',
    'ip',
    'translate',
]

# save
need_save_chat_ids = []
influxdb = {
    'host': '',
    'port': 0,
    'username': '',
    'password': '',
    'database': '',
}

# ssr_gate
ssr_gate_url = ''