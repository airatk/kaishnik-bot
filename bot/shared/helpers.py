from telebot import apihelper

from bot import bot
from bot import keys

from sys import argv


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler):
    def wrapper(callback):
        callback_handler(callback)
        
        apihelper.answer_callback_query(
            token=TOKEN,
            callback_query_id=callback.id,
            cache_time=0
        )
    
    return wrapper


# Launcher
def main():
    launch_modes = [ "testing", "eternal" ]
    
    if len(argv) != 3 or argv[2] not in launch_modes:
        print(
            "\n"
            "  Incorrect options!\n\n"
            "> python3 . -m {mode1} - to launch in {mode1} mode\n"
            "> python3 . -m {mode2} - to launch in {mode1} mode\n"
            .format(
                mode1=launch_modes[0],
                mode2=launch_modes[1]
            )
        )
        
        return
    
    print(f"Launched in {argv[2]} mode...")
    
    if argv[2] == launch_modes[0]:
        bot.polling()
    elif argv[2] == launch_modes[1]:
        bot.infinity_polling(True)
