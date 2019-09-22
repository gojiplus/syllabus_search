# -*- coding: utf-8 -*-
"""
app.views
~~~~~~~~~

Rendering application pages.
"""

from copy import deepcopy
from flask import render_template, request, abort, flash
from . import app, Course, Session, Assessment
from .parser import get_parser, get_header
from .utils import template_exists, get_conf, \
    validate_data, search, TERMS, YEARS

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
        ('stylesheet', 'text/css', 'https://cdn.datatables.net/buttons/1.5.6/css/buttons.dataTables.min.css'),
        ('stylesheet', 'text/css', 'css/style.css')
    ],
    'scripts': [
        'vendor/jquery/dist/jquery.min.js',
        'vendor/bootstrap/dist/js/bootstrap.min.js',
        'vendor/datatables.net/js/jquery.dataTables.min.js',
        'vendor/datatables.net-bs4/js/dataTables.bootstrap4.min.js',
        'vendor/datatables.net-select/js/dataTables.select.min.js',
        'vendor/datatables.net-buttons/js/dataTables.buttons.min.js',
        'vendor/datatables.net-buttons/js/buttons.flash.min.js',
        'vendor/datatables.net-buttons/js/buttons.html5.min.js',
        'vendor/datatables.net-buttons/js/buttons.print.min.js',
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


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main index page of application. Accepts both GET and POST methods"""

    kwargs = {
        'terms': TERMS, 'years': YEARS,
        'course_data': None, 'form_data': None,
        'session_h': get_header(Session), 'assess_h': get_header(Assessment)
    }

    # Method is POST
    if request.method == 'POST':
        data = {k: v for k, v in request.form.items() if v}
        if data:
            kwargs['form_data'] = dict(request.form.items())
            if validate_data(data):
                found = search(Course, **data)
                if found:
                    flash('Found %d courses' % len(found), 'success')
                    parse = get_parser(Course, with_header=True)
                    kwargs['course_data'] = parse(found)
                else:
                    flash('No result found', 'warning')
        else:
            flash('Unable to search! You have not filled in the form.', 'failed')

    # Method is GET or POST with empty data
    return _render('index', **kwargs)
