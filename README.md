# Каист

[<img src="https://github.com/airatk/kaishnik-bot/blob/master/design/logo/logo.png" alt="kaishnik-bot logo" align="right" width="175" />][2]

_telegram bot for students of KNRTU-KAI to make their daily routine more pleasant_

### Stack
* Python
* [aiogram][1]

## Reason
The bot might be considered as `kai.ru` & `old.kai.ru` wrapper. Official mobile-unfriendly ugly inconvenient website had to be replaced by something usable. Here the [@kaishnik_bot][2] comes in.

## Setup

Since the university is located in Kazan which is the Moscow time zone, the time zone should be set to `Europe/Moscow`.

### Data
There should be `data/` folder in the root directory of the bot. It should contain the following non-extension files with data in binary form:
* `users` file with dictionary which contains `chat_id: Student` pairs.
* `dayoffs` file with list of `(int, int)` tuples to store dayoffs. 
* `keys` file is used to store tokens & keys accessed using `config` module.

### Launch setup
The `requirements.txt` file is included to the repository. So, use `pip3 install -r requirements.txt` to get all the necessities.
Use `python3 ./` to launch.

## Commands
* **classes** - занятия
* **score** - баллы
* **lecturers** - преподаватели
* **notes** - заметки
* **week** - чётность недели
* **exams** - экзамены
* **locations** - здания КАИ
* **brs** - что за БРС?
* **edit** - изменить расписание
* **settings** - настройки
* **help** - подсказки
* **donate** - сказать спасибо

Each command has its own directory:

    *command_name*/
    ├── __init__.py
    ├── *commands_file*.py
    ├── *commands_file*.py
    ├── guard.py
    └── utilities/
        ├── keyboards.py
        ├── helpers.py
        ├── constants.py
        └── types.py

The structure is essential meanwhile all the noted files are optional. One-file commands are exceptions, and are located at `bot/commands/others/` directory. `bot/commands/schedule/` directory is also an exception, and may be considered as a super-command which consists of 3 similar, but separate commands. 

## Other stuff
* `update-logs/` folder contains notes which were sent to users as update announcements.
* `cas-external-login/` folder contains some information about logging in CAS & simple login implementation.

## Design
All the stuff was drawn using [Pixelmator Pro][6]. 

[![kaishnik_bot poster][5]][2]


[1]: https://github.com/aiogram/aiogram "Repository of aiogram"
[2]: https://telegram.me/kaishnik_bot "Open the bot in Telegram"
[3]: https://telegram.me/BotFather "Open BotFather in Telegram"
[4]: https://core.telegram.org/bots/api "Telegram Bot API official reference"
[5]: https://github.com/airatk/kaishnik-bot/blob/master/design/poster/poster.png "kaishnik-bot poster"
[6]: https://www.pixelmator.com/pro "Pixelmator Pro"
