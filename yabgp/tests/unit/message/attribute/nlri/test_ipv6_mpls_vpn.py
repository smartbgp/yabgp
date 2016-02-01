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

""" Test IPv6 MPLS VPN NLRI """

import unittest

from yabgp.message.attribute.nlri.ipv6_mpls_vpn import IPv6MPLSVPN


class TestIPv6MPLSVPN(unittest.TestCase):

    def test_update_parse(self):
        nlri_hex = b'\x98\x00\x03\x61\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00\x04' \
                   b'\x98\x00\x03\x71\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        nlri_list = [
            {'label': [54], 'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
            {'label': [55], 'rd': '100:12', 'prefix': '2010:1:12::/64'}
        ]
        self.assertEqual(nlri_list, IPv6MPLSVPN.parse(value=nlri_hex))

    def test_update_construct(self):
        nlri_hex = b'\x98\x00\x03\x61\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00\x04' \
                   b'\x98\x00\x03\x71\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        nlri_list = [
            {'label': [54], 'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
            {'label': [55], 'rd': '100:12', 'prefix': '2010:1:12::/64'}
        ]
        self.assertEqual(nlri_hex, IPv6MPLSVPN.construct(value=nlri_list))

    def test_withdraw_parse(self):
        nlri_hex = b'\x98\x80\x00\x00\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00' \
                   b'\x04\x98\x80\x00\x00\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        nlri_list = [
            {'label': [524288], 'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
            {'label': [524288], 'rd': '100:12', 'prefix': '2010:1:12::/64'}
        ]
        self.assertEqual(nlri_list, IPv6MPLSVPN.parse(value=nlri_hex, iswithdraw=True))

    def test_withdraw_construct(self):
        nlri_hex = b'\x98\x80\x00\x00\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00' \
                   b'\x04\x98\x80\x00\x00\x00\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        nlri_list = [
            {'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
            {'rd': '100:12', 'prefix': '2010:1:12::/64'}
        ]
        self.assertEqual(nlri_hex, IPv6MPLSVPN.construct(value=nlri_list, iswithdraw=True))


if __name__ == '__main__':
    unittest.main()
