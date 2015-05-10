# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    playtech wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from src import frontend, administration

application = DispatcherMiddleware(frontend.create_app(), {
    '/administration': administration.create_app()
})


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
