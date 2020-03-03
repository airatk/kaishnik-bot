from pickle import load
from pickle import dump


def save_data(file: str, object: None):
    with open(file, "wb") as opened_file:
        dump(object, opened_file, protocol=4)

def load_data(file: str) -> None:
    with open(file, "rb") as opened_file:
        return load(opened_file)
