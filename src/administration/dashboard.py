# -*- coding: utf-8 -*-
"""
    src.administration.dashboard
    ~~~~~~~~~~~~~~~~~~

    Admin dashboard controller
"""
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for

from . import route

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates/')


@route(bp, "/")
def index():
    return render_template("index.html")
