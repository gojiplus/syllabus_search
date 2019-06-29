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
    'search_courses'
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


def build_keywords(string: str):
    def combine(s):
        return ' & '.join([
            w.lower() for w in s.split() if w.lower() not in stopwords])

    phrases = string.split(' OR ')
    enclosed = lambda s: '&' in s and len(phrases) > 1
    fmt = lambda s: ('({})' if enclosed(s) else '{}').format(s)
    return ' | '.join([fmt(combine(phrase)) for phrase in phrases if phrase])


def search_courses(**kwargs):
    def parse_row(obj: Course):
        tas = ', '.join(i for i in obj.tas)
        cats = ', '.join(c.name for c in obj.categories)
        instructors = ', '.join(
            '{}{}'.format(i.name, ' ({})'.format(', '.join(i.degrees)) if i.degrees else '')
            for i in obj.instructors
        )
        return [obj.name, cats, obj.year, obj.term, obj.credits, obj.faculty,
                instructors, tas, obj.num_assessments, obj.num_sessions]

    header = ['Name', 'Categories', 'Year', 'Term', 'Credits',
              'Faculty', 'Instructors', 'TAs', 'No. Assess.', 'No. Sessions']

    start_term = kwargs.get('start_term')
    end_term = kwargs.get('end_term')
    start_year = kwargs.get('start_year')
    end_year = kwargs.get('end_year')
    keywords = kwargs.get('keyword')

    conditions = ()
    if start_term and end_term:
        if start_term == end_term:
            conditions += (Course.term == start_term,)
        else:
            conditions += (Course.term.in_([start_term, end_term]),)
    elif start_term or end_term:
        term = start_term or end_term
        conditions += (Course.term == term,)

    if start_year and end_year:
        if start_year == end_year:
            conditions += (Course.year == int(start_year),)
        elif start_year < end_year:
            conditions += (Course.year.between(int(start_year), int(end_year)),)
        else:
            raise NotImplementedError
    elif start_year or end_year:
        conditions += (Course.year == int(start_year or end_year),)

    if keywords:
        keywords = build_keywords(keywords)
        if keywords:
            course_ids = [i[0] for i in {
                *db.query(Session.course_id).filter(Session.document.match(keywords)).all(),
                *db.query(Assessment.course_id).filter(Assessment.document.match(keywords)).all()
            }]
            if course_ids:
                conditions += (or_(Course.document.match(keywords), Course.id.in_(course_ids)),)
            else:
                conditions += (Course.document.match(keywords),)

    try:
        courses = db.query(Course).filter(and_(*conditions)).all()
        if courses:
            flash('Found %d results' % len(courses), 'success')
            return [header, *(parse_row(i) for i in courses)]
    except:
        pass

    flash('No result found', 'warning')
    return None
