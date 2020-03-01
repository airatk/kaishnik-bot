from bot.shared.data.constants import USERS_FILE

from pickle import load
from pickle import dump


def save_data(file: str, object: None):
    with open(file, "wb") as file:
        dump(object, file, protocol=4)

def load_data(file: str) -> None:
    with open(file, "rb") as file:
        return load(file)
