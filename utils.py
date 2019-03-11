import pprint
import config


def info(*args):
    if len(args) == 1:
        pprint.pprint(args[0])
    else:
        print(*args)


def log(*args):
    if config.debug:
        info(*args)
