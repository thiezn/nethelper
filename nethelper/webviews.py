"""
views.py
~~~~~~~~

Holds all the REST API views
"""

from aiohttp import web
import aiohttp_jinja2
from .models import IPv4Network, Port, MacAddress, NetworkMetric, DnsRecord


@aiohttp_jinja2.template('query.html')
async def query_page(request):
    """Serving the main webpage querying networks, mac's and ports"""

    # Retrieve client connection details
    peername = request.transport.get_extra_info('peername')
    try:
        client_ip, client_port = peername
    except:
        client_ip, client_port = None, None

    if client_ip == '127.0.0.1':
        if 'X-Real-IP' in request.headers:
            client_ip = request.headers['X-Real-IP']

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
            # Didn't receive a proper network
            # TODO: make sure to log the exceptions as it might also be a
            # problem in the models.py implementation
            pass
    except KeyError:
        pass

    # Parse DNS query
    try:
        data['dns'] = await DnsRecord.load_from_query(
            request.query['dns'], request.query['dnstype']
        )
    except KeyError:
        pass

    # Parse port query
    try:
        try:
            data['port'] = Port(int(request.query['port']), 'tcp')
        except ValueError:
            # Didn't receive a valid ip OR its because the port list isn't
            # sanitised yet (e.g. some fields have port ranges like 225-241
            # TODO: make sure to log the exceptions as it might also be a
            # problem in the models.py implementation
            pass
    except KeyError:
        pass

    # Parse mac query
    try:
        try:
            data['mac'] = MacAddress(request.query['mac'])
        except ValueError:
            # Didn't receive a valid mac
            # TODO: make sure to log the exceptions as it might also be a
            # problem in the models.py implementation
            pass
    except KeyError:
        pass

    try:
        try:
            if request.query['metricunit'] == 'bps':
                data['metric'] = NetworkMetric.from_bits(
                    int(request.query['metric']), round_to=2
                )
            elif request.query['metricunit'] == 'kbps':
                data['metric'] = NetworkMetric.from_kilobits(
                    int(request.query['metric']), round_to=2
                )
            elif request.query['metricunit'] == 'Mbps':
                data['metric'] = NetworkMetric.from_megabits(
                    int(request.query['metric']), round_to=2
                )
            elif request.query['metricunit'] == 'Gbps':
                data['metric'] = NetworkMetric.from_gigabits(
                    int(request.query['metric']), round_to=2
                )
        except ValueError:
            # TODO: make sure to log the exceptions as it might also be a
            # problem in the models.py implementation
            pass
    except KeyError:
        pass

    return data


@aiohttp_jinja2.template('api.html')
async def api_page(request):
    return {'api_page_active': True}


@aiohttp_jinja2.template('whoarewe.html')
async def whoarewe_page(request):
    return {'whoarewe_page_active': True}
