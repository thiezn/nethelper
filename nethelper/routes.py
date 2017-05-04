"""
routes.py
~~~~~~~~~

Initialise the HTTP REST API routes/endpoints
"""
import os

from .apiviews import calculate_network, summarize_network, get_azure_networks
from .apiviews import parse_mac_address
from .apiviews import calculate_metrics
from .apiviews import get_all_ports, get_ports

from .webviews import query_page, api_page, whoarewe_page


def setup_api_routes(app):
    """Initialises the REST API routes

    :param app: :class:`web.Application()` object:
    """
    app.router.add_post('/api/v1/networks/calculate', calculate_network)
    app.router.add_post('/api/v1/networks/summarize', summarize_network)
    app.router.add_get('/api/v1/networks/list/azure', get_azure_networks)

    app.router.add_post('/api/v1/mac', parse_mac_address)

    app.router.add_post('/api/v1/metrics/calculate', calculate_metrics)

    app.router.add_get('/api/v1/ports', get_all_ports)
    app.router.add_post('/api/v1/ports', get_ports)


def setup_web_routes(app):
    """Initialises the Web routes"""
    # TODO: Static content should ideally be served by nginx.
    static_path = '{}/static'.format(os.path.dirname(os.path.realpath(__file__)))
    app.router.add_static('/static', static_path, name='static')

    app.router.add_get('/', query_page)
    app.router.add_get('/api', api_page)
    app.router.add_get('/whoarewe', whoarewe_page)
