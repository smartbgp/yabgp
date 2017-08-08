#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from oslo_config import cfg

from yabgp.agent import prepare_service
from yabgp.handler import BaseHandler
# from yabgp.common import constants as bgp_cons


CONF = cfg.CONF


class CliHandler(BaseHandler):
    def __init__(self):
        super(CliHandler, self).__init__()

    def on_update_error(self, peer, timestamp, msg):
        print('[-] UPDATE ERROR,', msg)

    def route_refresh_received(self, peer, msg, msg_type):
        print('[+] ROUTE_REFRESH received,', msg)

    def keepalive_received(self, peer, timestamp):
        print('[+] KEEPALIVE received')

    def open_received(self, peer, timestamp, result):
        print('[+] OPEN received,', result)

    def update_received(self, peer, timestamp, msg):
        print('[+] UPDATE received,', msg)

    def notification_received(self, peer, msg):
        print('[-] NOTIFICATION received,', msg)


def main():
    try:
        cli_handler = CliHandler()
        prepare_service(handler=cli_handler)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    sys.exit(main())
