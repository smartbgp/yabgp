# Copyright 2025 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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

""" Test Multi-Topology Identifier TLV """

import unittest

from yabgp.message.attribute.linkstate.node.mt_id import MultiTopologyIdentifier


class TestMultiTopologyIdentifier(unittest.TestCase):
    """Test MultiTopologyIdentifier TLV (Type 263)
    """

    def test_unpack_single_mt_id(self):
        """Test unpack with single MT-ID

        Data: 00 02
            - Reserved: 0x0
            - MT-ID: 0x002 = 2 (IPv6 unicast)
        """
        data_bin = bytes.fromhex('0002')

        expected = {
            'type': 'mt_id',
            'value': [2]
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    def test_unpack_multiple_mt_ids(self):
        """Test unpack with multiple MT-IDs

        Data: 00 00 00 02 00 03
            - MT-ID 1: 0x0000 = 0 (default topology)
            - MT-ID 2: 0x0002 = 2 (IPv6 unicast)
            - MT-ID 3: 0x0003 = 3 (IPv4 multicast)
        """
        data_bin = bytes.fromhex('000000020003')

        expected = {
            'type': 'mt_id',
            'value': [0, 2, 3]
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    def test_unpack_empty_data(self):
        """Test unpack with empty data

        Data: (empty)
        Expected: Empty MT-ID list
        """
        data_bin = b''

        expected = {
            'type': 'mt_id',
            'value': []
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    def test_unpack_default_topology(self):
        """Test unpack with default topology (MT-ID = 0)

        Data: 00 00
            - MT-ID: 0x0000 = 0 (default topology)
        """
        data_bin = bytes.fromhex('0000')

        expected = {
            'type': 'mt_id',
            'value': [0]
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    def test_unpack_max_mt_id(self):
        """Test unpack with maximum MT-ID value (0xFFFF)

        Data: ff ff
            - MT-ID: 0xFFFF = 65535 (maximum value)
        """
        data_bin = bytes.fromhex('ffff')

        expected = {
            'type': 'mt_id',
            'value': [65535]
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    def test_unpack_common_mt_ids(self):
        """Test unpack with common MT-ID values

        Common MT-IDs (RFC 5120):
            - 0: Default topology
            - 2: IPv6 unicast topology
            - 3: IPv4 multicast topology
            - 4: IPv6 multicast topology

        Data: 00 00 00 02 00 03 00 04
        """
        data_bin = bytes.fromhex('0000000200030004')

        expected = {
            'type': 'mt_id',
            'value': [0, 2, 3, 4]
        }

        self.assertEqual(expected, MultiTopologyIdentifier.unpack(data_bin).dict())

    # ==================== Exception/Abnormal Packet Tests ====================

    def test_unpack_single_byte(self):
        """Test unpack with single byte (incomplete MT-ID)

        Data: 00 (only 1 byte, MT-ID requires 2 bytes)
        Expected: struct.error
        """
        data_bin = bytes.fromhex('00')

        with self.assertRaises(Exception):
            MultiTopologyIdentifier.unpack(data_bin)

    def test_unpack_odd_bytes_3(self):
        """Test unpack with odd number of bytes (3 bytes)

        Data: 00 02 00 (3 bytes, last byte is incomplete)
            - MT-ID 1: 0x0002 = 2 (parsed successfully)
            - Remaining: 0x00 (incomplete, only 1 byte)
        Expected: struct.error on second iteration
        """
        data_bin = bytes.fromhex('000200')

        with self.assertRaises(Exception):
            MultiTopologyIdentifier.unpack(data_bin)

    def test_unpack_odd_bytes_5(self):
        """Test unpack with odd number of bytes (5 bytes)

        Data: 00 02 00 03 00 (5 bytes)
            - MT-ID 1: 0x0002 = 2
            - MT-ID 2: 0x0003 = 3
            - Remaining: 0x00 (incomplete)
        Expected: struct.error on third iteration
        """
        data_bin = bytes.fromhex('0002000300')

        with self.assertRaises(Exception):
            MultiTopologyIdentifier.unpack(data_bin)


if __name__ == "__main__":
    unittest.main()
