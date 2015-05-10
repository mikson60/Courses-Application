# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

from flask.ext.script import Manager, Shell

from src import frontend
from src.core import db

from src.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand

manager = Manager(frontend.create_app())

def shell_context():
    return dict(app=manager.app, db=db)

manager.add_command("shell", Shell(make_context=shell_context))

manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())


if __name__ == "__main__":
    manager.run()
