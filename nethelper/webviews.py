"""
views.py
~~~~~~~~

Holds all the REST API views
"""

from aiohttp import web


async def index_page(request):
    data = '<html><body>Hello index page!!</body></html>'
    return web.Response(data)

async def contact_page(request):
    data = '<html><body>Hello contact page!!</body></html>'
    return web.Response(data)
