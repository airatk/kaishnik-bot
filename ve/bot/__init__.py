from sys import argv

from .sbot import Bot


def main():
    sbot = Bot()
    
    if len(argv) > 1 and argv[1] == "i":
        sbot.notification.start()
        sbot.start()
        sbot.notification.join()
    elif len(argv) > 1 and argv[1] == "c":
        print("without notification")
        sbot.start()
    else:
        sbot.test()
