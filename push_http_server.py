from flask import (
Flask,
request,
)
from flask_cors import CORS
import zm_chan_bot
import config


app = Flask(__name__)
CORS(app, supports_credentials=True)
bot = zm_chan_bot.Bot(config)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print('data:', data)
    bot.send(data)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
