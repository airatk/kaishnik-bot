# Каист
_telegram bot for students of KNRTU-KAI to make their daily routine more pleasant_

### Stack
* Python
* [aiogram][1]

## Reason
The bot might be considered as `kai.ru` & `old.kai.ru` wrapper. Official mobile-unfriendly ugly inconvenient website had to be replaced by something more usable. Here the [@kaishnik_bot][2] comes up.

## Setup

The time zone should be set to `Europe/Moscow` as well (since the university's located in Kazan in Moscow time zone).

### Data
There should be `data/` folder in the root directory of the bot. It should contant the following non-extension files with data in binary form:
* `users` file with dictionary which contains `chat_id: Student` pairs.
* `is_week_reversed` file with a boolean value which is used to define the correct type of a week. 
* `keys` file is used to store tokens & keys accessed using `config` module.

### Launch setup
The `requirements.txt` file is included to the repository. So, enter `pip3 install -r requirements.txt` to get all the necessary stuff.
Type `python3 . -m 'launch mode'` to launch where `launch mode` is either `testing` or `eternal`.

## Commands
* **classes** - занятия
* **score** - баллы
* **lecturers** - преподаватели
* **notes** - заметки
* **week** - чётность недели
* **exams** - экзамены
* **locations** - здания КАИ
* **card** - номер зачётки
* **brs** - что за БРС?
* **edit** - изменить расписание
* **login** - вход
* **me** - ты
* **donate** - сказать спасибо
* **help** - подсказки
* **cancel** - отменить команду

Each command has its own directory:

    *command_name*/
        *command_file*.py
        *command_file*.py
        guard.py
        utilities/
            keyboards.py
            helpers.py
            constants.py
            types.py

The structure is essential meanwhile all the noted files are optional. One-file commands are exceptions & are located at `bot/commands/others/` directory.

## Other stuff
* `update-logs/` folder contains notes which were sent to users as update announcements.
* `cas-external-login/` folder contains some information about loginning into CAS & its simple implementation.

## Design
All the stuff was drawn using Pixelmator Pro. 

![kaishnik_bot logo][5]
![kaishnik_bot poster][6]


[1]: https://github.com/aiogram/aiogram "Repository of aiogram"
[2]: https://telegram.me/kaishnik_bot "Open the bot in Telegram"
[3]: https://telegram.me/BotFather "Open BotFather in Telegram"
[4]: https://core.telegram.org/bots/api "Telegram Bot API official reference"
[5]: https://github.com/AiratK/kaishnik-bot/blob/master/design/logo.png "kaishnik-bot logo"
[6]: https://github.com/AiratK/kaishnik-bot/blob/master/design/poster.png "kaishnik-bot poster"
[7]: https://www.pixelmator.com/pro "Pixelmator Pro"
