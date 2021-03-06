import json

default_local = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_local}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
