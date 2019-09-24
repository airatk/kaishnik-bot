def clarify_markdown(string):
    is_single = False
    
    for (index, letter) in enumerate(string):
        if letter in [ "*", "_" ]:
            index = index
            is_single = not is_single
    
    return "".join([ string[:index], "\\", string[index:] ]) if is_single else string
