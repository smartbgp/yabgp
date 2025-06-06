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

""" Test IPv6 Unicast """

import unittest

from yabgp.message.attribute.nlri.ipv6_unicast import IPv6Unicast


class TestIPv6Unicast(unittest.TestCase):
    def test_parse(self):
        nlri_data = b'\x80\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x40\x20\x01\x32' \
                    b'\x32\x00\x01\x00\x00\x7f\x20\x01\x48\x37\x16\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        value_parsed = IPv6Unicast().parse(nlri_data)
        value_hoped = ['2001:3232::1/128', '2001:3232:1::/64', '2001:4837:1632::2/127']
        self.assertEqual(value_hoped, value_parsed)

    def test_parse_2(self):
        nlri_data = b'\x70\x32\x6c\xce\x92\x25\xea\x36\x5e\x4d\x71\x59\x45\x22\x00\x00\x00'
        value_parsed = IPv6Unicast().parse(nlri_data)
        value_hoped = ['326c:ce92:25ea:365e:4d71:5945:2200:0/112']
        self.assertEqual(value_hoped, value_parsed)

    def test_parse_3(self):
        nlri_data = b'\x00\x00\x03\xe9\x40\x20\x01\x0d\xb8\x00\x00\x00\x00'
        value_parsed = IPv6Unicast().parse(nlri_data, addpath=True)
        value_hoped = [{'path_id': 1001, 'prefix': '2001:db8::/64'}]
        self.assertEqual(value_hoped, value_parsed)

    def test_parse_withdraw(self):
        nlri_data = b'\x40\x20\x01\x0d\xb8\x00\x01\x00\x02\x40\x20\x01\x0d\xb8\x00\x01\x00\x01\x40\x20\x01\x0d' \
                    b'\xb8\x00\x01\x00\x00'
        value_parsed = IPv6Unicast.parse(nlri_data)
        value_hoped = ['2001:db8:1:2::/64', '2001:db8:1:1::/64', '2001:db8:1::/64']
        self.assertEqual(value_hoped, value_parsed)

    def test_construct_nlri(self):
        nlri_list = ['2001:db8:1:2::/64', '2001:db8:1:1::/64', '2001:db8:1:3::/64']
        value_hex = IPv6Unicast.construct(nlri_list)
        value_hoped = b'\x40\x20\x01\x0D\xB8\x00\x01\x00\x02\x40\x20\x01\x0D\xB8\x00\x01\x00\x01' \
                      b'\x40\x20\x01\x0D\xB8\x00\x01\x00\x03'
        self.assertEqual(value_hoped, value_hex)

    def test_construct_nlri_2(self):
        nlri_list = ['2001:3232::1/128', '2001:3232:1::/64', '2001:4837:1632::2/127']
        value_hex = IPv6Unicast.construct(nlri_list)
        value_hoped = b'\x80\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x40\x20\x01\x32' \
                      b'\x32\x00\x01\x00\x00\x7f\x20\x01\x48\x37\x16\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        self.assertEqual(value_hoped, value_hex)

    def test_construct_nlri_3(self):
        nlri_list = ['326c:ce92:25ea:365e:4d71:5945:2200:0/112']
        value_hex = IPv6Unicast.construct(nlri_list)
        value_hoped = b'\x70\x32\x6c\xce\x92\x25\xea\x36\x5e\x4d\x71\x59\x45\x22\x00'
        self.assertEqual(value_hoped, value_hex)


if __name__ == '__main__':
    unittest.main()
