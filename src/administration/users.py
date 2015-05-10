# -*- coding: utf-8 -*-
"""
    src.administration.users
    ~~~~~~~~~~~~~~~~~~~~~

    Users administration controller
"""

from flask import Blueprint, render_template, abort, request
from flask.json import jsonify

from ..models import User, Role
from ..core import db

from . import route

bp = Blueprint('users', __name__, template_folder='templates/', url_prefix="/users")


@route(bp, '/')
def index():
    return render_template("misc/users.html")


@route(bp, '/list')
def list():
    users = {}

    for u in User.query.all(): #TODO: pagination
        o = {}
        o["email"] = u.email
        o["first_name"] = u.first_name
        o["roles"] = {r.id:r.name for r in u.roles}
        users[u.id] = o

    roles = { r.id:r.name for r in Role.query.all() }
    return jsonify({"users":users, "all_roles": roles})


@route(bp, '/action')
def action():
    action = request.args.get("action", None)

    if action is None:
        print(action)
        print("action is none")
        return abort(404)

    resp = {}
    if action == "addRole":
        r = Role.query.filter_by(id=request.args.get("role_id", None, type=int)).first_or_404()
        u = User.query.filter_by(id=request.args.get("user_id", None, type=int)).first_or_404()
        if r not in u.roles:
            u.roles.append(r)
            db.session.commit()
        resp["role"] = r.name
    elif action == "remRole":
        r = Role.query.filter_by(id=request.args.get("role_id", None, type=int)).first_or_404()
        u = User.query.filter_by(id=request.args.get("user_id", None, type=int)).first_or_404()
        if r in u.roles:
            u.roles.remove(r)
            db.session.commit()
    else:
        return abort(404)

    return jsonify(resp)
