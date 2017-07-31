import requests
import json
import socket


def push_msg(msg):
    s = socket.socket()
    s.connect(('a.bjong.me', 8800))
    s.sendall(msg)
    s.close()


def get_weather(city_name):
    r = requests.get('https://jirenguapi.applinzi.com/weather.php?city={}'.format(city_name))
    r.encoding = 'utf-8'
    resp = json.loads(r.text)
    print(resp)
    today = resp.get('results')[0].get('weather_data')[0]
    msg = '{city} {date} {weather} 今日温度{temperature}'.format(city=city_name, date=today['date'], weather=today['weather'], temperature=today['temperature'])
    return msg


def push_weather(city_name):
    data = {
        'id': 228267026,
        'message': get_weather(city_name)
    }
    push_msg(json.dumps(data).encode())


push_weather('绍兴')
