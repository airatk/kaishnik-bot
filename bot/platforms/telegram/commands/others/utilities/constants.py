from bot.utilities.constants import BOT_ADDRESSING


BRS: str = (
    "*БРС*\n"
    "_балльно-рейтинговая система_\n"
    "\n"
    "Обычно можно получить *50* баллов за семестр и столько же за экзамен. *100* баллов всего.\n"
    "\n"
    "• 3ка - от *51* до *70*\n"
    "• 4ка - от *71* до *85*\n"
    "• 5ка - от *86* до *100*\n"
    "\n"
    "Для зачёта достаточно получить *51* балл в сумме.\n"
)

HELP: str = (
    "*~$ kbot --help*\n"
    "\n"
    "*classes & exams*\n"
    "• Для того, чтобы узнать расписание занятий другой группы, введи /classes *[ группа ]*\n"
    "• То же работает с /exams\n"
    "\n"
    "*notes*\n"
    "• При добавлении новой заметки можно выделить текст \**жирным*\* или \__курсивом_\_, обособив его звёздочками или нижним подчёркиванием.\n"
    "\n"
    "*settings*\n"
    "• Расписание может отображаться в полном и компактном форматах. В первом режиме доступны время-место, название и тип пары, а также имя преподавателя и кафедра предмета. Во втором — имени преподавателя и кафедры предмета нет, а тип предмета укорочен: *Л* — лекция, *П* — практика, *ЛР* — лабораторная работа, *К* — консультация, а также *(п)* — для обозначения потокового занятия.\n"
    "\n"
    "*групповые чаты*\n"
    "• Бота можно добавить в групповой чат. Необходимо сделать его админом и не запрещать ему удалять сообщения.\n"
    "• Текстовые сообщения должны начинаться с обращения {bot_addressing} либо быть реплаями, команды — не должны:\n"
    "• /command\n"
    "• {bot_addressing} текст\n"
    "• текст (в случае, если реплай)\n"
    "\n"
    "*другое*\n"
    "• Внутри бота реализована GUARD-система, не позволяющая захламлять чат. Для того, чтобы второй запрос стал доступен, необходимо завершить или отменить первый.\n"
    "\n"
    "*ссылки*\n"
    "• Каист в ВК: vk.com/kaishnik\_bot\n"
    "• Исходный код Каиста: github.com/airatk/kaishnik-bot\n"
    "• Инстаграм разработчика: instagram.com/airatk.inst\n"
    "• ВК разработчика: vk.com/airatk\n"
    "\n"
    # "_Бот был написан студентом во время учёбы на 1 курсе с применением исключительно самостоятельно полученных знаний, без какого-либо доступа к каким-либо API КАИ._\n"
    # "\n"
    "Хотелки, жалобы, любые интересующие вопросы — разработчику: @airatk\n"
).format(bot_addressing=BOT_ADDRESSING[:-1])

DONATE: str = (
    "Если тебе понравился бот, ты можешь добровольно отблагодарить разработчика денежным донатом:\n"
    "\n"
    "• *Сбер*: 2202 2012 3023 9101\n"
    "• *PayPal*: paypal.me/kamairat\n"
    "\n"
    "Спасибо, что пользуешься ботом!☺️\n"
)

DICE: str = "🏀"
