# -*- coding: utf-8 -*-
"""
    veoauto.users
    ~~~~~~~~~~~~~~

    veoauto users package
"""

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User
