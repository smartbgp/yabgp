# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

""" Test Open message"""

import unittest

import ipaddr

from yabgp.message.open import Open
from yabgp.common.constants import VERSION


class TestOpen(unittest.TestCase):

    def setUp(self):
        self.open = Open()

    def test_parse(self):
        msg_hex = '\x04\x5b\xa0\x00\xb4\x03\x03\x03\x09\x25\x02\x06\x01\x04\x00\x01\x00\x80' \
                  '\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00\x02\x02\x02\x00\x02\x03' \
                  '\x83\x01\x00\x02\x06\x41\x04\x00\x01\x04\x6a'
        open_msg = self.open.parse(msg_hex)
        results = {'bgpID': '3.3.3.9', 'Version': 4, 'holdTime': 180, 'ASN': 66666,
                   'Capabilities': {
                       'GracefulRestart': False,
                       'ciscoMultiSession': True,
                       'ciscoRouteRefresh': True,
                       '4byteAS': True,
                       'AFI_SAFI': [(1, 128), (1, 1)],
                       'routeRefresh': True}}
        self.assertEqual(results, open_msg)

    def test_construct(self):

        self.open.version = VERSION
        self.open.asn = 66666
        self.open.hold_time = 180
        self.open.bgp_id = int(ipaddr.IPv4Address('1.1.1.1'))
        my_capa = {
            'GracefulRestart': False,
            'ciscoMultiSession': True,
            'ciscoRouteRefresh': True,
            '4byteAS': True,
            'AFI_SAFI': [(1, 128), (1, 1)],
            'routeRefresh': True}
        msg_hex = self.open.construct(my_capa)
        hope_hex = '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00=\x01\x04[\xa0\x00\xb4\x01' \
                   '\x01\x01\x01 \x02\x06\x01\x04\x00\x01\x00\x80\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00' \
                   '\x02\x02\x02\x00\x02\x06A\x04\x00\x01\x04j'
        self.assertEqual(hope_hex, msg_hex)

if __name__ == '__main__':
    unittest.main()
