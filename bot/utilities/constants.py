from config import Config


KEYS_FILE: str = "data/keys"

with open(KEYS_FILE) as keys_file:
    KEYS: Config = Config(keys_file)


BOT_ADDRESSING: str = "/kaist"" "  # The ending whitespace was added for style purposes
