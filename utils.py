import json

from types import SimpleNamespace as Namespace # Maybe using something like this?


class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def get_secret() -> Config:
    try:
        with open("secret.json", "r") as f:
            return Config(**json.load(f))
    except FileNotFoundError:
        raise FileNotFoundError("File secret.json not found")
