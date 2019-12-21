def clarify_markdown(string: str) -> str:
    is_single: bool = False
    
    for (index, letter) in enumerate(string):
        if letter in [ "*", "_" ]:
            index: int = index
            is_single: bool = not is_single
    
    return "".join([ string[:index], "\\", string[index:] ]) if is_single else string
