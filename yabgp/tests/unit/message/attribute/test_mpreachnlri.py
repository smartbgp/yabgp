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

""" Unittest for MPReach NLRI"""

import unittest
from yabgp.message.attribute.mpreachnlri import MpReachNLRI


class TestMpReachNLRI(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_ipv4_mpls_vpn_parse(self):
        data_bin = b'\x80\x0e\x21\x00\x01\x80\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02' \
                   b'\x00\x78\x00\x01\x91\x00\x00\x00\x64\x00\x00\x00\x64\xaa\x00\x00\x00'
        data_hoped = {'afi_safi': (1, 128),
                      'nexthop': {'rd': '0:0', 'str': '2.2.2.2'},
                      'nlri': [{'label': [25],
                                'rd': '100:100',
                                'prefix': '170.0.0.0/32'}]}
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin[3:]))

    def test_ipv4_mpsl_vpn_construct_nexthop(self):
        nexthop = {'rd': '0:0', 'str': '2.2.2.2'}
        nexthop_bin = b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02'
        self.assertEqual(nexthop_bin, MpReachNLRI.construct_mpls_vpn_nexthop(nexthop))

    def test_ipv6_mpls_vpn_construct_nexthop(self):
        nexthop = {'rd': '0:0', 'str': '::ffff:172.16.4.12'}
        nexthop_bin = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\xff\xff\xac\x10\x04\x0c'
        self.assertEqual(nexthop_bin, MpReachNLRI.construct_mpls_vpn_nexthop(nexthop))

    def test_ipv4_mpls_vpn_construct(self):
        data_bin = b'\x80\x0e\x21\x00\x01\x80\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02' \
                   b'\x00\x78\x00\x01\x91\x00\x00\x00\x64\x00\x00\x00\x64\xaa\x00\x00\x00'
        data_parsed = {'afi_safi': (1, 128),
                       'nexthop': {'rd': '0:0', 'str': '2.2.2.2'},
                       'nlri': [{'label': [25],
                                 'rd': '100:100',
                                 'prefix': '170.0.0.0/32'}]}
        self.assertEqual(data_bin, MpReachNLRI.construct(data_parsed))

    def test_ipv6_unicast(self):
        data_bin = b"\x00\x02\x01\x10\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x01\x00\x80\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01" \
                   b"\x40\x20\x01\x32\x32\x00\x01\x00\x00\x7f\x20\x01\x48\x37\x16\x32\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x02"
        data_hoped = {
            'afi_safi': (2, 1),
            'nexthop': '2001:3232::1',
            'nlri': ['2001:3232::1/128', '::2001:3232:1:0/64', '2001:4837:1632::2/127']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin))

    def test_ipv6_unicast_with_linklocal_nexthop(self):
        data_bin = b"\x00\x02\x01\x20\x20\x01\x0d\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x02\xfe\x80\x00\x00\x00\x00\x00\x00\xc0\x02\x0b\xff\xfe\x7e\x00\x00\x00\x40" \
                   b"\x20\x01\x0d\xb8\x00\x02\x00\x02\x40\x20\x01\x0d\xb8\x00\x02\x00\x01\x40\x20" \
                   b"\x01\x0d\xb8\x00\x02\x00\x00"
        data_hoped = {
            'afi_safi': (2, 1),
            'linklocal_nexthop': 'fe80::c002:bff:fe7e:0',
            'nexthop': '2001:db8::2',
            'nlri': ['::2001:db8:2:2/64', '::2001:db8:2:1/64', '::2001:db8:2:0/64']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin))

    def test_ipv6_unicast_construct(self):
        data_parsed = {
            'afi_safi': (2, 1),
            'nexthop': '2001:3232::1',
            'nlri': ['2001:3232::1/128', '::2001:3232:1:0/64', '2001:4837:1632::2/127']}
        self.assertEqual(data_parsed, MpReachNLRI.parse(MpReachNLRI.construct(data_parsed)[3:]))

    def test_ipv6_unicast_with_locallink_nexthop_construct(self):
        data_hoped = {
            'afi_safi': (2, 1),
            'linklocal_nexthop': 'fe80::c002:bff:fe7e:0',
            'nexthop': '2001:db8::2',
            'nlri': ['::2001:db8:2:2/64', '::2001:db8:2:1/64', '::2001:db8:2:0/64']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(MpReachNLRI.construct(data_hoped)[3:]))

    def test_ipv6_mpls_vpn_parse(self):
        data_bin = b'\x80\x0e\x45\x00\x02\x80\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\xff\xff\xac\x10\x04\x0c\x00\x98\x00\x03\x61\x00\x00' \
                   b'\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00\x04\x98\x00\x03\x71\x00' \
                   b'\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        data_hoped = {
            'afi_safi': (2, 128),
            'nexthop': {'rd': '0:0', 'str': '::ffff:172.16.4.12'},
            'nlri': [
                {'label': [54], 'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
                {'label': [55], 'rd': '100:12', 'prefix': '2010:1:12::/64'}
            ]
        }
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin[3:]))

    def test_ipv6_mpls_vpn_construct(self):
        data_bin = b'\x80\x0e\x45\x00\x02\x80\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\xff\xff\xac\x10\x04\x0c\x00\x98\x00\x03\x61\x00\x00' \
                   b'\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x00\x00\x12\x00\x04\x98\x00\x03\x71\x00' \
                   b'\x00\x00\x64\x00\x00\x00\x0c\x20\x10\x00\x01\x00\x12\x00\x00'
        data_hoped = {
            'afi_safi': (2, 128),
            'nexthop': {'rd': '0:0', 'str': '::ffff:172.16.4.12'},
            'nlri': [
                {'label': [54], 'rd': '100:12', 'prefix': '2010:0:12:4::/64'},
                {'label': [55], 'rd': '100:12', 'prefix': '2010:1:12::/64'}
            ]
        }
        self.assertEqual(data_bin, MpReachNLRI.construct(data_hoped))

    def test_ipv4_flowspec_parse_multi_nlri_with_nexthop(self):
        data_bin = b'\x0e\x00\x1b\x00\x01\x85\x00\x00\x0a\x01\x18\xc0\x58\x03\x02\x18\xc0\x59\x03\x0a' \
                   b'\x01\x18\xc0\x58\x04\x02\x18\xc0\x59\x04'
        data_dict = {
            'afi_safi': (1, 133),
            'nexthop': '',
            'nlri': [
                {1: '192.88.3.0/24', 2: '192.89.3.0/24'},
                {1: '192.88.4.0/24', 2: '192.89.4.0/24'}
            ]}
        self.assertEqual(data_dict, MpReachNLRI.parse(data_bin[3:]))

    def test_ipv4_flowspec_construct(self):
        data_bin = b'\x80\x0e\x10\x00\x01\x85\x00\x00\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        data_dict = {'afi_safi': (1, 133), 'nexthop': '', 'nlri': [{1: '192.85.2.0/24', 2: '192.85.1.0/24'}]}
        self.assertEqual(data_bin, MpReachNLRI.construct(data_dict))

    def test_ipv4_flowspec_construct_multi_nlri(self):
        data_dict = {
            'afi_safi': (1, 133),
            'nexthop': '',
            'nlri': [
                {1: '192.88.3.0/24', 2: '192.89.3.0/24'},
                {1: '192.88.4.0/24', 2: '192.89.4.0/24'}
            ]}
        data_bin_cons = MpReachNLRI.construct(data_dict)
        self.assertEqual(data_dict, MpReachNLRI.parse(data_bin_cons[3:]))

    def test_l2vpn_evpn_parse_construct_route_type1(self):
        data_dict = {
            "afi_safi": (25, 70),
            "nexthop": "10.75.44.254",
            "nlri": [{
                "type": 1,
                "value": {
                    "rd": "1.1.1.1:32867",
                    "esi": 0,
                    "eth_tag_id": 100,
                    "label": [10]
                }
            }]
        }
        self.assertEqual(data_dict, MpReachNLRI.parse(MpReachNLRI.construct(data_dict)[3:]))

    def test_l2vpn_evpn_parse_route_type2(self):
        data_bin = b'\x80\x0e\x30\x00\x19\x46\x04\xac\x11\x00\x03\x00\x02\x25\x00\x01\xac\x11' \
                   b'\x00\x03\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c' \
                   b'\x30\x00\x11\x22\x33\x44\x55\x20\x0b\x0b\x0b\x01\x00\x00\x01'
        data_dict = {
            'afi_safi': (25, 70),
            'nexthop': '172.17.0.3',
            'nlri': [
                {
                    'type': 2,
                    'value': {
                        'eth_tag_id': 108,
                        'ip': '11.11.11.1',
                        'label': [0],
                        'rd': '172.17.0.3:2',
                        'mac': '00-11-22-33-44-55',
                        'esi': 0}}]
        }

        self.assertEqual(data_dict, MpReachNLRI.parse(data_bin[3:]))

    def test_l2vpn_evpn_construct_route_type2(self):
        data_bin = b'\x80\x0e\x30\x00\x19\x46\x04\xac\x11\x00\x03\x00\x02\x25\x00\x01\xac\x11' \
                   b'\x00\x03\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c' \
                   b'\x30\x00\x11\x22\x33\x44\x55\x20\x0b\x0b\x0b\x01\x00\x00\x00'
        data_dict = {
            'afi_safi': (25, 70),
            'nexthop': '172.17.0.3',
            'nlri': [
                {
                    'type': 2,
                    'value': {
                        'eth_tag_id': 108,
                        'ip': '11.11.11.1',
                        'label': [0],
                        'rd': '172.17.0.3:2',
                        'mac': '00-11-22-33-44-55',
                        'esi': 0}}]
        }

        self.assertEqual(data_bin, MpReachNLRI.construct(data_dict))

    def test_l2vpn_evpn_parse_construct_route_type3(self):
        data_dict = {
            "afi_safi": (25, 70),
            "nexthop": "10.75.44.254",
            "nlri": [
                {
                    "type": 3,
                    "value": {
                        "rd": "172.16.0.1:5904",
                        "eth_tag_id": 100,
                        "ip": "192.168.0.1"
                    }
                }
            ]
        }
        self.assertEqual(data_dict, MpReachNLRI.parse(MpReachNLRI.construct(data_dict)[3:]))

    def test_l2vpn_evpn_parse_construct_route_type4(self):
        data_dict = {
            "afi_safi": (25, 70),
            "nexthop": "10.75.44.254",
            "nlri": [
                {
                    "type": 4,
                    "value": {
                        "rd": "172.16.0.1:8888",
                        "esi": 0,
                        "ip": "192.168.0.1"
                    }
                }
            ]
        }
        self.assertEqual(data_dict, MpReachNLRI.parse(MpReachNLRI.construct(data_dict)[3:]))


if __name__ == '__main__':
    unittest.main()
