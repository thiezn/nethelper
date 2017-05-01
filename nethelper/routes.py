"""
routes.py
~~~~~~~~~

Initialises all the HTTP REST API routes
"""

from .views import index


def setup_routes(app):
    app.router.add_get('/', index)
    print('Adding route /')
