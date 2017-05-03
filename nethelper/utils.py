"""
utils.py
~~~~~~~~

Contains various utilities to support the models and application debugging
"""


def fetch_mac_address_vendor_file(
        url='http://standards.ieee.org/develop/regauth/oui/oui.txt'):
    # TODO: Fetch the file online
    # TODO: Move 'Well-known addresses' section to seperate file
    # TODO: Remove any empty lines from file
    # TODO: Remove any line starting with a #
    pass


def fetch_iana_port_list(
        url=(
            'https://www.iana.org/assignments/'
            'service-names-port-numbers/service-names-port-numbers.csv'
        )):
    """Retrieves and cleans up the official IANA port list

    :param url: URL to the IANA port list in csv format
    """
    # TODO: Create new lines for port ranges notated like for instance 225-241
    pass
