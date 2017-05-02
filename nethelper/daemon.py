"""
nethelper API
~~~~~~~~~~~~~

REST API to retrieve ip and mac address details.

There are a lot of websites and tools out there for this with various level of maturity.
The main goal of this API is to create the end all API for network administrators and
rule the world.
"""

# Try to import uvloop if available
# TODO: check if aiohttp is not slow anymore due to the parser, see url:
#       https://magic.io/blog/uvloop-blazing-fast-python-networking/
try:
    import uvloop
    import asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

import json
from aiohttp import web
import aiohttp_jinja2
import jinja2
from .routes import setup_api_routes, setup_web_routes


class NetHelperApi:
    """Class representing the nethelper REST API HTTP Daemon"""

    def __init__(self, host, port):
        """Initialise the nethelper REST API

        :param host (string): host/ip to listen on
        :param port (int): port number to listen on
        """
        self.host = host
        self.port = port

    @classmethod
    def load_from_config(cls, filename):
        """Initialises a :class:`NetHelperApi` instance from configuration file

        :param filename: the JSON configuration filename
        """
        with open(filename, 'r') as f:
            config = json.load(f)[0]

        return cls(
            config['host'],
            config['port']
        )

    def start(self):
        """Starts the REST API"""
        self.app = web.Application()

        # Enable jinja2 templates
        aiohttp_jinja2.setup(
            self.app, loader=jinja2.PackageLoader('nethelper', 'templates')
        )

        # Register routes
        setup_api_routes(self.app)
        setup_web_routes(self.app)

        # Start web daemon
        web.run_app(self.app, host=self.host, port=self.port)
