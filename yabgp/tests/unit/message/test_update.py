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

    def test_parse_prefix_mask_larger_than_32(self):
        prefix_hex = b'\x21\xb8\x9d\xe0\x18E\xb3\xdd\x18E\xb3\xdc\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        self.assertRaises(UpdateMessageError, Update.parse_prefix_list, prefix_hex)

    def test_construct_prefix_v4(self):
        nlri = ['184.157.224.1/32', '32.65.243.12/30', '89.232.254.0/23', '69.179.221.0/24',
                '61.172.0.0/16', '202.223.128.0/17', '156.152.0.0/15', '15.0.0.0/8',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        nlri_hex = Update.construct_prefix_v4(nlri)
        self.assertEqual(nlri, Update.parse_prefix_list(nlri_hex))

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
        update = Update.parse([None, False, msg_hex])
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
        update = Update.parse([None, True, msg_hex])
        attributes = {1: 2, 2: [(2, [30]), (1, [10, 20])], 3: '10.0.0.9', 4: 0, 7: (30, '10.0.0.9')}
        self.assertEqual(attributes, update['attr'])
        self.assertEqual([], update['withdraw'])
        self.assertEqual(['172.16.0.0/21'], update['nlri'])


if __name__ == '__main__':
    unittest.main()
