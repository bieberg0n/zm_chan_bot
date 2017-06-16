def reply(result):
    msg = result['message'].get('text')

    if msg == 'id':
        return result['message']['chat'].get('id')
    else:
        return
