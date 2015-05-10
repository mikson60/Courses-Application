# -*- coding: utf-8 -*-
"""
    src.frontend
    ~~~~~~~~~~~~~~~~~~

    Generic view functions module
"""


from flask import Blueprint, render_template, request, flash, redirect

from flask.ext.security import current_user

from ..forms import *
from ..models import *

from . import route


bp = Blueprint('views', __name__, static_folder="assets")

@route(bp, '/')
def index():
    return render_template('index.html')