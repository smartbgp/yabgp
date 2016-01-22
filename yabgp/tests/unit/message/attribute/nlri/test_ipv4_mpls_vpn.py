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

""" Test IPv4 MPLS VPN NLRI """

import unittest

from yabgp.message.attribute.nlri.ipv4_mpls_vpn import IPv4MPLSVPN


class TestIPv4MPLSVPN(unittest.TestCase):

    def test_parse(self):
        nlri_hex = b'\x78\x00\x01\x91\x00\x00\x00\x64\x00\x00\x00\x64\xaa\x00\x00\x00'
        self.assertEqual(
            [{'label': [25], 'rd': '100:100', 'prefix': '170.0.0.0/32'}], IPv4MPLSVPN.parse(nlri_hex))

    def test_construct_1(self):
        nlri_hex = b'\x76\x00\x01\x41\x00\x00\xfd\xea\x00\x00\x00\x01\x17\x00\x00\x00'
        nlri_list = [{'label': [20], 'rd': '65002:1', 'prefix': '23.0.0.0/30'}]
        self.assertEqual(nlri_list, IPv4MPLSVPN.parse(nlri_hex))
        self.assertEqual(nlri_hex, IPv4MPLSVPN.construct(nlri_list), )

    def test_construct_2(self):
        nlri_hex = b'\x78\x00\x01\x91\x00\x00\x00\x64\x00\x00\x00\x64\xaa\x00\x00\x00'
        nlri_list = [{'label': [25], 'rd': '100:100', 'prefix': '170.0.0.0/32'}]
        self.assertEqual(nlri_hex, IPv4MPLSVPN.construct(nlri_list))

    def test_construct_multi(self):
        nlri_list = [
            {'label': [25], 'rd': '100:100', 'prefix': '170.0.0.0/32'},
            {'label': [20], 'rd': '65002:1', 'prefix': '23.0.0.0/30'}
        ]
        self.assertEqual(nlri_list, IPv4MPLSVPN.parse(IPv4MPLSVPN.construct(nlri_list)))

if __name__ == '__main__':
    unittest.main()
