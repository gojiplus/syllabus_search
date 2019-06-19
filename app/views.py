# -*- coding: utf-8 -*-
"""
app.views
~~~~~~~~~

Rendering application pages.
"""

from copy import deepcopy
from urllib.parse import quote, unquote
from flask import render_template, request, \
    abort, flash, Response, url_for, redirect
from . import app, db, Course
from .utils import template_exists, get_conf

GLOBAL_VARS = {
    'navbar': [
        # (href, caption)
    ],
    'links': [
        # (rel, type, file)
        ('icon', 'image/x-icon', 'img/favicon-32.png'),
        ('shortcut icon', 'image/x-icon', 'img/favicon-32.png'),
        ('stylesheet', 'text/css', 'vendor/bootstrap/dist/css/bootstrap.min.css'),
        ('stylesheet', 'text/css', 'vendor/datatables.net-bs4/css/dataTables.bootstrap4.min.css'),
        ('stylesheet', 'text/css', 'vendor/datatables.net-select-bs4/css/select.bootstrap4.min.css'),
        ('stylesheet', 'text/css', 'css/style.css')
    ],
    'scripts': [
        'vendor/jquery/dist/jquery.min.js',
        'vendor/datatables.net/js/jquery.dataTables.min.js',
        'vendor/datatables.net-bs4/js/dataTables.bootstrap4.min.js',
        'vendor/datatables.net-select/js/dataTables.select.min.js',
        'js/app.js'
    ]
}


def _render(page, **kwargs):
    # Check page template
    template = '%s.html' % page
    if not template_exists(template):
        abort(404, 'Page not found')

    # Prepare variables
    variables = deepcopy(GLOBAL_VARS)
    title = get_conf(page, 'title')
    header = get_conf(page, 'header')
    intro = get_conf(page, 'intro')
    if title:
        variables['title'] = title
    if header:
        variables['header'] = header
    if intro:
        variables['intro'] = intro
    variables.update(kwargs)

    # Render template
    return render_template(template, **variables)


def search_courses():
    # noinspection PyTypeChecker
    def parse_row(obj: Course):
        instructors = ', '.join(i.name for i in obj.instructors)
        tas = ', '.join(i for i in obj.tas)
        return [obj.name, obj.year, obj.term, obj.credits, obj.faculty,
                instructors, tas, len(obj.assessments), len(obj.sessions)]

    data = [['Name', 'Year', 'Term', 'Credits', 'Faculty',
             'Instructors', 'TAs', 'No. Assess.', 'No. Sessions']]
    for i in db.query(Course).all():
        data.append(parse_row(i))
    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main index page of application. Accepts both GET and POST methods"""

    def form_data():
        return {k: quote(v) for k, v in request.form.items() if v}

    # Method is POST
    if request.method == 'POST':
        data = form_data()
        if data:
            return redirect(url_for('result', **data))

    # Method is GET or POST with empty data
    return _render('index', course_data=search_courses())
