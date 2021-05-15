# Каист

[<img src="https://github.com/airatk/kaishnik-bot/blob/main/design/logo/logo.png" alt="kaishnik-bot logo" align="right" width="175" />][3]

_telegram bot for students of KNRTU-KAI to make their daily routine more pleasant_

### Stack
* Python
* [aiogram][1]
* PostgreSQL, [peewee][2]

## Reason
The bot might be considered as `kai.ru` & `old.kai.ru` wrapper. Official mobile-unfriendly ugly inconvenient website had to be replaced by something usable. Here the [@kaishnik_bot][3] comes in.

## Setup
Since the university is located in Kazan which is the Moscow time zone, the time zone should be set to `Europe/Moscow`.

### Data
There should be `data/` folder in the root directory of the bot. It should contain the following non-extension files with needed data:
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
* **dice** - бросок на удачу
* **locations** - здания КАИ
* **brs** - что за БРС?
* **edit** - изменить расписание
* **settings** - настройки
* **help** - подсказки
* **donate** - сказать спасибо

## Architecture
The bot is stored in project root directory folder called `bot/`. The `bot/` contains 3 subdirectories: 
* `platforms/` - implementation of bot on a variety of social networks.
* `models/` - classes of `peewee` models of data stored in `PostgreSQL` database.
* `utilities/` - additional code that takes student data from the university servers, connects the bot to the database, and so on.

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

The structure is essential meanwhile all the noted files are optional. One-file commands are exceptions, and are located at `bot/platforms/<platform>/commands/others/` directory. `bot/platforms/<platform>/commands/schedule/` directory is also an exception, and may be considered as a super-command which consists of 3 similar, but separate commands. 

## Other stuff
* `update-logs/` folder contains notes which were sent to users as update announcements.
* `cas-external-login/` folder contains some information about logging in CAS & simple login implementation.

## Design
All the stuff was drawn using [Pixelmator Pro][5]. 

[![kaishnik_bot poster][4]][3]


[1]: https://github.com/aiogram/aiogram "Repository of aiogram"
[2]: https://github.com/coleifer/peewee "Repository of peewee"
[3]: https://telegram.me/kaishnik_bot "Open the bot in Telegram"
[4]: https://github.com/airatk/kaishnik-bot/blob/main/design/poster/poster.png "kaishnik-bot poster"
[5]: https://www.pixelmator.com/pro "Pixelmator Pro"
