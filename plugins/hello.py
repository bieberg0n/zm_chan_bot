history = []

def is_hello(msg):
    names = ('米酱', '@zm_chan')
    if [True for name in names if name in msg]:
        return True
    else:
        return False


def allow_reply(result):
    return result['message']['from'].get('username') == 'bjong'


def reply(result):

    if not allow_reply(result):
        return

    else:
        msg = result['message'].get('text')
        history.append(msg)

        if len(history) >= 4 and is_hello(history[-4]) and\
           is_hello(history[-3]) and\
           is_hello(history[-2]) and is_hello(history[-1]):
            return
        else:
            pass

        if len(history) >= 3 and is_hello(history[-3]) and\
           is_hello(history[-2]) and is_hello(history[-1]):
            return '......'

        else:
            pass

        if is_hello(msg):
            return '嗯？'

        else:
            pass



# if __name__ in '__main__':
#     reply()
