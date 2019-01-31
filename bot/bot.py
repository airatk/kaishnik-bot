import telebot
import secrets

telebot.apihelper.proxy = secrets.PROXY
bot = telebot.TeleBot(secrets.TOKEN)

def send_action(action_type):
    def function_wrapper(command):
        def argument_wrapper(message):
            bot.send_chat_action(message.chat.id, action_type)
            command(message)
        return argument_wrapper
    return function_wrapper

@bot.message_handler(commands=["start"])
@send_action(action_type="typing")
def start(message):
    bot.send_message(message.chat.id, "Йоу!")

@bot.message_handler(commands=["classes"])
@send_action(action_type="typing")
def classes(message):
    pass

@bot.message_handler(commands=["exams"])
@send_action(action_type="typing")
def exams(message):
    pass

@bot.message_handler(commands=["score"])
@send_action(action_type="typing")
def score(message):
    pass

@bot.message_handler(commands=["buildings"])
@send_action(action_type="find_location")
def buildings(message):
    pass

@bot.message_handler(commands=["settings"])
@send_action(action_type="typing")
def settings(message):
    pass

bot.polling()
