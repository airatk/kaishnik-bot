from .sbot import Bot

from multiprocessing import Process


def main():
    sbot = Bot()
    
    process = Process(target=sbot.notification)
    process.start()
    
    sbot.start()
    
    process.join()
