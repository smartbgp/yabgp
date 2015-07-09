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

""" Test AS PATH attribute """

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_MALFORMED_ASPATH
from yabgp.message.attribute.aspath import ASPath


class TestASPATH(unittest.TestCase):
    def test_parse(self):

        as_path = ASPath.parse(value=b'')
        self.assertEqual(as_path, [])

        # 2bytes ASN
        as_path = ASPath.parse(value=b'\x02\x04\x0c\xb9y3\x88 S\xd9')
        self.assertEqual(as_path, [(2, [3257, 31027, 34848, 21465])])

        # 4bytes ASN
        as_path = ASPath.parse(value=b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9',
                               asn4=True)
        self.assertEqual(as_path, [(2, [3257, 31027, 34848, 21465])])

        # MALFORMED_ASPATH
        try:
            ASPath.parse(value=b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_MALFORMED_ASPATH)
        try:
            ASPath.parse(value=b'\x05\x04\x0c\xb9y3\x88 S\xd9')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_MALFORMED_ASPATH)

    def test_parse_as_set_as_federate(self):
        as_path = ASPath.parse(value=b'\x04\x02\x03\xe9\x03\xea\x03\x02\x03\xeb\x03\xec')
        self.assertEqual(as_path, [(4, [1001, 1002]), (3, [1003, 1004])])

    def test_construct(self):

        # 2 bytes ASN
        as_path = ASPath.construct(asn4=False, value=[(2, [3257, 31027, 34848, 21465])])
        self.assertEqual(as_path, b'@\x02\n\x02\x04\x0c\xb9y3\x88 S\xd9')

        # 4 bytes ASN
        as_path = ASPath.construct(asn4=True, value=[(2, [3257, 31027, 34848, 21465])])
        self.assertEqual(as_path, b'@\x02\x12\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9')

    def test_construct_as_set(self):
        as_path = ASPath.construct(asn4=False, value=[(2, [1001, 1002]), (1, [1003, 1004])])
        self.assertEqual(as_path, b'@\x02\x0c\x02\x02\x03\xe9\x03\xea\x01\x02\x03\xeb\x03\xec')

    def test_construct_as_set_as_federate(self):
        as_path = ASPath.construct(asn4=False, value=[(4, [1001, 1002]), (3, [1003, 1004])])
        self.assertEqual(as_path, b'@\x02\x0c\x04\x02\x03\xe9\x03\xea\x03\x02\x03\xeb\x03\xec')


if __name__ == '__main__':
    unittest.main()
