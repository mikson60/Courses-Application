# -*- coding: utf-8 -*-
"""
    src.manage.users
    ~~~~~~~~~~~~~~~~~~~~~~~~

    User management commands
"""


from flask.ext.script import Command, prompt, prompt_pass
from flask.ext.security.utils import encrypt_password
from flask.ext.security import RegisterForm

from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy

from flask import current_app

from ..services import users

import datetime


_security  = LocalProxy(lambda: current_app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)





class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt('Email')
        user = users.first(email=email)
        if not user:
            print('Invalid user')
            return
        users.delete(user)
        print('User deleted successfully')


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        for u in users.all():
            print('User(id=%s email=%s)' % (u.id, u.email))
