from zm_chan_bot import allow_reply


def reply(result):
    if allow_reply(result):
        msg = result['message'].get('text')

        msg = msg.replace('@zm_chan_bot', '').replace(' ', '')
        if msg == 'id':
            return result['message']['chat'].get('id')
