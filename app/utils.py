import os, datetime, nltk
from . import app, db, config, Course, Session, Assessment, APP_PATH
from flask import url_for, request, flash
from configparser import NoOptionError, NoSectionError
from sqlalchemy import and_, or_

__all__ = [
    'getpath',
    'template_exists',
    'get_conf',
    'list_parser',
    'validate_data',
    'search',
    'TERMS',
    'YEARS'
]

try:
    stopwords = set(nltk.corpus.stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(nltk.corpus.stopwords.words('english'))


def getpath(*path):
    if path:
        path = os.path.join(*path)
        if os.path.isabs(path):
            return path
        return os.path.join(APP_PATH, path)
    return APP_PATH


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
                if start.isdigit() and (end.isdigit() or end in ('current', 'now')):
                    if end in ('current', 'now'):
                        end = datetime.datetime.now().year
                    ret = []
                    start, end = int(start), int(end)
                    while start <= end:
                        ret.append(start)
                        start += 1
                    if ret:
                        return ret
        return [string.strip()]
    return []


TERMS = list_parser(get_conf('search_form', 'terms', fallback=''))
YEARS = list_parser(get_conf('search_form', 'years', fallback=''))


def build_keywords(string: str):
    def combine(s):
        return ' & '.join([
            w.lower() for w in s.split() if w.lower() not in stopwords])

    phrases = string.split(' OR ')
    enclosed = lambda s: '&' in s and len(phrases) > 1
    fmt = lambda s: ('({})' if enclosed(s) else '{}').format(s)
    return ' | '.join([fmt(combine(phrase)) for phrase in phrases if phrase])


def validate_data(data):
    required = set()
    missing = required - (required & set(data))
    if missing:
        flash('Missing required fields: %s' % ', '.join(str(i) for i in missing), 'failed')
        return False

    t1, t2 = data.get('start_term'), data.get('end_term')
    y1, y2 = data.get('start_year'), data.get('end_year')

    y1 = int(y1) if y1 else None
    y2 = int(y2) if y2 else None

    if t1 and t1 not in TERMS:
        flash('Unexpected starting term: %s' % t1, 'failed')
        return False
    if t2 and t2 not in TERMS:
        flash('Unexpected ending term: %s' % t2, 'failed')
        return False
    if y1 and y1 not in YEARS:
        flash('Unexpected starting year: %d' % y1, 'failed')
        return False
    if y2 and y2 not in YEARS:
        flash('Unexpected starting year: %d' % y1, 'failed')
        return False
    if t1 and not y1:
        flash('Start year is missing', 'failed')
        return False
    if y1 and not t1:
        flash('Start term is missing', 'failed')
        return False
    if t2 and not y2:
        flash('End year is missing', 'failed')
        return False
    if y2 and not t2:
        flash('End term is missing', 'failed')
        return False

    if y1 and y2:
        p1, p2 = TERMS.index(t1), TERMS.index(t2)
        if any([y1 > y2, y1 == y2 and p1 > p2]):
            flash('End period must come after start period', 'failed')
            return False

    return True


def build_query(**kwargs):
    course_id = kwargs.get('course_id')
    start_term = kwargs.get('start_term')
    end_term = kwargs.get('end_term')
    start_year = kwargs.get('start_year')
    end_year = kwargs.get('end_year')
    keywords = kwargs.get('keyword', kwargs.get('keywords'))

    if course_id:
        course_id = int(course_id)
    if start_year:
        start_year = int(start_year)
    if end_year:
        end_year = int(end_year)

    if start_year and start_year == end_year and start_term == end_term:
        start_term, end_term = end_term, None
        start_year, end_year = end_year, None

    conditions = ()

    if course_id:
        conditions += (Course.id == course_id,)

    if start_year and end_year:
        p1, p2 = TERMS.index(start_term), TERMS.index(end_term)
        if start_year == end_year:
            conditions += (
                Course.term.in_(TERMS[p1:p2 + 1]),
                Course.year == start_year
            )

        else:
            periods = (and_(
                Course.term.in_(TERMS[p1:]),
                Course.year == start_year
            ),)

            if start_year + 1 < end_year:
                if start_year + 1 < end_year - 1:
                    periods += (Course.year.between(start_year + 1, end_year - 1),)
                else:
                    periods += (Course.year == start_year + 1,)

            periods += (and_(
                Course.term.in_(TERMS[:p2 + 1]),
                Course.year == end_year
            ),)

            conditions += (or_(*periods),)

    elif start_year:
        p1 = TERMS.index(start_term)
        conditions += (or_(
            and_(Course.term.in_(TERMS[p1:]), Course.year == start_year),
            Course.year > start_year
        ),)

    elif end_year:
        p2 = TERMS.index(end_term)
        conditions += (or_(
            Course.year < end_year,
            and_(Course.term.in_(TERMS[:p2 + 1]), Course.year == end_year)
        ),)

    if keywords:
        keywords = build_keywords(keywords)
        if keywords:
            conditions += (or_(
                Course.document.match(keywords),
                Session.document.match(keywords),
                Assessment.document.match(keywords)
            ),)

    return conditions


def search(entity, **kwargs):
    entities = {Course, Session, Assessment}
    assert entity in entities, entity

    table = db.query(entity).join(Course.sessions, Course.assessments)
    conditions = build_query(**kwargs)

    try:
        return table.filter(*conditions).all()
    except:
        return None
