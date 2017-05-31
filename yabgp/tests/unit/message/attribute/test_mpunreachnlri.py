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

""" Unittest for MPUnReach NLRI"""

import unittest
from yabgp.message.attribute.mpunreachnlri import MpUnReachNLRI


class TestMpUnReachNLRI(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_ipv4_mpls_vpn_parse(self):
        data_bin = b'\x80\x0f\x12\x00\x01\x80\x70\x80\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\xc0\xa8\xc9'
        data_hoped = {'afi_safi': (1, 128),
                      'withdraw': [{'label': [524288],
                                    'rd': '2:2',
                                    'prefix': '192.168.201.0/24'}]}
        self.assertEqual(data_hoped, MpUnReachNLRI.parse(data_bin[3:]))

    def test_ipv4_mpls_vpn_construct(self):
        data_bin = b'\x80\x0f\x12\x00\x01\x80\x70\x80\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\xc0\xa8\xc9'
        data_hoped = {'afi_safi': (1, 128),
                      'withdraw': [{'rd': '2:2',
                                    'prefix': '192.168.201.0/24'}]}
        self.assertEqual(data_bin, MpUnReachNLRI.construct(data_hoped))

    def test_ipv6_unicast_parse(self):
        data_bin = b"\x00\x02\x01\x80\x20\x01\x48\x37\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20"
        data_hoped = {'afi_safi': (2, 1), 'withdraw': ['2001:4837::20/128']}
        self.assertEqual(data_hoped, MpUnReachNLRI.parse(data_bin))

    def test_ipv6_unicast_construct(self):
        nlri_dict = {
            'afi_safi': (2, 1),
            'withdraw': ['2001:3232::1/128', '::2001:3232:1:0/64', '2001:4837:1632::2/127']}
        self.assertEqual(nlri_dict, MpUnReachNLRI.parse(MpUnReachNLRI.construct(nlri_dict)[3:]))

    def test_ipv6_mpls_vpn_parse_construct(self):
        data_dict = {
            'afi_safi': (2, 128),
            'withdraw': [
                {'label': [524288], 'rd': '100:10', 'prefix': '2001:3232::1/128'},
                {'label': [524288], 'rd': '100:11', 'prefix': '2001:4837:1632::2/127'}
            ]
        }
        self.assertEqual(
            data_dict,
            MpUnReachNLRI.parse(
                value=MpUnReachNLRI.construct(value=data_dict)[3:]
            ))

    def test_ipv4_flowspec_parse(self):
        data_bin = b'\x00\x01\x85\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        nlri_dict = {'afi_safi': (1, 133), 'withdraw': [{1: '192.85.2.0/24', 2: '192.85.1.0/24'}]}
        self.assertEqual(nlri_dict, MpUnReachNLRI.parse(data_bin))

    def test_ipv4_flowspec_construct(self):
        data_bin = b'\x00\x01\x85\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        nlri_dict = {'afi_safi': (1, 133), 'withdraw': [{1: '192.85.2.0/24', 2: '192.85.1.0/24'}]}
        self.assertEqual(data_bin, MpUnReachNLRI.construct(nlri_dict)[3:])

    def test_l2vpn_evpn_route_type_1_parse_construct(self):
        data_dict = {
            "afi_safi": (25, 70),
            "withdraw": [{
                "type": 1,
                "value": {
                    "rd": "1.1.1.1:32867",
                    "esi": 0,
                    "eth_tag_id": 100,
                    "label": [10]
                }
            }]}
        self.assertEqual(data_dict, MpUnReachNLRI.parse(MpUnReachNLRI.construct(data_dict)[3:]))

    def test_l2vpn_evpn_route_type_2_parse_construct(self):
        data_dict = {
            'afi_safi': (25, 70),
            'withdraw': [
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
        self.assertEqual(data_dict, MpUnReachNLRI.parse(MpUnReachNLRI.construct(data_dict)[3:]))

    def test_l2vpn_evpn_route_type_3_parse_construct(self):
        data_dict = {
            "afi_safi": (25, 70),
            "withdraw": [
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
        self.assertEqual(data_dict, MpUnReachNLRI.parse(MpUnReachNLRI.construct(data_dict)[3:]))

    def test_l2vpn_evpn_route_type_4_parse_construct(self):
        data_dict = {
            "afi_safi": (25, 70),
            "withdraw": [
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
        self.assertEqual(data_dict, MpUnReachNLRI.parse(MpUnReachNLRI.construct(data_dict)[3:]))


if __name__ == '__main__':
    unittest.main()
