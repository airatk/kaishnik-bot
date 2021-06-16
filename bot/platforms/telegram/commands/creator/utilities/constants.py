from bot.utilities.constants import KEYS


CREATOR: int = int(KEYS.CREATOR)

MAX_TEXT_LENGTH: int = 3900
MAX_CAPTION_LENGTH: int = 900

CONTROL_PANEL: str = (
    "*Control panel*\n"
    "_creator access only_\n"
    "\n"
    "_{} — required, [] — optional_\n"
    "\n"
    "*stats*\n"
    "/users \[\n"
        "\t\t\t\[ month: { yyyy-mm } ]\n"
        "\t\t\t\[ me ]\n"
        "\t\t\t\[ number: {} ]\n"
        "\t\t\t\[ state: {\n"
            "\t\t\t\t\t\t\[ setup ]\n"
            "\t\t\t\t\t\t\[ unsetup ]\n"
        "\t\t\t} ]\n"
        "\t\t\t\[ user-id: {} ]\n"
        "\t\t\t\[ username: {} ]\n"
        "\t\t\t\[ firstname: {} ]\n"
        "\t\t\t\[ name: {} ]\n"
        "\t\t\t\[ group: {} ]\n"
        "\t\t\t\[ bb-login: {} ]\n"
    "]\n"
    "/metrics \[\n"
        "\t\t\t\[ date: { yyyy-mm-dd } ]\n"
        "\t\t\t\[ month: { yyyy-mm } ]\n"
    "]\n"
    "\n"
    "*cleaning*\n"
    "/clear\n"
    "/drop {\n"
        "\t\t\t{\n"
            "\t\t\t\t\t\t\[ guards ]\n"
            "\t\t\t\t\t\t\[ me ]\n"
            "\t\t\t\t\t\t\[ all ]\n"
            "\t\t\t\t\t\t\[ groups ]\n"
            "\t\t\t\t\t\t\[ compacts ]\n"
            "\t\t\t\t\t\t\[ extendeds ]\n"
            "\t\t\t\t\t\t\[ bb ]\n"
        "\t\t\t}\n"
        "\t\t\t\[ message: {} ]\n"
    "}\n"
    "\n"
    "*others*\n"
    "/broadcast {\n"
        "\t\t\t{ users: {\n"
            "\t\t\t\t\t\t\[ user-id&… ]\n"
            "\t\t\t\t\t\t\[ me ]\n"
            "\t\t\t\t\t\t\[ all ]\n"
            "\t\t\t\t\t\t\[ groups ]\n"
            "\t\t\t\t\t\t\[ compacts ]\n"
            "\t\t\t\t\t\t\[ extendeds ]\n"
            "\t\t\t\t\t\t\[ bb ]\n"
        "\t\t\t} }\n"
        "\t\t\t\[ signed: false ]\n"
        "\t\t\t{ message: {} }\n"
        "\n"
        "\t\t\tEntities to broadcast:\n"
        f"\t\t\t• message — up to {MAX_TEXT_LENGTH} characters in length.\n"
        f"\t\t\t• photo — with caption up to {MAX_CAPTION_LENGTH} characters in length.\n"
        f"\t\t\t• audio — in the .MP3 or .M4A format, with caption up to {MAX_CAPTION_LENGTH} characters in length.\n"
        f"\t\t\t• video — in the .MP4 format, up to 50 MB in size, with caption up to {MAX_CAPTION_LENGTH} characters in length.\n"
        f"\t\t\t• document — up to 50 MB in size, with caption up to {MAX_CAPTION_LENGTH} characters in length.\n"
        "\n"
    "}\n"
    "/dayoff {\n"
        "\t\t\t\[ list ]\n"
        "\t\t\t\[ add: { dd-mm } ]\n"
        "\t\t\t\[ message: {} ]\n"
        "\t\t\t\[ drop: {\n"
            "\t\t\t\t\t\t\[ mm-dd ]\n"
            "\t\t\t\t\t\t\[ all ]\n"
        "\t\t\t} ]\n"
    "}\n"
    "\n"
    "*hashtags*\n"
    "# users\n"
    "# metrics\n"
    "# data\n"
    "# cleared\n"
    "# erased\n"
    "# dropped\n"
    "# broadcast\n"
)

USERS_STATS: str = (
    "*Users*\n"
    "_stats of #users_\n"
    "\n"
    "*platforms*\n"
    "• telegram: {telegram}\n"
    "• vk: {vk}\n"
    "\n"
    "*types*\n"
    "• groups: {groups}\n"
    "• compact: {compact}\n"
    "• extended: {extended}\n"
    "• bb: {bb}\n"
    "\n"
    "*states*\n"
    "• setup: {setup}\n"
    "• unsetup: {unsetup}\n"
    "\n"
    "*{total}* users in total!"
)

COMMAND_REQUESTS_STATS: str = (
    "*Metrics*\n"
    "_monthly & daily #metrics_\n"
    "\n"
    "*commands*\n"
    "• /classes: {classes_monthly}, {classes_daily}\n"
    "• /score: {score_monthly}, {score_daily}\n"
    "• /lecturers: {lecturers_monthly}, {lecturers_daily}\n"
    "• /notes: {notes_monthly}, {notes_daily}\n"
    "• /week: {week_monthly}, {week_daily}\n"
    "• /exams: {exams_monthly}, {exams_daily}\n"
    "• /dice: {dice_monthly}, {dice_daily}\n"
    "• /locations: {locations_monthly}, {locations_daily}\n"
    "• /brs: {brs_monthly}, {brs_daily}\n"
    "• /settings: {settings_monthly}, {settings_daily}\n"
    "• /help: {help_monthly}, {help_daily}\n"
    "• /donate: {donate_monthly}, {donate_daily}\n"
    "\n"
    "• /cancel: {cancel_monthly}, {cancel_daily}\n"
    "\n"
    "• /start: {start_monthly}, {start_daily}\n"
    "• /login: {login_monthly}, {login_daily}\n"
    "\n"
    "*unknown*\n"
    "• non-text: {unknown_nontext_message_monthly}, {unknown_nontext_message_daily}\n"
    "• text: {unknown_text_message_monthly}, {unknown_text_message_daily}\n"
    "• callback: {unknown_callback_monthly}, {unknown_callback_daily}\n"
    "\n"
    "*others*\n"
    "• no permissions: {no_permissions_monthly}, {no_permissions_daily}\n"
    "• unlogin: {unlogin_monthly}, {unlogin_daily}\n"
    "\n"
    "*{total_monthly}* requests for the month.\n"
    "*{total_daily}* requests for the day.\n"
)

MONTH_GRAPH: str = (
    "*{month} Graph*\n"
    "_#{hashtag}_\n"
    "\n"
    "`{graph}`\n"
    "\n"
    "`• monthly total: {total}`\n"
    "`• daily average: {average}`\n"
)

BROADCAST_MESSAGE_TEMPLATE: str = (
    "*Телеграмма от разработчика*\n"
    "#broadcast\n"
    "\n"
    "{broadcast_message}\n"
    "\n"
    "• Поддержать бота: /donate\n"
    "• Написать разработчику: @airatk\n"
    "• Подписаться на разработчика: instagram.com/airatk.inst\n"
)
