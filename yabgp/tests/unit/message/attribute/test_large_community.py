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

""" Test Community attribute """

import unittest

from yabgp.message.attribute.largecommunity import LargeCommunity


class TestLargeCommunity(unittest.TestCase):

    def test_parse(self):

        community = LargeCommunity.parse(value=b'\x00\x03\x00\x0d\x00\x00\x00\x03\x00\x00\x00\x05')
        self.assertEqual(["196621:3:5"], community)

    def test_construct(self):

        large_community = LargeCommunity.construct(value=['196621:3:5', '196621:4:1'])
        self.assertEqual(b'\xe0\x20\x18'
                         b'\x00\x03\x00\x0d\x00\x00\x00\x03\x00\x00\x00\x05'
                         b'\x00\x03\x00\x0d\x00\x00\x00\x04\x00\x00\x00\x01', large_community)


if __name__ == '__main__':
    unittest.main()
