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

""" Test Flex Algorithm Definition TLV """

import unittest

from yabgp.message.attribute.linkstate.node.flex_algo_define import (
    FlexAlgorithmDefine,
    FlexAlgoExcludeAdminGroup,
    FlexAlgoIncludeAnyAdminGroup,
    FlexAlgoIncludeAllAdminGroup,
    FlexAlgoDefinitionFlags,
    FlexAlgoExcludeSRLG
)


class TestFlexAlgorithmDefine(unittest.TestCase):
    """Test FlexAlgorithmDefine TLV (Type 1039)"""

    def test_unpack_without_sub_tlvs(self):
        """Test unpack FAD TLV without sub-TLVs

        Data: 80 01 00 80
            - Flex-Algo: 0x80 = 128
            - Metric-Type: 0x01 = 1 (Min Unidirectional Link Delay)
            - Calc-Type: 0x00 = 0 (SPF)
            - Priority: 0x80 = 128
        """
        data_bin = bytes.fromhex('80010080')
        expected = {
            'type': 'flex_algo_defn',
            'value': {
                'flex_algo': 128,
                'metric_type': 1,
                'calc_type': 0,
                'priority': 128,
                'sub_tlvs': []
            }
        }
        self.assertEqual(expected, FlexAlgorithmDefine.unpack(data_bin).dict())

    def test_unpack_with_sub_tlvs(self):
        """Test unpack FAD TLV with sub-TLVs

        Data: 80 01 00 80 04 13 00 02 80 00
            Fixed fields (4 bytes):
                - Flex-Algo: 0x80 = 128
                - Metric-Type: 0x01 = 1 (Min Unidirectional Link Delay)
                - Calc-Type: 0x00 = 0 (SPF)
                - Priority: 0x80 = 128
            Sub-TLV 1043 (6 bytes):
                - Type: 0x0413 = 1043 (Flex-Algo Definition Flags)
                - Length: 0x0002 = 2
                - Value: 0x8000 (M-flag = 1)
        """
        data_bin = bytes.fromhex('80010080' + '041300028000')
        expected = {
            'type': 'flex_algo_defn',
            'value': {
                'flex_algo': 128,
                'metric_type': 1,
                'calc_type': 0,
                'priority': 128,
                'sub_tlvs': [
                    {
                        'type': 'flex_algo_defn_flags',
                        'value': {'M': 1}
                    }
                ]
            }
        }
        self.assertEqual(expected, FlexAlgorithmDefine.unpack(data_bin).dict())


class TestFlexAlgoExcludeAdminGroup(unittest.TestCase):
    """Test FlexAlgoExcludeAdminGroup TLV (Type 1040)"""

    def test_unpack_single_group(self):
        """Test unpack with single admin group

        Data: 00 00 00 01
            - Admin Group: 0x00000001 = 1
        """
        data_bin = bytes.fromhex('00000001')
        expected = {
            'type': 'flex_algo_excl_admin_group',
            'value': [1]
        }
        self.assertEqual(expected, FlexAlgoExcludeAdminGroup.unpack(data_bin).dict())

    def test_unpack_multiple_groups(self):
        """Test unpack with multiple admin groups

        Data: 00 00 00 01 00 00 00 02 FF FF FF FF
            - Admin Group 1: 0x00000001 = 1
            - Admin Group 2: 0x00000002 = 2
            - Admin Group 3: 0xFFFFFFFF = 4294967295
        """
        data_bin = bytes.fromhex('000000010000000200000003')
        expected = {
            'type': 'flex_algo_excl_admin_group',
            'value': [1, 2, 3]
        }
        self.assertEqual(expected, FlexAlgoExcludeAdminGroup.unpack(data_bin).dict())


class TestFlexAlgoIncludeAnyAdminGroup(unittest.TestCase):
    """Test FlexAlgoIncludeAnyAdminGroup TLV (Type 1041)"""

    def test_unpack(self):
        """Test unpack Include-Any Admin Group"""
        data_bin = bytes.fromhex('00000001000000FF')
        expected = {
            'type': 'flex_algo_incl_any_admin_group',
            'value': [1, 255]
        }
        self.assertEqual(expected, FlexAlgoIncludeAnyAdminGroup.unpack(data_bin).dict())


class TestFlexAlgoIncludeAllAdminGroup(unittest.TestCase):
    """Test FlexAlgoIncludeAllAdminGroup TLV (Type 1042)"""

    def test_unpack(self):
        """Test unpack Include-All Admin Group"""
        data_bin = bytes.fromhex('00000003')
        expected = {
            'type': 'flex_algo_incl_all_admin_group',
            'value': [3]
        }
        self.assertEqual(expected, FlexAlgoIncludeAllAdminGroup.unpack(data_bin).dict())


class TestFlexAlgoDefinitionFlags(unittest.TestCase):
    """Test FlexAlgoDefinitionFlags TLV (Type 1043)"""

    def test_unpack_m_flag_not_set(self):
        """Test unpack with M-flag not set

        Data: 00 00
            - Flags: 0x0000
            - M-flag: 0
        """
        data_bin = bytes.fromhex('0000')
        expected = {
            'type': 'flex_algo_defn_flags',
            'value': {'M': 0}
        }
        self.assertEqual(expected, FlexAlgoDefinitionFlags.unpack(data_bin).dict())

    def test_unpack_m_flag_set(self):
        """Test unpack with M-flag set

        Data: 80 00
            - Flags: 0x8000
            - M-flag: 1 (bit 15 set)
        """
        data_bin = bytes.fromhex('8000')
        expected = {
            'type': 'flex_algo_defn_flags',
            'value': {'M': 1}
        }
        self.assertEqual(expected, FlexAlgoDefinitionFlags.unpack(data_bin).dict())


class TestFlexAlgoExcludeSRLG(unittest.TestCase):
    """Test FlexAlgoExcludeSRLG TLV (Type 1044)"""

    def test_unpack_single_srlg(self):
        """Test unpack with single SRLG value"""
        data_bin = bytes.fromhex('00000064')  # SRLG = 100
        expected = {
            'type': 'flex_algo_excl_srlg',
            'value': [100]
        }
        self.assertEqual(expected, FlexAlgoExcludeSRLG.unpack(data_bin).dict())

    def test_unpack_multiple_srlg(self):
        """Test unpack with multiple SRLG values"""
        data_bin = bytes.fromhex('000000640000012C000001F4')  # SRLG = 100, 300, 500
        expected = {
            'type': 'flex_algo_excl_srlg',
            'value': [100, 300, 500]
        }
        self.assertEqual(expected, FlexAlgoExcludeSRLG.unpack(data_bin).dict())


if __name__ == "__main__":
    unittest.main()
