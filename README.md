# kaishnik-bot
_Telegram bot for KAI students_

## What the ?
The bot might be considered as kai.ru & old.kai.ru wrapper. It's build using [pyTelegramBotAPI][1].

## Reason
Mobile-unfriendly ugly inconvenient website had to be replaced by something useable & not only useable. Here the  [@kaishnik_bot][2] comes up.

## Setup
First of all, this is Python 3.

The bot is written to be launched as a simple script, therefor you only need to type `python3 bot.py` into the console to launch it. 

Before the launch you've got to set 2 environmental variables:
* **TOKEN** is a unique bot thing given by [@BotFather][3].
* **CREATOR** is a chat ID (integer type, see [Telegram Bot API][4]) of ~~a creator~~ an admin. This person has access to the /creator command. 

Also, the requirements.txt file is included to the repository. So, enter `pip3 install -r requirements.txt` to the console to have all necessary stuff.

The full process looks like this:

    git clone https://github.com/airatk/kaishnik_bot
    pip3 install -r requirements.txt
    cd bot/
    python3 bot.py

## Design
The logo was drawn using Pixelmator Pro. 

_Undescribably useful, joyfully cute!_ ![logo][4]

[1]: https://github.com/eternnoir/pyTelegramBotAPI                       "Repository of pyTelegramBotAPI"
[2]: https://telegram.me/kaishnik_bot                                    "Open bot in Telegram"
[3]: https://telegram.me/BotFather                                       "Open BotFather in Telegram"
[4]: https://core.telegram.org/bots/api                                  "Telegram Bot API"
[5]: https://github.com/AiratK/kaishnik-bot/blob/master/design/logo.png  "kaishnik_bot logo"
