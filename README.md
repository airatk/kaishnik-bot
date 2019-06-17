# kaishnik-bot
_Telegram bot for KAI students_

## What the ?
The bot might be considered as kai.ru & old.kai.ru wrapper. It's built using [pyTelegramBotAPI][1].

## Reason
Mobile-unfriendly ugly inconvenient website had to be replaced by something usable & not only usable. Here the [@kaishnik_bot][2] comes up.

## Setup

### Environment setup
Before the launch you've got to set 2 environmental variables:
* `KBOT_TOKEN` is a unique bot thing given by [@BotFather][3].
* `KBOT_CREATOR` is a chat ID (integer type, see [Telegram Bot API][4]) of ~~the creator~~ an admin. This person has access to the `/creator` command.

The time zone should be set to `Europe/Moscow` as well (since the university's located in Kazan in Moscow time zone).

### Data
There should be `data/` folder (with non-extension files which contain data written in binary form) in the root directory of the bot. It should contant:
* `users` file with dictionary which contains `chat_id: Student()` pairs.
* `is_week_reversed` file with a boolean value which is used to define the correct type of a week. 

### Launch setup
First of all, this is Python 3.

Secondly, the `requirements.txt` file is included to the repository. So, enter `pip3 install -r requirements.txt` to the console to have all the necessary stuff.

Finally, type `python3 startup.py` to launch.

## Other stuff
* `update-logs/` folder contains notes which were sent to users as update announcements.

## Design
All the stuff was drawn using Pixelmator Pro. 

_Undescribably useful, joyfully cute!_

![kaishnik_bot logo][5]
![kaishnik_bot poster][6]


[1]: https://github.com/eternnoir/pyTelegramBotAPI "Repository of pyTelegramBotAPI"
[2]: https://telegram.me/kaishnik_bot "Open the bot in Telegram"
[3]: https://telegram.me/BotFather "Open BotFather in Telegram"
[4]: https://core.telegram.org/bots/api "Telegram Bot API official reference"
[5]: https://github.com/AiratK/kaishnik-bot/blob/master/design/logo.png "kaishnik-bot logo"
[6]: https://github.com/AiratK/kaishnik-bot/blob/master/design/poster.png "kaishnik-bot poster"
