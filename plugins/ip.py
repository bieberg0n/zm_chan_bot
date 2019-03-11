import requests
import socket
import subprocess
from zm_chan_bot import allow_reply


def valid_ip(address):
    try:
        ip_bytes = socket.inet_aton(address)
        return ip_bytes
    except:
        return False


def reply(result):
    if allow_reply(result):
        msg = result['message'].get('text')
        msg = msg.replace('@zm_chan_bot', '').replace(' ', '')
        if valid_ip(msg):
            address_raw = subprocess.getoutput('~/src/sh/qqwry {}'.format(msg))
            address = address_raw.split('\n')[-1]
            return address
