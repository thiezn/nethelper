"""
views.py
~~~~~~~~

Holds all the REST API views
"""

from aiohttp import web
import aiohttp_jinja2
from .models import IPv4Network, Port, MacAddress


@aiohttp_jinja2.template('query.html')
async def query_page(request):
    """Serving the main webpage querying networks, mac's and ports"""

    # Retrieve client connection details
    peername = request.transport.get_extra_info('peername')
    try:
        client_ip, client_port = peername
    except:
        client_ip, client_port = None, None

    data = {
        'query_page_active': True,
        'client_ip': client_ip,
        'client_port': client_port,
        'client_headers': request.headers
    }

    # Parse network query
    try:
        try:
            data['network'] = IPv4Network(request.query['network'])

        except ValueError:
            pass
    except KeyError:
        pass

    # Parse port query
    try:
        data['port'] = Port(int(request.query['port']), 'tcp')
    except KeyError:
        pass

    # Parse mac query
    try:
        data['mac'] = MacAddress(request.query['mac'])
    except KeyError:
        pass

    return data


@aiohttp_jinja2.template('api.html')
async def api_page(request):
    return {'api_page_active': True}


@aiohttp_jinja2.template('whoarewe.html')
async def whoarewe_page(request):
    return {'whoarewe_page_active': True}
