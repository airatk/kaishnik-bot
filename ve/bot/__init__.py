from sys import argv

from .sbot import Bot


def main():
    sbot = Bot()
    
    sbot.notification.start()
    
    if len(argv) > 1:
        sbot.start()
    else:
        sbot.test()
    
    sbot.notification.join()
