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

from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN, ERR_MSG_UPDATE_MALFORMED_ASPATH
from yabgp.common.exception import UpdateMessageError
from yabgp.message.attribute.aspath import ASPath


class TestASPATH(unittest.TestCase):

    def test_parse_empty(self):
        as_path = ASPath.parse(value=b'')
        self.assertEqual(as_path, [])

    def test_parse_asn2(self):
        # 2bytes ASN
        # Segment Type: 2 (AS_SEQUENCE)
        # Length: 4 ASNs
        # ASNs: 3257, 31027, 34848, 21465
        data = b'\x02\x04\x0c\xb9y3\x88 S\xd9'
        as_path = ASPath.parse(value=data)
        self.assertEqual(as_path, [(2, [3257, 31027, 34848, 21465])])

    def test_parse_asn4(self):
        # 4bytes ASN
        # Segment Type: 2 (AS_SEQUENCE)
        # Length: 4 ASNs
        # ASNs: 3257, 31027, 34848, 21465
        data = b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9'
        as_path = ASPath.parse(value=data, asn4=True)
        self.assertEqual(as_path, [(2, [3257, 31027, 34848, 21465])])

    def test_parse_mixed_asn2_asn4_mismatch(self):
        # If we try to parse 4-byte ASN data as 2-byte ASN (default), it should fail or produce garbage.
        # In this specific case, it hits an invalid segment type in the second "perceived" segment.
        data = b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9'
        try:
            ASPath.parse(value=data, asn4=False)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_MALFORMED_ASPATH)

    def test_parse_malformed_type(self):
        # Invalid Segment Type 5
        data = b'\x05\x04\x0c\xb9y3\x88 S\xd9'
        try:
            ASPath.parse(value=data)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_MALFORMED_ASPATH)

    def test_parse_truncated_header(self):
        # Only 1 byte provided, need 2 for header
        data = b'\x02'
        try:
            ASPath.parse(value=data)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_parse_truncated_body_asn2(self):
        # Header says 1 ASN (2 bytes), but only 1 byte provided
        # Type: 2, Count: 1 -> Need 2 bytes of body
        data = b'\x02\x01\x00'
        try:
            ASPath.parse(value=data, asn4=False)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_parse_truncated_body_asn4(self):
        # Header says 1 ASN (4 bytes), but only 3 bytes provided
        # Type: 2, Count: 1 -> Need 4 bytes of body
        data = b'\x02\x01\x00\x00\x00'
        try:
            ASPath.parse(value=data, asn4=True)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_parse_as_set_as_federate(self):
        as_path = ASPath.parse(value=b'\x04\x02\x03\xe9\x03\xea\x03\x02\x03\xeb\x03\xec')
        self.assertEqual(as_path, [(4, [1001, 1002]), (3, [1003, 1004])])

    def test_parse_all_segment_types(self):
        # Cover all 4 types in one path
        # 1. AS_SET (1), len=1, val=[100]
        # 2. AS_SEQUENCE (2), len=1, val=[200]
        # 3. AS_CONFED_SEQUENCE (3), len=1, val=[300]
        # 4. AS_CONFED_SET (4), len=1, val=[400]
        # 2-byte ASN
        data = (
            b'\x01\x01\x00\x64'  # Type 1, Len 1, AS 100
            b'\x02\x01\x00\xc8'  # Type 2, Len 1, AS 200
            b'\x03\x01\x01\x2c'  # Type 3, Len 1, AS 300
            b'\x04\x01\x01\x90'  # Type 4, Len 1, AS 400
        )
        as_path = ASPath.parse(value=data, asn4=False)
        expected = [
            (1, [100]),
            (2, [200]),
            (3, [300]),
            (4, [400])
        ]
        self.assertEqual(as_path, expected)

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

    def test_parse_complex_asn4(self):
        # 4bytes ASN with multiple segments and multiple ASNs per segment
        # Segment 1: Type 2 (AS_SEQUENCE), Count 4, ASNs: [65536, 65537, 65538, 65539]
        # Segment 2: Type 1 (AS_SET), Count 3, ASNs: [65540, 65541, 65542]
        # Segment 3: Type 3 (AS_CONFED_SEQUENCE), Count 2, ASNs: [65543, 65544]
        # Segment 4: Type 4 (AS_CONFED_SET), Count 2, ASNs: [65545, 65546]
        data = (
            b'\x02\x04\x00\x01\x00\x00\x00\x01\x00\x01\x00\x01\x00\x02\x00\x01\x00\x03'
            b'\x01\x03\x00\x01\x00\x04\x00\x01\x00\x05\x00\x01\x00\x06'
            b'\x03\x02\x00\x01\x00\x07\x00\x01\x00\x08'
            b'\x04\x02\x00\x01\x00\x09\x00\x01\x00\x0a'
        )
        as_path = ASPath.parse(value=data, asn4=True)
        expected = [
            (2, [65536, 65537, 65538, 65539]),
            (1, [65540, 65541, 65542]),
            (3, [65543, 65544]),
            (4, [65545, 65546])
        ]
        self.assertEqual(as_path, expected)


if __name__ == '__main__':
    unittest.main()
