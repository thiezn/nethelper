#!/usr/bin/env python3

from nethelper import NetHelper
import os


def main():
    path = os.path.dirname(os.path.realpath(__file__))

    web_daemon = NetHelper.load_from_config('{}/config/server.json'.format(path))
    web_daemon.start()


if __name__ == '__main__':
    main()
