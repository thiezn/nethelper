#!/usr/bin/env python3

from nethelper import NetHelperApi
import os


def main():
    path = os.path.dirname(os.path.realpath(__file__))

    web_daemon = NetHelperApi.load_from_config('{}/config/server.json'.format(path))
    web_daemon.start()


if __name__ == '__main__':
    main()
