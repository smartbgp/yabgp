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

""" Test BGP KeepAlive message"""

import unittest

from yabgp.message.keepalive import KeepAlive
from yabgp.common.exception import MessageHeaderError


class TestKeepAlive(unittest.TestCase):

    def test_parse(self):
        msg_hex = ''
        keepalive_msg = KeepAlive().parse(msg_hex)
        self.assertEqual(None, keepalive_msg)

    def test_parse_msg_header_error(self):
        self.assertRaises(MessageHeaderError, KeepAlive().parse, b'\x00')

    def test_construct(self):

        msg_hex = KeepAlive().construct()
        hope_msg = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04'
        self.assertEqual(hope_msg, msg_hex)

if __name__ == '__main__':
    unittest.main()
