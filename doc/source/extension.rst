Write Customized YABGP through Extension Handlers
==================================================

YABGP is an extendable BGP probe which can be used to establish BGP session with all kinds of routers, and send/received BGP messages to/from them.
The decoded BGP messages with ``json`` format will be written in a file by default.
But through our ``handler mechanism``, you can writed your own bgpd process by implementation of your own handler.

What you only need to do in your own hander is to deside how to process all kinds of receveid BGP messages and BGP session connection situation.
The handler will inherit from ``BaseHandler`` and implement all methods of it. you can wirte your own code in each message process method
and do what to want to do with received messages like maintain RIB, insert into database, etc. If you want to add more configurable options,
please reference the ``DefaultHandler``.

.. code:: python

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    from __future__ import print_function
    import sys

    from yabgp.agent import prepare_service
    from yabgp.handler import BaseHandler


    class CliHandler(BaseHandler):
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
            prepare_service(handler=cli_handler)
        except Exception as e:
            print(e)


    if __name__ == '__main__':
        sys.exit(main())


How to run it? very simple! let's call this file as ``my_bgpd.py``, and you can run it just like ``yabgpd``

.. note::

    Please make sure you have install yabgp for requirements, you can do that through ``pip install yabgp``


.. code:: bash

    $ python my_bgpd.py  --bgp-local_as=100 --bgp-remote_addr=1.1.1.1 --bgp-remote_as=100 --bgp-afi_safi=ipv4,bgpls,flowspec