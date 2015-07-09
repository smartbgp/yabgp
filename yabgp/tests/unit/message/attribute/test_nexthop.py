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

"""Test Nexthop attribute
"""

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.common.constants import ERR_MSG_UPDATE_INVALID_NEXTHOP
from yabgp.message.attribute.nexthop import NextHop


class TestNextHop(unittest.TestCase):

    def test_parse(self):

        next_hop = NextHop.parse(value=b'\x0a\x0a\x0a\x01')
        self.assertEqual(next_hop, '10.10.10.1')
        self.assertEqual(NextHop.parse(value=b'\x00\x00\x00\x00'), '0.0.0.0')
        self.assertEqual(NextHop.parse(value=b'\xff\xff\xff\xff'), '255.255.255.255')

    def test_parse_invalid_length(self):
        # invalid length
        self.assertRaises(UpdateMessageError, NextHop.parse,
                          b'\x0a\x0a\x0a\x01\x01')
        try:
            NextHop.parse(b'\x0a\x0a\x0a\x01\x01')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_construct(self):

        next_hop = NextHop.construct(value='10.10.10.1')
        self.assertEqual(next_hop, b'\x40\x03\x04\x0a\x0a\x0a\x01')
        self.assertEqual(NextHop.construct('0.0.0.0'), b'\x40\x03\x04\x00\x00\x00\x00')

    def test_construct_invalid_nexthop(self):
        # invalid next hop
        self.assertRaises(UpdateMessageError, NextHop.construct, '300.1.1')
        try:
            NextHop.construct(value='300.33.33.33')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_INVALID_NEXTHOP)

    def test_construct_with_flags(self):
        nexthop = NextHop.construct(value='10.10.10.10')
        self.assertEqual(nexthop, b'\x40\x03\x04\x0a\x0a\x0a\x0a')
if __name__ == '__main__':
    unittest.main()
