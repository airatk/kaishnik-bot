def clarify_markdown(string: str) -> str:
    index: int = 0
    is_single: bool = False
    
    for (letter_index, letter) in enumerate(string):
        if letter in [ "*", "_" ]:
            (index, is_single) = (letter_index, not is_single)
    
    return "\\".join([ string[:index], string[index:] ]) if is_single else string
