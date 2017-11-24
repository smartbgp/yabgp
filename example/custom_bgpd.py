#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from flask import Blueprint
import flask

from yabgp.agent import prepare_service
from yabgp.handler import BaseHandler


class APIHandler(object):

    blueprint = Blueprint('demo', __name__)
    url_prefix = '/v1'


@APIHandler.blueprint.route('/rib')
def root():
    """
    v1 api root. Get the api status.
    """
    intro = {
        'rib': []
    }
    return flask.jsonify(intro)


class CliHandler(BaseHandler):
    """demo handler implementation
    """

    def __init__(self):
        super(CliHandler, self).__init__()

    def init(self):
        pass

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

    def on_connection_lost(self, peer):
        print('[-] CONNECTION lost')

    def on_connection_failed(self, peer, msg):
        print('[-] CONNECTION failed,', msg)


def main():
    try:
        cli_handler = CliHandler()
        prepare_service(handler=cli_handler, api_hander=APIHandler())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    sys.exit(main())
