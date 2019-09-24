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
