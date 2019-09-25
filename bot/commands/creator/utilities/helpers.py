from bot import bot


def parse_creator_request(request: str) -> (str, str):
    request_words = request.split()
    
    if len(request_words) <= 1:
        return (None, None)
    
    option = request_words[1]  # The 0th index is for a command
    
    if ":" in option:
        option_data = option.split(":")
        return (option_data[0], option_data[1])
    else:
        return (option, None)

def update_progress_bar(loading_message, values: list, index: int):
    period = 20
    percent = int((index + 1)/len(values)*period)
    
    try:
        bot.edit_message_text(
            chat_id=loading_message.chat.id,
            message_id=loading_message.message_id,
            text="".join(
                [ "`[ " ] +
                [ "+" for _ in range(percent) ] +
                [ "-" for _ in range(period - percent) ] +
                [ " ]`" ]
            ),
            parse_mode="Markdown"
        )
    except Exception:
        pass
