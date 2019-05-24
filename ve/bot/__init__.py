from .sbot import Bot


def main():
    sbot = Bot()
    
    sbot.notification.start()
    
    sbot.start()
    
    sbot.notification.join()
