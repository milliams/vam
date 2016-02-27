import os
import pathlib


def home() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser('~'))


def vam_dir() -> pathlib.Path:
    return home() / '.vam'


def packages():
    return [x for x in vam_dir().iterdir() if x.is_dir()]

