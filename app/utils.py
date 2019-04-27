import os
from configparser import ConfigParser

__all__ = [
    'getpath',
    'config'
]

MAIN_DIR = os.path.dirname(os.path.dirname(__file__))


def getpath(*path):
    if path:
        path = os.path.join(*path)
        if os.path.isabs(path):
            return path
        return os.path.join(MAIN_DIR, path)
    return MAIN_DIR


config = ConfigParser(
    converters={
        'dict': lambda s: {
            k.strip(): v.strip()
            for k, v in (i.split(':') for i in s.split('\n'))
        } if s != 'null' else {},
        'list': lambda s: s.split(',' if ',' in s else None) if s != 'null' else []
    }
)
config.read(getpath('config.ini'))
