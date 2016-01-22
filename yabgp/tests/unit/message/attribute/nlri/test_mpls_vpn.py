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

""" Test MPLS VPN """

import unittest

from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN


class TestMPLSVPN(unittest.TestCase):

    def test_parse_mpls_label_stack(self):
        label_bin = b'\x00\x01\x41'
        self.assertEqual([20], MPLSVPN.parse_mpls_label_stack(label_bin))
        label_bin = b'\x00\x01\x10\x00\x01\x31'
        self.assertEqual([17, 19], MPLSVPN.parse_mpls_label_stack(label_bin))
        label_bin = b'\x80\x00\x00'
        self.assertEqual([524288], MPLSVPN.parse_mpls_label_stack(label_bin))

    def test_construct_mpls_label_stack(self):
        label_bin = b'\x00\x01\x41'
        self.assertEqual(label_bin, MPLSVPN.construct_mpls_label_stack(labels=[20]))

    def test_parse_and_construct_rd_type0(self):
        # for rd type 0
        rd_bin = b'\x00\x00\xfd\xea\x00\x00\x00\x01'
        rd_parsed = '65002:1'
        self.assertEqual(rd_parsed, MPLSVPN.parse_rd(rd_bin))
        self.assertEqual(rd_bin, MPLSVPN.construct_rd(rd_parsed))

    def test_parse_and_construct_rd_type1(self):

        rd_bin = b'\x00\x01\xac\x11\x00\x03\x00\x02'
        rd_parsed = '172.17.0.3:2'
        self.assertEqual(rd_parsed, MPLSVPN.parse_rd(rd_bin))
        self.assertEqual(rd_bin, MPLSVPN.construct_rd(rd_parsed))

    def test_parse_and_construct_rd_type2(self):
        rd_bin = b'\x00\x02\x00\x01\x00\x00\x00\x02'
        rd_parsed = '65536:2'
        self.assertEqual(rd_parsed, MPLSVPN.parse_rd(rd_bin))
        self.assertEqual(rd_bin, MPLSVPN.construct_rd(rd_parsed))

if __name__ == '__main__':
    unittest.main()
