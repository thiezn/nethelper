#!/usr/bin/env python3

from nethelper import NetHelperApi


def main():
    web_daemon = NetHelperApi.load_from_config('config/server.json')
    web_daemon.start()


if __name__ == '__main__':
    main()
