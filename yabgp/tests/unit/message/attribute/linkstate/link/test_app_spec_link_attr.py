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

""" Test Application-Specific Link Attributes TLV """

import unittest

from yabgp.message.attribute.linkstate.link.app_spec_link_attr import AppSpecLinkAttr


class TestAppSpecLinkAttr(unittest.TestCase):
    """Test AppSpecLinkAttr TLV (Type 1122)"""

    def test_unpack_with_te_metric(self):
        """Test unpack ASLA TLV with TE Metric sub-TLV

        Data: 04 04 00 00 10 00 00 00 00 00 00 00 04 44 00 04 ff ff ff ff
            Header (4 bytes):
                - SABM Length: 0x04 = 4
                - UDABM Length: 0x04 = 4
                - Reserved: 0x0000
            SABM (4 bytes): 0x10000000
            UDABM (4 bytes): 0x00000000
            Sub-TLV (8 bytes):
                - Type: 0x0444 = 1092 (TE Default Metric)
                - Length: 0x0004 = 4
                - Value: 0xffffffff = 4294967295
        """
        data_bin = bytes.fromhex('04040000100000000000000004440004ffffffff')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 4, 'value': '0x10000000'},
                'udabm': {'len': 4, 'value': '0x00000000'},
                'sub_tlvs': [
                    {
                        'type': 'te_metric',
                        'value': 4294967295
                    }
                ]
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_zero_length_masks(self):
        """Test unpack ASLA TLV with zero-length SABM and UDABM

        Data: 00 00 00 00 04 44 00 04 00 00 00 64
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
            SABM: none (length = 0)
            UDABM: none (length = 0)
            Sub-TLV (8 bytes):
                - Type: 0x0444 = 1092 (TE Default Metric)
                - Length: 0x0004 = 4
                - Value: 0x00000064 = 100
        """
        data_bin = bytes.fromhex('000000000444000400000064')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 0, 'value': None},
                'udabm': {'len': 0, 'value': None},
                'sub_tlvs': [
                    {
                        'type': 'te_metric',
                        'value': 100
                    }
                ]
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_8_byte_masks(self):
        """Test unpack ASLA TLV with 8-byte (64-bit) SABM and UDABM

        Data: 08 08 00 00 12 34 56 78 9a bc de f0 00 00 00 00 00 00 00 ff
            Header (4 bytes):
                - SABM Length: 0x08 = 8
                - UDABM Length: 0x08 = 8
                - Reserved: 0x0000
            SABM (8 bytes): 0x123456789abcdef0
            UDABM (8 bytes): 0x00000000000000ff
        """
        data_bin = bytes.fromhex('08080000123456789abcdef000000000000000ff')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 8, 'value': '0x123456789abcdef0'},
                'udabm': {'len': 8, 'value': '0x00000000000000ff'},
                'sub_tlvs': []
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_only_sabm(self):
        """Test unpack ASLA TLV with only SABM (UDABM length = 0)

        Data: 04 00 00 00 10 00 00 00
            Header (4 bytes):
                - SABM Length: 0x04 = 4
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
            SABM (4 bytes): 0x10000000
            UDABM: none (length = 0)
        """
        data_bin = bytes.fromhex('0400000010000000')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 4, 'value': '0x10000000'},
                'udabm': {'len': 0, 'value': None},
                'sub_tlvs': []
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_only_udabm(self):
        """Test unpack ASLA TLV with only UDABM (SABM length = 0)

        Data: 00 04 00 00 ab cd ef 12
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x04 = 4
                - Reserved: 0x0000
            SABM: none (length = 0)
            UDABM (4 bytes): 0xabcdef12
        """
        data_bin = bytes.fromhex('00040000abcdef12')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 0, 'value': None},
                'udabm': {'len': 4, 'value': '0xabcdef12'},
                'sub_tlvs': []
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_unknown_sub_tlv(self):
        """Test unpack ASLA TLV with unknown sub-TLV type

        Data: 00 00 00 00 ff ff 00 04 de ad be ef
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
            Sub-TLV (8 bytes):
                - Type: 0xffff = 65535 (Unknown)
                - Length: 0x0004 = 4
                - Value: 0xdeadbeef
        """
        data_bin = bytes.fromhex('00000000ffff0004deadbeef')

        result = AppSpecLinkAttr.unpack(data_bin).dict()

        self.assertEqual(result['type'], 'ASLA')
        self.assertEqual(result['value']['sabm'], {'len': 0, 'value': None})
        self.assertEqual(result['value']['udabm'], {'len': 0, 'value': None})
        self.assertEqual(len(result['value']['sub_tlvs']), 1)
        self.assertEqual(result['value']['sub_tlvs'][0]['type'], 65535)
        # Unknown sub-TLV value is returned as hex string
        self.assertIn('deadbeef', result['value']['sub_tlvs'][0]['value'].lower())

    def test_unpack_with_multiple_sub_tlvs(self):
        """Test unpack ASLA TLV with multiple sub-TLVs

        Data: 04 04 00 00 10 00 00 00 00 00 00 00
              04 44 00 04 00 00 00 0a
              04 44 00 04 00 00 00 14
            Header (4 bytes):
                - SABM Length: 0x04 = 4
                - UDABM Length: 0x04 = 4
                - Reserved: 0x0000
            SABM (4 bytes): 0x10000000
            UDABM (4 bytes): 0x00000000
            Sub-TLV 1 (8 bytes):
                - Type: 0x0444 = 1092 (TE Default Metric)
                - Length: 0x0004 = 4
                - Value: 0x0000000a = 10
            Sub-TLV 2 (8 bytes):
                - Type: 0x0444 = 1092 (TE Default Metric)
                - Length: 0x0004 = 4
                - Value: 0x00000014 = 20
        """
        data_bin = bytes.fromhex(
            '04040000'          # Header
            '10000000'          # SABM
            '00000000'          # UDABM
            '044400040000000a'  # Sub-TLV 1: TE Metric = 10
            '0444000400000014'  # Sub-TLV 2: TE Metric = 20
        )

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 4, 'value': '0x10000000'},
                'udabm': {'len': 4, 'value': '0x00000000'},
                'sub_tlvs': [
                    {'type': 'te_metric', 'value': 10},
                    {'type': 'te_metric', 'value': 20}
                ]
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_header_only(self):
        """Test unpack ASLA TLV with header only (no masks, no sub-TLVs)

        Data: 00 00 00 00
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
        """
        data_bin = bytes.fromhex('00000000')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 0, 'value': None},
                'udabm': {'len': 0, 'value': None},
                'sub_tlvs': []
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    def test_unpack_with_8_byte_sabm_4_byte_udabm(self):
        """Test unpack ASLA TLV with mixed mask lengths (8-byte SABM, 4-byte UDABM)

        Data: 08 04 00 00 00 00 00 00 00 00 00 01 ff ff ff ff
            Header (4 bytes):
                - SABM Length: 0x08 = 8
                - UDABM Length: 0x04 = 4
                - Reserved: 0x0000
            SABM (8 bytes): 0x0000000000000001
            UDABM (4 bytes): 0xffffffff
        """
        data_bin = bytes.fromhex('080400000000000000000001ffffffff')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 8, 'value': '0x0000000000000001'},
                'udabm': {'len': 4, 'value': '0xffffffff'},
                'sub_tlvs': []
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())

    # ==================== Exception/Abnormal Packet Tests ====================

    def test_unpack_data_too_short(self):
        """Test unpack ASLA TLV with data shorter than header (< 4 bytes)

        Data: 04 04 00 (only 3 bytes, header requires 4 bytes)
        Expected: IndexError or struct.error
        """
        data_bin = bytes.fromhex('040400')  # Only 3 bytes

        with self.assertRaises((IndexError, Exception)):
            AppSpecLinkAttr.unpack(data_bin)

    def test_unpack_empty_data(self):
        """Test unpack ASLA TLV with empty data

        Data: (empty)
        Expected: IndexError or struct.error
        """
        data_bin = b''

        with self.assertRaises((IndexError, Exception)):
            AppSpecLinkAttr.unpack(data_bin)

    def test_unpack_sabm_length_exceeds_data(self):
        """Test unpack ASLA TLV where SABM length exceeds available data

        Data: 08 00 00 00 12 34 56 78 (SABM length=8 but only 4 bytes available)
            Header (4 bytes):
                - SABM Length: 0x08 = 8 (but only 4 bytes follow)
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
            SABM: 0x12345678 (truncated, should be 8 bytes)
        Expected: struct.error or incorrect parsing
        """
        data_bin = bytes.fromhex('0800000012345678')  # SABM length=8, but only 4 bytes

        with self.assertRaises((Exception,)):
            AppSpecLinkAttr.unpack(data_bin)

    def test_unpack_udabm_length_exceeds_data(self):
        """Test unpack ASLA TLV where UDABM length exceeds available data

        Data: 00 08 00 00 12 34 56 78 (UDABM length=8 but only 4 bytes available)
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x08 = 8 (but only 4 bytes follow)
                - Reserved: 0x0000
            UDABM: 0x12345678 (truncated, should be 8 bytes)
        Expected: struct.error or incorrect parsing
        """
        data_bin = bytes.fromhex('0008000012345678')  # UDABM length=8, but only 4 bytes

        with self.assertRaises((Exception,)):
            AppSpecLinkAttr.unpack(data_bin)

    def test_unpack_sub_tlv_header_incomplete(self):
        """Test unpack ASLA TLV where sub-TLV header is incomplete

        Data: 00 00 00 00 04 44 (sub-TLV type present but length missing)
            Header (4 bytes):
                - SABM Length: 0x00 = 0
                - UDABM Length: 0x00 = 0
                - Reserved: 0x0000
            Sub-TLV: incomplete header (only 2 bytes, needs 4 for type+length)
        Expected: struct.error
        """
        data_bin = bytes.fromhex('000000000444')  # Incomplete sub-TLV header

        with self.assertRaises((Exception,)):
            AppSpecLinkAttr.unpack(data_bin)


if __name__ == "__main__":
    unittest.main()
