# kaishnik-bot
_Telegram bot for KAI students_

## What the ?
The bot might be considered as kai.ru & old.kai.ru wrapper. It's build using [pyTelegramBotAPI][1].

## Reason
Mobile-unfriendly ugly inconvenient website had to be replaced by something useable & not only useable. Here the  [@kaishnik_bot][2] comes up.

## Setup

### Environment setup
Before the launch you've got to set 2 environmental variables:
* `KBOT_TOKEN` is a unique bot thing given by [@BotFather][3].
* `KBOT_CREATOR` is a chat ID (integer type, see [Telegram Bot API][4]) of ~~the creator~~ an admin. This person has access to the /creator command.

The time zone should be set to Europe/Moscow as well (since the university's located in Kazan in Moscow time zone).

### Launch setup
First of all, this is Python 3.

The bot is written to be launched as a simple script, therefor you only need to type `python3 startup.py` into the console to launch it.

Also, the requirements.txt file is included to the repository. So, enter `pip3 install -r requirements.txt` to the console to have all necessary stuff.

### Data
There should be `data/` folder in the root directory of the bot. It should contant `users` file with dictionary, and `is_week_reversed` with boolean value.

The full process looks like this:

    git clone https://github.com/airatk/kaishnik-bot
    pip3 install -r requirements.txt
    python3 startup.py

## Other stuff
### Rubbish
`rubbish/` folder is for stuff which shouldn't be implemented because of oversized complexity & therefore wasn't, I just couldn't find effort to delete those :(

### Update logs
`update-logs/` folder is for notes which were sent to users as update announcements.

## Design
The logo was drawn using Pixelmator Pro. 

_Undescribably useful, joyfully cute!_

![logo][5]

[1]: https://github.com/eternnoir/pyTelegramBotAPI "Repository of pyTelegramBotAPI"
[2]: https://telegram.me/kaishnik_bot "Open the bot in Telegram"
[3]: https://telegram.me/BotFather "Open BotFather in Telegram"
[4]: https://core.telegram.org/bots/api "Telegram Bot API official reference"
[5]: https://github.com/AiratK/kaishnik-bot/blob/master/design/logo.png "kaishnik-bot logo"
