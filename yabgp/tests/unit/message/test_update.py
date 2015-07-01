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

from yabgp.message.update import Update
from yabgp.common.exception import UpdateMessageError


class TestUpdate(unittest.TestCase):
    def test_parse_prefix_list(self):

        prefix_hex = b'\x13\xb8\x9d\xe0\x18E\xb3\xdd\x18E\xb3\xdc\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        nlri = ['184.157.224.0/19', '69.179.221.0/24', '69.179.220.0/24',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        self.assertEqual(nlri, Update().parse_prefix_list(prefix_hex))

    def test_parse_prefix_mask_larger_than_32(self):
        prefix_hex = b'\x21\xb8\x9d\xe0\x18E\xb3\xdd\x18E\xb3\xdc\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        self.assertRaises(UpdateMessageError, Update().parse_prefix_list, prefix_hex)

    def test_construct_prefix_v4(self):
        nlri = ['184.157.224.0/19', '69.179.221.0/24', '69.179.220.0/24',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        nlri_hex = Update().construct_prefix_v4(nlri)
        self.assertEqual(nlri, Update.parse_prefix_list(nlri_hex))

    # def test_parse_attributes_ipv4(self):
    #
    #     attr_hex = b'@\x01\x01\x00@\x02\x08\x02\x03\x00\x01\x00\x02\x00\x03@\x03\x04\xac\x10\x01\x0e\x80\x04\x04' \
    #                b'\x00\x00\x00\x00@\x05\x04\x00\x00\x00d\x80\t\x04\xac\x10\x01\x0e\x80\n\x08\x02\x02\x02\x02dddd'
    #     attributes = {1: 0,
    #                   2: [(2, [1, 2, 3])],
    #                   3: '172.16.1.14',
    #                   4: 0,
    #                   5: 100,
    #                   9: '172.16.1.14',
    #                   10: ['2.2.2.2', '100.100.100.100']}
    #     self.assertEqual(attributes, Update().parse_attributes(attr_hex, False))


if __name__ == '__main__':
    unittest.main()
