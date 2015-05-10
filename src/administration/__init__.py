# -*- coding: utf-8 -*-
"""
    kindlustus.administration
    ~~~~~~~~~~~~~~~~~~

"""
from functools import wraps
from base64 import b64encode

from flask import g, session, request, jsonify, render_template,\
    redirect, current_app, abort
from flask.ext.security import login_required, roles_accepted
from flask.ext.assets import Environment


from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)
    app.static_folder = "assets"
    Environment(app)

    def custom_datetimeformat(value, format='%d.%m.%Y'):
        return value.strftime(format)

    if not app.debug:
        import logging
        from logging import FileHandler
        file_handler = FileHandler("admin_error_log.txt")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

    @route(app, '/')
    def index():
        return render_template("layouts/administration.html")

    return app


def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @roles_accepted('ADMIN')
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
