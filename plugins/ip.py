import requests
import socket


def valid_ip(address):
    try:
        ip_bytes = socket.inet_aton(address)
        return ip_bytes
    except:
        return False


def reply(result):
    msg = result['message'].get('text')
    msg = msg.replace('@zm_chan_bot', '').replace('米酱', '').replace('紫米酱', '').replace(' ', '')
    if valid_ip(msg):
        headers = {'User-Agent': 'curl/7.35.0'}
        r = requests.get('http://ip.cn/?ip={}'.format(msg), headers=headers)
        return r.text
    else:
        return
