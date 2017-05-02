"""
views.py
~~~~~~~~

Holds all the REST API views
"""

from aiohttp import web
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index_page(request):
    return {
        'results': ['hello', 'world']
    }


@aiohttp_jinja2.template('api.html')
async def api_page(request):
    pass


@aiohttp_jinja2.template('contact.html')
async def contact_page(request):
    pass


@aiohttp_jinja2.template('about.html')
async def about_page(request):
    pass


async def query(request):
    """Parse POSTed query and call the correct models for
    networks, ports or mac addresses
    """
    data = await request.post()
    return web.Response(text=data['query'])
