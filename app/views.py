# -*- coding: utf-8 -*-
"""
app.views
~~~~~~~~~

Rendering application pages.
"""

from copy import deepcopy
from flask import render_template, request, abort, flash
from . import app
from .utils import template_exists, get_conf, list_parser, search_courses

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
        'vendor/bootstrap/dist/js/bootstrap.min.js',
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


def validate_data(data, terms, years):
    required = {'start_term', 'end_term', 'start_year', 'end_year'}
    missing = required - (required & set(data))
    if missing:
        flash('Missing required fields: %s' % ', '.join(str(i) for i in missing), 'failed')
        return False

    t1, t2 = data['start_term'], data['end_term']
    y1, y2 = int(data['start_year']), int(data['end_year'])

    if t1 not in terms:
        flash('Unexpected starting term: %s' % t1, 'failed')
        return False
    if t2 not in terms:
        flash('Unexpected ending term: %s' % t2, 'failed')
        return False
    if y1 not in years:
        flash('Unexpected starting year: %d' % y1, 'failed')
        return False
    if y2 not in years:
        flash('Unexpected starting year: %d' % y1, 'failed')
        return False

    if y1 < y2:
        return True
    elif y1 == y2:
        p1, p2 = terms.index(t1), terms.index(t2)
        if p1 <= p2:
            return True

    flash('Expected time range must be sooner to later', 'failed')
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main index page of application. Accepts both GET and POST methods"""

    terms = list_parser(get_conf('search_form', 'terms', fallback=''))
    years = list_parser(get_conf('search_form', 'years', fallback=''))

    kwargs = {
        'course_data': None, 'form_data': None, 'terms': terms, 'years': years
    }

    # Method is POST
    if request.method == 'POST':
        data = {k: v for k, v in request.form.items() if v}
        reset = data.pop('reset', False)
        if reset is False:
            if data:
                kwargs['form_data'] = dict(request.form.items())
                if validate_data(data, terms, years):
                    kwargs['course_data'] = search_courses(**data)
            else:
                flash('Unable to search! You have not filled in the form.', 'failed')

    # Method is GET or POST with empty data
    return _render('index', **kwargs)
