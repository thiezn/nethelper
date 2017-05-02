"""
models.py
~~~~~~~~~

Contains the various object models
"""

import ipaddress


class IPv4Network:
    """Class representing a IPv4 network address"""

    def __init__(self, ip_address, netmask=None, bitmask=None, strict=False):
        """Initialise :class:`Network` instance

        :param ip_address (string): IP address (e.g. 10.0.0.0 or 10.0.0.0/24)
        :param netmask: The IP netmask, only use when ip_address doesn't contain a mask
        :param bitmask: The IP bitmask, only use when ip_address doesn't contain a mask
        :param strict: Only allows valid class networks
        """
        # Verify init arguments
        if '/' in ip_address:
            network_query = ip_address
        elif netmask:
            network_query = '{}/{}'.format(ip_address, netmask)
        elif bitmask:
            network_query = '{}/{}'.format(ip_address, bitmask)
        else:
            raise ValueError('Invalid parameters: {} {} {}'.format(ip_address, netmask, bitmask))

        # Parse network
        try:
            result = ipaddress.ip_network(network_query, strict=strict)
        except ValueError as e:
            return {'error': str(e)}

        # Initialise properties
        self.network = str(result.network_address)
        self.broadcast = str(result.broadcast_address)
        self.is_private = result.is_private
        self.is_multicast = result.is_multicast
        self.netmask = result.with_netmask.split('/')[1]
        self.bitmask = result.with_prefixlen.split('/')[1]
        self.hostmask = result.with_hostmask.split('/')[1]
        self.num_addresses = result.num_addresses
        self.first_host = str(ipaddress.ip_address(int(result.network_address + 1)))
        self.last_host = str(ipaddress.ip_address(int(result.broadcast_address - 1)))

    def __repr__(self):
        return '<Network {}/{}>'.format(self.network, self.bitmask)

    def to_json(self):
        """Returns a JSON representation of the :class:`Network` object"""
        return {
            'network': self.network,
            'broadcast': self.broadcast,
            'is_private': self.is_private,
            'is_multicast': self.is_multicast,
            'netmask': self.netmask,
            'bitmask': self.bitmask,
            'hostmask': self.hostmask,
            'num_addresses': self.num_addresses,
            'first_host': self.first_host,
            'last_host': self.last_host
        }


class MacAddress:
    """Class representing a network MAC Address"""

    def __init__(self, mac_address, vendor_filename='mac_vendors.txt'):
        """ Tries to find the mac address vendor address """
        (
            self.mac_address_flat,
            self.mac_address,
            self.mac_address_dots,
            self.mac_address_dashes
        ) = self._parse_mac_notation(mac_address)

        # TODO: universal vs local mac:  https://en.wikipedia.org/wiki/MAC_address
        # self.is_unicast =
        # self.is_multicast =
        # self.is_universal =
        # self is_local =

        # TODO: set vendor_id to None and skip vendorfile check if self.is_local = True
        self.vendor_id = self.mac_address[:6]

        # Search for mac in mac vendor file
        # TODO: verify if this is correct and see if we can optimise
        # by doing less splitting
        self.vendors = []
        with open(vendor_filename, 'r') as f:
            for line in f:
                split_line = line.split()
                if self.vendor_id.startswith(split_line[0]):
                    self.vendors.append(line.split('# ')[1])

    def __repr__(self):
        return '<MacAddress {}>'.format(self.mac_address)

    def to_json(self):
        """Returns a json representation of the :class:`MacAddress` object"""
        return {
            'mac_address': self.mac_address,
            'mac_address_flat': self.mac_address_flat,
            'mac_address_dots': self.mac_address_dots,
            'mac_address_dashes': self.mac_address_dashes,
            'mac_address_binary': self.mac_address_binary,
            'vendor_id': self.vendor_id,
            'vendors': self.vendors,
            'is_unicast': self.is_unicast,
            'is_multicast': self.is_multicast,
            'is_universal': self.is_universal,
            'is_local': self.is_local
        }

    @staticmethod
    def parse_mac_notation(self, mac_address):
        """Parses a given mac address

        This function will try to find out the MAC address notation
        and returns a tuple of different well known notation flavours

        :param mac_address: MAC Address
        """
        mac_flat = mac_address.replace('.', '').replace(':', '').replace('-', '').upper()

        try:
            # TODO: Add bit notation of mac. 00001000110001 etc
            # The bit notation can then be used for determining unicast/multicast etc
            mac = '{}:{}:{}:{}:{}:{}'.format(
                mac_flat[:2],
                mac_flat[2:4],
                mac_flat[4:6],
                mac_flat[6:8],
                mac_flat[8:10],
                mac_flat[10:12]
            )
            mac_dots = '{}.{}.{}'.format(
                mac_flat[:4],
                mac_flat[4:8],
                mac_flat[8:12]
            )
            mac_dashes = '{}-{}-{}-{}-{}-{}'.format(
                mac_flat[:2],
                mac_flat[2:4],
                mac_flat[4:6],
                mac_flat[6:8],
                mac_flat[8:10],
                mac_flat[10:12]
            )

        except IndexError:
            raise ValueError('Invalid MAC address passed {}'.format(mac_address))

        return mac_flat, mac, mac_dots, mac_dashes


class NetworkMetric:
    """Class representing a network metric like Mbps or kBps"""

    def __init__(self, B_s, kB_s, MB_s, GB_s, bps, kbps, Mbps, Gbps, round_to=None):
        self.round_to = round_to

        self.B_s = B_s      # Bytes per second
        self.kB_s = kB_s    # kiloBytes per second
        self.MB_s = MB_s    # MegaBytes per second
        self.GB_s = GB_s    # GigaBytes per second

        self.bps = bps      # bits per second
        self.kbps = kbps    # Kilobits per second
        self.Mbps = Mbps    # Megabits per second
        self.Gbps = Gbps    # Gigabits per second

    def __repr__(self):
        # TODO: figure out a way to get the best representation
        if self.round_to is None:
            Mbps = self.Mbps
        else:
            Mbps = round(self.Mbps, self.round_to)

        return '<NetworkMetric {} Mbps>'.format(Mbps)

    def to_json(self):
        """Returns a json representation of the :class:`NetworkMetric` object"""
        if self.round_to is None:
            B_s = self.B_s
            kB_s = self.kB_s
            MB_s = self.MB_s
            GB_s = self.GB_s
            bps = self.bps
            kbps = self.kbps
            Mbps = self.Mbps
            Gbps = self.Gbps
        else:
            B_s = round(self.B_s, self.round_to)
            kB_s = round(self.kB_s, self.round_to)
            MB_s = round(self.MB_s, self.round_to)
            GB_s = round(self.GB_s, self.round_to)
            bps = round(self.bps, self.round_to)
            kbps = round(self.kbps, self.round_to)
            Mbps = round(self.Mbps, self.round_to)
            Gbps = round(self.Gbps, self.round_to)
        return {
            'bps': bps,
            'kbps': kbps,
            'Mbps': Mbps,
            'Gbps': Gbps,
            'B/s': B_s,
            'kB/s': kB_s,
            'MB/s': MB_s,
            'GB/s': GB_s,
        }

    @classmethod
    def from_bytes(cls, B_s, round_to=None):
        """Initialise :class:`NetworkMetric` from Bytes per second"""
        kB_s = B_s / 1024   # kiloBytes per second
        MB_s = kB_s / 1024  # MegaBytes per second
        GB_s = MB_s / 1024  # GigaBytes per second

        bps = B_s / 8       # bits per second
        kbps = kB_s / 8     # Kilobits per second
        Mbps = MB_s / 8     # Megabits per second
        Gbps = GB_s / 8     # Gigabits per second

        return cls(B_s, kB_s, MB_s, GB_s, bps, kbps, Mbps, Gbps, round_to)

    @classmethod
    def from_bits(cls, bps, round_to=None):
        """Initialise :class:`NetworkMetric` from bits per second"""
        B_s = bps * 8       # Bytes per second
        kB_s = B_s / 1024   # kiloBytes per second
        MB_s = kB_s / 1024  # MegaBytes per second
        GB_s = MB_s / 1024  # GigaBytes per second

        kbps = kB_s / 8     # Kilobits per second
        Mbps = MB_s / 8     # Megabits per second
        Gbps = GB_s / 8     # Gigabits per second

        return cls(B_s, kB_s, MB_s, GB_s, bps, kbps, Mbps, Gbps, round_to)

    @classmethod
    def from_kilobits(cls, kbps, round_to=None):
        """Initialise :class:`NetworkMetric` from kilobits per second"""
        B_s = kbps * 8 / 1024      # Bytes per second
        kB_s = B_s / 1024          # kiloBytes per second
        MB_s = kB_s / 1024         # MegaBytes per second
        GB_s = MB_s / 1024         # GigaBytes per second

        bps = kbps / 1024          # bits per second
        Mbps = MB_s / 8            # Megabits per second
        Gbps = GB_s / 8            # Gigabits per second

        return cls(B_s, kB_s, MB_s, GB_s, bps, kbps, Mbps, Gbps, round_to)
