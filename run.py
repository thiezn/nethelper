#!/usr/bin/env python3

from nethelper import NetHelperApi


def main():
    api = NetHelperApi.load_from_config('config/server.json')
    api.start()


if __name__ == '__main__':
    main()
