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
from . import app
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
        ('stylesheet', 'text/css', 'vendor/datatables.net-dt/css/jquery.dataTables.min.css'),
        ('stylesheet', 'text/css', 'css/style.css')
    ],
    'scripts': [
        'vendor/jquery/dist/jquery.min.js',
        'vendor/popper.js/dist/popper.min.js',
        'vendor/bootstrap/dist/js/bootstrap.min.js',
        'vendor/datatables.net/js/jquery.dataTables.min.js',
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

    # Method is POST
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        if keywords:
            return redirect(url_for('result', keywords=quote(keywords)))

    # Method is GET or POST with empty data
    return _render('index')

