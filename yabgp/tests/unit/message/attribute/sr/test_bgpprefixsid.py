# Copyright 2024 Cisco Systems, Inc.
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

""" Test BGP Prefix SID TLV """

import unittest

from yabgp.message.update import BGPPrefixSID


class TestBGPPrefixSID(unittest.TestCase):

    def test_unpack(self):
        """

        :return:
        """
        data_bin = b'\xc0\x28\x25' \
                   b'\x05\x00\x22\x00' \
                   b'\x01\x00\x1e\x00\x20\x05\xbb\x00\x01\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\x00' \
                   b'\x01\x00\x06\x20\x10\x10\x00\x10\x30'
        data_list = [{
            'srv6_l3_service': {
                'srv6_service_sub_tlvs': [{
                    'srv6_sid_information': {
                        'srv6_sid_value': '2005:bb00:112::',
                        'srv6_service_sid_flags': 0,
                        'srv6_endpoint_behavior': 63,
                        'srv6_service_data_sub_sub_tlvs': [{
                            'srv6_sid_structure': {
                                'locator_block_length': 32,
                                'locator_node_length': 16,
                                'function_length': 16,
                                'argument_length': 0,
                                'transposition_length': 16,
                                'transposition_offset': 48
                            }
                        }]
                    }
                }]
            }
        }]
        self.assertEqual(data_list, BGPPrefixSID.unpack(data=data_bin[3:]))
