# Каист Бот

_telegram & vk bot for students of KNRTU-KAI to make their daily routine more pleasant_

### Stack
* Python
* [AIOGram][4], [VKWave][5], [Peewee ORM][6]
* PostgreSQL

#### On Telegram

[![On Telegram](https://raw.githubusercontent.com/airatk/kaishnik-bot/main/design/screenshots/telegram-screenshots.png)][1]

#### On VK
[![On VK](https://raw.githubusercontent.com/airatk/kaishnik-bot/main/design/screenshots/vk-screenshots.png)][2]


## Reason

The bot might be considered as `kai.ru` wrapper. Official mobile-unfriendly ugly inconvenient website had to be replaced by something usable. Here the [@kaishnik_bot][1] comes in.


## Setup

Since the university is located in Kazan which is the Moscow time zone, the time zone should be set to `Europe/Moscow`.

### Data
There should be `data/` folder in the root directory of the bot. It should contain `keys` non-extension file with tokens & keys accessed using `config` module.

### Launch setup
The `requirements.txt` file is included to the repository. So, use `pip3 install -r requirements.txt` to get all the necessities.
Use `python3 ./` to launch.


## Architecture

The bot is stored in project root directory folder called `bot/`. The `bot/` contains 3 subdirectories: 
* `platforms/` - implementation of the bot on a variety of social networks.
* `models/` - classes of [`peewee`][6] models of data stored in `PostgreSQL` database.
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

The structure is essential meanwhile all the noted files are optional. One-file commands are exceptions, and are located in `bot/platforms/<platform>/commands/others/` directory. `bot/platforms/<platform>/commands/schedule/` directory is also an exception, and may be considered as a super-command which consists of 3 similar, but separate commands.


## Other stuff

* `update-logs/` folder contains notes which were sent to users as update announcements.
* `design/` folder contains [`.pxd`][7] & `.png` files with all the bot associatied design.


## Design

All the stuff was drawn using [Pixelmator Pro][7].

[![kaishnik_bot poster][3]][1]


[1]: https://telegram.me/kaishnik_bot "Open the bot on Telegram"
[2]: https://vk.com/kaishnik_bot "Open the bot on VK"
[3]: https://github.com/airatk/kaishnik-bot/blob/main/design/poster/poster.png "kaishnik-bot poster"
[4]: https://github.com/aiogram/aiogram "Repository of aiogram"
[5]: https://github.com/fscdev/vkwave "Repository of vkwave"
[6]: https://github.com/coleifer/peewee "Repository of peewee"
[7]: https://www.pixelmator.com/pro "Pixelmator Pro"
