import os
from . import app
from flask import url_for, request
from configparser import ConfigParser, NoOptionError, NoSectionError

__all__ = [
    'getpath',
    'config',
    'template_exists',
    'get_conf',
    'list_parser'
]

MAIN_DIR = os.path.dirname(app.root_path)


def getpath(*path):
    if path:
        path = os.path.join(*path)
        if os.path.isabs(path):
            return path
        return os.path.join(MAIN_DIR, path)
    return MAIN_DIR


config = ConfigParser()
config.read(getpath('config.ini'))


def endswith(str1, str2):
    return str1.lower().endswith(str2.lower())


def static_url(filename):
    if filename.startswith('http://') or filename.startswith('https://'):
        return filename
    return url_for('static', filename=filename)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.tests['endswith'] = endswith
app.jinja_env.filters['static_url'] = static_url
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def template_exists(template):
    return os.path.exists(os.path.join(app.root_path, app.template_folder, template))


def get_conf(section, option, fallback=None):
    try:
        return config.get(section, option)
    except (NoOptionError, NoSectionError):
        return fallback


def list_parser(string: str):
    if string:
        if ',' in string:
            return [s.strip() for s in string.split(',')]
        if '-' in string:
            try:
                start, end = [s.strip() for s in string.split('-')]
            except ValueError:
                pass
            else:
                if start.isdigit() and end.isdigit():
                    ret = []
                    start, end = int(start), int(end)
                    while start <= end:
                        ret.append(start)
                        start += 1
                    if ret:
                        return ret
        return [string.strip()]
    return []
