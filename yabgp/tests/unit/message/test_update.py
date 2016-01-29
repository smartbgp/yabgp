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

""" Test Update message"""

import unittest
from yabgp.common.constants import HDR_LEN
from yabgp.message.update import Update
from yabgp.common.exception import UpdateMessageError


class TestUpdate(unittest.TestCase):
    def test_parse_prefix_list(self):
        prefix_hex = b'\x13\xb8\x9d\xe0\x18E\xb3\xdd\x18E\xb3\xdc\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        nlri = ['184.157.224.0/19', '69.179.221.0/24', '69.179.220.0/24',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        self.assertEqual(nlri, Update.parse_prefix_list(prefix_hex))

    def test_parse_prefix_list_with_addpath(self):
        prefix_hex = b'\x00\x00\x00\x01\x20\x05\x05\x05\x05\x00\x00\x00\x01\x20\xc0\xa8\x01\x05'
        nlri = [
            {'prefix': '5.5.5.5/32', 'path_id': 1},
            {'prefix': '192.168.1.5/32', 'path_id': 1}
        ]
        self.assertEqual(nlri, Update.parse_prefix_list(prefix_hex, True))

    def test_parse_prefix_mask_larger_than_32(self):
        prefix_hex = b'\x21\xb8\x9d\xe0\x18E\xb3\xdd\x18E\xb3\xdc\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        self.assertRaises(UpdateMessageError, Update.parse_prefix_list, prefix_hex)

    def test_construct_prefix_v4(self):
        nlri = ['184.157.224.1/32', '32.65.243.12/30', '89.232.254.0/23', '69.179.221.0/24',
                '61.172.0.0/16', '202.223.128.0/17', '156.152.0.0/15', '15.0.0.0/8',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        nlri_hex = Update.construct_prefix_v4(nlri)
        self.assertEqual(nlri, Update.parse_prefix_list(nlri_hex))

    def test_construct_prefix_v4_addpath(self):
        nlri = [{'path_id': 1, 'prefix': '99.99.99.99/32'}]
        nlri_hex = Update.construct_prefix_v4(nlri, add_path=True)
        self.assertEqual(b'\x00\x00\x00\x01\x20\x63\x63\x63\x63', nlri_hex)

    def test_parse_attributes_ipv4(self):
        attr_hex = b'@\x01\x01\x00@\x02\x08\x02\x03\x00\x01\x00\x02\x00\x03@\x03\x04\xac\x10\x01\x0e\x80\x04\x04' \
                   b'\x00\x00\x00\x00@\x05\x04\x00\x00\x00d\x80\t\x04\xac\x10\x01\x0e\x80\n\x08\x02\x02\x02\x02dddd'
        attributes = {1: 0,
                      2: [(2, [1, 2, 3])],
                      3: '172.16.1.14',
                      4: 0,
                      5: 100,
                      9: '172.16.1.14',
                      10: ['2.2.2.2', '100.100.100.100']}
        self.assertEqual(attributes, Update.parse_attributes(attr_hex, False))
        self.assertRaises(UpdateMessageError, Update.parse_attributes, attr_hex, True)

    def test_construct_attributes_ipv4(self):
        attr = {
            1: 2,
            2: [(2, [701, 71])],
            3: '219.158.1.204',
            5: 100,
            6: b'',
            7: (71, '16.96.243.103'),
            8: ['4837:701', '4837:2100'],
            9: '219.158.1.204',
            10: ['219.158.1.209', '0.0.0.30']}
        attr_hex = Update.construct_attributes(attr, asn4=True)
        self.assertEqual(attr, Update.parse_attributes(attr_hex, asn4=True))

    def test_parse_and_construct_ipv4_unicast_2byteas(self):
        # 2 bytes asn
        msg_hex = b'\x00\x00\x00\x28\x40\x01\x01\x02\x40\x02\x0a\x02\x01\x00\x1e\x01\x02\x00\x0a\x00\x14\x40\x03\x04' \
                  b'\x0a\x00\x00\x09\x80\x04\x04\x00\x00\x00\x00\xc0\x07\x06\x00\x1e\x0a\x00\x00\x09\x15\xac\x10\x00'
        update = Update.parse(None, msg_hex)
        attributes = {1: 2, 2: [(2, [30]), (1, [10, 20])], 3: '10.0.0.9', 4: 0, 7: (30, '10.0.0.9')}
        self.assertEqual(attributes, update['attr'])
        self.assertEqual([], update['withdraw'])
        self.assertEqual(['172.16.0.0/21'], update['nlri'])
        self.assertEqual(msg_hex, Update.construct(msg_dict=update, asn4=False)[HDR_LEN:])

    def test_parse_ipv4_4byteas(self):
        # 4 bytes asn
        msg_hex = b'\x00\x00\x00\x30\x40\x01\x01\x02\x40\x02\x10\x02\x01\x00\x00\x00\x1e\x01\x02\x00\x00\x00\x0a\x00' \
                  b'\x00\x00\x14\x40\x03\x04\x0a\x00\x00\x09\x80\x04\x04\x00\x00\x00\x00\xc0\x07\x08\x00\x00\x00' \
                  b'\x1e\x0a\x00\x00\x09\x15\xac\x10\x00'
        update = Update.parse(None, msg_hex, True)
        attributes = {1: 2, 2: [(2, [30]), (1, [10, 20])], 3: '10.0.0.9', 4: 0, 7: (30, '10.0.0.9')}
        self.assertEqual(attributes, update['attr'])
        self.assertEqual([], update['withdraw'])
        self.assertEqual(['172.16.0.0/21'], update['nlri'])

    def test_parse_ipv4_addpath_update(self):
        msg_hex = b'\x00\x00\x00\x30\x40\x01\x01\x00\x40\x02\x06\x02\x01\x00\x00\xfb\xff\x40\x03\x04\x0a\x00\x0e' \
                  b'\x01\x80\x04\x04\x00\x00\x00\x00\x40\x05\x04\x00\x00\x00\x64\x80\x0a\x04\x0a\x00\x22' \
                  b'\x04\x80\x09\x04\x0a\x00\x0f\x01\x00\x00\x00\x01\x20\x05\x05\x05\x05\x00\x00\x00\x01' \
                  b'\x20\xc0\xa8\x01\x05'
        update = Update.parse(None, msg_hex, True, True)
        attributes = {1: 0, 2: [(2, [64511])], 3: '10.0.14.1', 4: 0, 5: 100, 9: '10.0.15.1', 10: ['10.0.34.4']}
        self.assertEqual(attributes, update['attr'])
        self.assertEqual([], update['withdraw'])
        self.assertEqual([
            {'path_id': 1, 'prefix': '5.5.5.5/32'},
            {'path_id': 1, 'prefix': '192.168.1.5/32'}], update['nlri'])

    def test_parse_ipv4_addpath_withdraw(self):
        msg_hex = b'\x00\x09\x00\x00\x00\x01\x20\x63\x63\x63\x63\x00\x00'
        update = Update.parse(None, msg_hex, True, True)
        self.assertEqual([{'path_id': 1, 'prefix': '99.99.99.99/32'}], update['withdraw'])

    def test_parse_and_construct_ipv6_unicast_update(self):
        value_parse = {
            'attr': {
                1: 0,
                2: [(2, [65502])],
                4: 0,
                14: {
                    'afi_safi': (2, 1),
                    'linklocal_nexthop': 'fe80::c002:bff:fe7e:0',
                    'nexthop': '2001:db8::2',
                    'nlri': ['::2001:db8:2:2/64', '::2001:db8:2:1/64', '::2001:db8:2:0/64']}
            }}
        self.assertEqual(value_parse['attr'], Update.parse(
            None,
            Update.construct(
                msg_dict=value_parse,
                asn4=True)[HDR_LEN:], True)['attr'], True)

    def test_parse_and_construct_ipv4_mpls_vpn_update(self):
        data_bin = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00' \
                   b'\x74\x02\x00\x00\x00\x5d\x40\x01\x01\x02\x40\x02\x00\x80\x04\x04\x00' \
                   b'\x00\x00\x00\x40\x05\x04\x00\x00\x00\x64\xc0\x10\x08\x00\x02\x00\x02' \
                   b'\x00\x00\x00\x02\x80\x0a\x10\xc0\xa8\x01\x01\xc0\xa8\x01\x02\xc0\xa8' \
                   b'\x01\x03\xc0\xa8\x01\x04\x80\x09\x04\xc0\xa8\x01\x06\x80\x0e\x20\x00' \
                   b'\x01\x80\x0c\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xa8\x01\x06\x00\x70' \
                   b'\x00\x01\xd1\x00\x00\x00\x02\x00\x00\x00\x02\xc0\xa8\xc9'
        data_hoped = {
            'attr': {1: 2,
                     2: [],
                     4: 0,
                     5: 100,
                     9: '192.168.1.6',
                     10: ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
                     14: {'afi_safi': (1, 128),
                          'nexthop': {'rd': '0:0', 'str': '192.168.1.6'},
                          'nlri': [{'label': [29],
                                    'rd': '2:2',
                                    'prefix': '192.168.201.0/24'}]},
                     16: [[2, '2:2']]
                     }
        }
        self.maxDiff = None
        self.assertEqual(data_hoped['attr'], Update.parse(None, data_bin[HDR_LEN:], True)['attr'])
        self.assertEqual(data_hoped['attr'],
                         Update.parse(None, Update.construct(msg_dict=data_hoped)[HDR_LEN:], True)['attr'])

    def test_parse_and_construct_ipv4_mpls_vpn_withdraw(self):
        data_bin = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00' \
                   b'\x2c\x02\x00\x00\x00\x15\x80\x0f\x12\x00\x01\x80\x70\x80\x00\x00\x00' \
                   b'\x00\x00\x02\x00\x00\x00\x02\xc0\xa8\xc9'
        data_hoped = {'attr': {15: {'afi_safi': (1, 128),
                                    'withdraw': [{'label': [524288],
                                                  'rd': '2:2',
                                                  'prefix': '192.168.201.0/24'}]}}}
        self.assertEqual(data_hoped['attr'], Update.parse(None, data_bin[HDR_LEN:], True)['attr'])
        self.assertEqual(data_bin, Update.construct(msg_dict=data_hoped))

    def test_parse_construct_l2vpn_evpn(self):
        data_bin = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x63\x02\x00\x00\x00' \
                   b'\x4c\xc0\x10\x08\x06\x00\x01\x00\x00\x00\x01\xf4\x40\x01\x01\x00\x40\x02\x00\x40\x05\x04' \
                   b'\x00\x00\x00\x64\x80\x0e\x30\x00\x19\x46\x04\x0a\x4b\x2c\xfe\x00\x02\x25\x00\x01\xac\x11' \
                   b'\x00\x03\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c\x30\x00\x11\x22' \
                   b'\x33\x44\x55\x20\x0b\x0b\x0b\x01\x00\x00\x00'
        data_dict = {
            "attr": {
                1: 0,
                2: [],
                5: 100,
                14: {
                    "afi_safi": (25, 70),
                    "nexthop": "10.75.44.254",
                    "nlri": [
                        {
                            "type": 2,
                            "value": {
                                "eth_tag_id": 108,
                                "ip": "11.11.11.1",
                                "label": [0],
                                "rd": "172.17.0.3:2",
                                "mac": "00-11-22-33-44-55",
                                "esi": 0}}]
                },
                16: [[1536, 1, 500]]
            }}
        self.assertEqual(data_bin, Update.construct(msg_dict=data_dict))
        self.assertEqual(data_dict['attr'], Update.parse(None, data_bin[HDR_LEN:])['attr'])

if __name__ == '__main__':
    unittest.main()
