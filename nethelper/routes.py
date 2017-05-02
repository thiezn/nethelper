"""
routes.py
~~~~~~~~~

Initialise the HTTP REST API routes/endpoints
"""

from .views import calculate_network, summarize_network, get_azure_networks
from .views import parse_mac_address
from .views import calculate_metrics
from .views import get_all_ports, get_ports


def setup_routes(app):
    """Initialises the REST API endpoints

    :param app: :class:`web.Application()` object:
    """
    app.router.add_post('/networks/calculate', calculate_network)
    app.router.add_post('/networks/summarize', summarize_network)
    app.router.add_get('/networks/list/azure', get_azure_networks)

    app.router.add_post('/mac', parse_mac_address)

    app.router.add_post('/metrics/calculate', calculate_metrics)

    app.router.add_get('/ports', get_all_ports)
    app.router.add_post('/ports', get_ports)
