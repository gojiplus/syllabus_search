import os
from . import app
from configparser import ConfigParser, NoOptionError, NoSectionError

__all__ = [
    'getpath',
    'config',
    'template_exists',
    'get_conf'
]

MAIN_DIR = os.path.dirname(app.root_path)


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


def template_exists(template):
    return os.path.exists(os.path.join(app.root_path, app.template_folder, template))


def get_conf(section, option, fallback=None):
    try:
        return config.get(section, option)
    except (NoOptionError, NoSectionError):
        return fallback
