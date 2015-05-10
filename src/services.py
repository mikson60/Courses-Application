# -*- coding: utf-8 -*-
"""
    src.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .users import UsersService

#: An instance of the :class:`UsersService` class
users = UsersService()
