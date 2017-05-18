def reply(msg):
    print(msg)

    if '米酱' in msg:
        reply_text = '米酱爱你哦！'
    else:
        reply_text = '哼！'

    return reply_text
