from telebot import apihelper

from bot import bot
from bot import keys

from sys import argv


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler):
    def wrapper(callback):
        callback_handler(callback)
        
        apihelper.answer_callback_query(
            token=keys.TOKEN,
            callback_query_id=callback.id,
            cache_time=0
        )
    
    return wrapper


# Launcher
def main():
    launch_modes = [ "testing", "eternal" ]
    
    if len(argv) != 2 or argv[1] not in launch_modes:
        print(
            "\n"
            "  Incorrect options!\n\n"
            "> python3 . {mode1} - to launch in {mode1} mode\n"
            "> python3 . {mode2} - to launch in {mode1} mode\n"
            .format(
                mode1=launch_modes[0],
                mode2=launch_modes[1]
            )
        )
        
        return
    
    print(f"Launched in {argv[1]} mode...")
    
    if argv[1] == launch_modes[0]: bot.polling()
    elif argv[1] == launch_modes[1]: bot.infinity_polling(True)
