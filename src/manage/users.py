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


class CreateUserCommand(Command):
    """Create a user"""

    def run(self):
        email            = prompt('Email')
        password         = prompt_pass('Password')
        password_confirm = prompt_pass('Confirm Password')
        first_name       = prompt('First name')
        last_name        = prompt('Last name')

        data             = MultiDict(dict(email=email, password=password,
                                          password_confirm=password_confirm,
                                          first_name=first_name,
                                          last_name=last_name))
        form             = RegisterForm(data, csrf_enabled=False)

        if form.validate():
            user = _datastore.create_user(email=email,
                                          password=encrypt_password(password),
                                            first_name=first_name,
                                            last_name=last_name, active=True,
                                            confirmed_at=datetime.datetime.utcnow())
            get_or_create_role = _datastore.find_or_create_role("ADMIN")
            _datastore.add_role_to_user(user, get_or_create_role)
            _datastore.commit()

            print('\nUser created successfully')
            print('User(id=%s email=%s)' % (user.id, user.email))
            return

        print('\nError creating user:')
        for errors in form.errors.values():
            print('\n'.join(errors))


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
