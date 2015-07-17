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
            [{'label': (25, 1), 'rd': '100:100', 'rd_type': 0, 'str': '170.0.0.0/32'}], IPv4MPLSVPN.parse(nlri_hex))

if __name__ == '__main__':
    unittest.main()
