"""
views.py
~~~~~~~~

Holds all the REST API views
"""

from aiohttp import web
from .models import IPv4Network, MacAddress, NetworkMetric, Port
import json


def raise_generic_json_error():
    raise web.HTTPBadRequest(
        text=json.dumps({'error': 'incorrect json payload'}),
        content_type='application/json'
    )


async def calculate_network(request):
    """Calculate network details"""
    data = await request.json()

    if 'netmask' in data and 'bitmask' in data:
        raise web.HTTPBadRequest(
            body={'error': 'Please don\'t provide bitmask and netmask together'},
            content_type='application/json'
        )

    if 'netmask' in data:
        network = IPv4Network(data['network'], netmask=data['netmask'])
    elif 'bitmask' in data:
        network = IPv4Network(data['network'], bitmask=data['bitmask'])
    elif 'network' in data and '/' in data['network']:
        # TODO use IPv4Network exception to handle the checking of correct syntax better
        network = IPv4Network(data['network'])
    else:
        raise_generic_json_error()

    return web.json_response(network.to_json())

async def summarize_network(request):
    data = await request.json()
    return web.json_response(data)

async def get_azure_networks(request):
    data = {'hello': 'world'}
    return web.json_response(data)

async def parse_mac_address(request):
    data = await request.json()

    try:
        mac_address = MacAddress(data['mac_address'])
    except KeyError:
        raise_generic_json_error()

    return web.json_response(mac_address.to_json())

async def calculate_metrics(request):
    data = await request.json()

    # Default to round values to 4 digits
    if 'round_to' not in data:
        data['round_to'] = 4

    if 'bps' in data:
        metric = NetworkMetric.from_bits(data['bps'], data['round_to'])
    elif 'kbps' in data:
        metric = NetworkMetric.from_kilobits(data['kbps'], data['round_to'])
    elif 'B/s' in data:
        metric = NetworkMetric.from_bytes(data['B/s'], data['round_to'])
    else:
        raise_generic_json_error()
    return web.json_response(metric.to_json())

async def get_all_ports(request):
    data = {'hello': 'world'}
    return web.json_response(data)

async def get_ports(request):
    data = await request.json()

    if 'protocol' not in data and 'port' not in data:
        raise_generic_json_error()

    port = Port(data['port'], data['protocol'])
    return web.json_response(port.to_json())
