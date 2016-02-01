# Copyright 2016 Cisco Systems, Inc.
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

import unittest

from yabgp.message.attribute.nlri import NLRI


class TestNLRI(unittest.TestCase):

    def test_construct_prefix_vpnv6(self):
        prefix_hex = b'\x20\x10\x00\x00\x00\x12\x00\04'
        prefix_str = '2010:0:12:4::/64'
        self.assertEqual(prefix_hex, NLRI.construct_prefix_v6(prefix_str))


if __name__ == '__main__':
    unittest.main()
