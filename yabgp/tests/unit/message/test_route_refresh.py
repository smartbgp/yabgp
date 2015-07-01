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

""" Test Route Refresh message"""

import unittest
from yabgp.message.route_refresh import RouteRefresh
from yabgp.common.constants import MSG_CISCOROUTEREFRESH
from yabgp.common.constants import MSG_ROUTEREFRESH


class TestRouteRefresh(unittest.TestCase):

    def test_parse(self):

        msg_hex = b'\x00\x01\x00\x80'
        msg_parsed = RouteRefresh().parse(msg_hex)
        msg_hoped = (1, 0, 128)
        self.assertEqual(msg_hoped, msg_parsed)

    def test_construct_rfc_route_refresh(self):

        msg = (1, 0, 128)
        msg_hex = RouteRefresh(afi=msg[0], res=msg[1], safi=msg[2]).construct(MSG_ROUTEREFRESH)
        msg_hoped = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x17\x05\x00\x01\x00\x80'
        self.assertEqual(msg_hoped, msg_hex)

    def test_construct_cisco_route_refresh(self):

        msg = (1, 0, 128)
        msg_hex = RouteRefresh(afi=msg[0], res=msg[1], safi=msg[2]).construct(MSG_CISCOROUTEREFRESH)
        msg_hoped = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x17\x80\x00\x01\x00\x80'
        self.assertEqual(msg_hoped, msg_hex)

if __name__ == '__main__':
    unittest.main()
