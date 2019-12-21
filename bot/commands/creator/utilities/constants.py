from bot import keys


CREATOR: int = int(keys.CREATOR)

CONTROL_PANEL: str = (
    "*Control panel*\n"  # {} - required, [] - optional
    "_creator access only_\n"
    "\n*stats*\n"  # commands of bot usage statistics
    "/users\n"
    "/metrics \[ drop ]\n"
    "/data {\n"
        "\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
        "\t\t\t\[ number:{} ]\[ index:{} ]\n"
        "\t\t\t\[ name:{} ]\[ group:{} ]\n"
        "\t\t\t\[ year:{} ]\n"
    "}\n"
    "\n*cleanning*\n"  # commands to get rid of inactive users
    "/clear\n"
    "/erase {\n"
        "\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
        "\t\t\t\[ :chat ID 1: … … ]\n"
    "}\n"
    "/drop { all }\n"
    "/guarddrop {\n"
        "\t\t\t\[ all ]\n"
        "\t\t\t\[ :chat ID 1: … … ]\n"
    "}\n"
    "\n*others*\n"  # uncategorised commands
    "/broadcast { :message: }\n"
    "/reverse { week }\n"
    "\n*hashtags*\n"  # hashtags
    "# users\n"
    "# metrics\n"
    "# data\n"
    "# erased\n"
    "# broadcast\n"
    "# dropped\n"
    "# guarddropped\n"
    "# reversed"
)

USERS_STATS: str = (
    "*Users*\n"
    "_stats of_ #users\n"
    "\n*institutes*\n"  # institutes
    "• {faculty_1}: {number_faculty_1}\n"
    "• {faculty_2}: {number_faculty_2}\n"
    "• {faculty_3}: {number_faculty_3}\n"
    "• {faculty_4}: {number_faculty_4}\n"
    "• {faculty_5}: {number_faculty_5}\n"
    "• {faculty_6}: {number_faculty_6}\n"
    "\n*years*\n"  # year
    "• {year_1}: {number_year_1}\n"
    "• {year_2}: {number_year_2}\n"
    "• {year_3}: {number_year_3}\n"
    "• {year_4}: {number_year_4}\n"
    "• {year_5}: {number_year_5}\n"
    "• {year_6}: {number_year_6}\n\n"
    "*group only*: {number_group_only}\n"  # group only
    "*unsetup*: {number_unsetup}\n\n"  # unsetup
    "*{total}* users in total!"  # total
)

COMMAND_REQUESTS_STATS: str = (
    "*Metrics*\n"
    "_daily_ #metrics\n"
    "\n*usage*\n"  # main commands requests number
    "/classes: {classes_request_number}\n"
    "/score: {score_request_number}\n"
    "/lecturers: {lecturers_request_number}\n"
    "/week: {week_request_number}\n"
    "/notes: {notes_request_number}\n"
    "/exams: {exams_request_number}\n"
    "/locations: {locations_request_number}\n"
    "/card: {card_request_number}\n"
    "/brs: {brs_request_number}\n"
    "/me: {me_request_number}\n"
    "/cancel: {cancel_request_number}\n"
    "\n*setup*\n"  # setup commands requests number
    "/start: {start_request_number}\n"
    "/login: {login_request_number}\n"
    "unlogin: {unlogin_request_number}\n"
    "\n*other*\n"  # uncategorised commands requests number
    "/edit: {edit_request_number}\n"
    "/help: {help_request_number}\n"
    "/donate: {donate_request_number}\n"
    "unknown: {unknown_request_number}\n"  # unknown commands requests number
    "\n*{total_request_number}* requests in total!"  # total requests number
)

USER_DATA: str = (
    "{firstname} {lastname} @{username}\n"
    "chat id {chat_id}\n\n"
    "• Institute: {institute}\n"
    "• Year: {year}\n"
    "• Group: {group_number}\n"
    "• Name: {name}\n"
    "• Card: {card}\n\n"
    "• Notes: {notes_number}\n"
    "• Edited subjects: {edited_classes_number}\n"
    "• Fellow students: {fellow_students_number}\n\n"
    "• Is full: {is_full}\n"
    "• Guard text: {guard_text}\n"
    "• Is guard message none: {is_guard_message_none}\n\n"
    "#{hashtag}"
)

BROADCAST_MESSAGE_TEMPLATE: str = (
    "*Телеграмма от разработчика*\n"
    "#broadcast\n\n"
    "{broadcast_message}\n\n"
    "Поддержать бота финансово: /donate\n"
    "Написать разработчику: @airatk"
)
