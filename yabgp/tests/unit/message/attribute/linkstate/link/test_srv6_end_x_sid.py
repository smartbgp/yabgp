# Copyright 2022 Cisco Systems, Inc.
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

""" Test SRv6 End.X SID """

import unittest

from yabgp.message.attribute.linkstate.link.srv6_end_x_sid import SRv6EndXSid


class TestSRv6EndXSid(unittest.TestCase):

    def test_unpack(self):
        data_bin = b'\x04\x52' \
                   b'\x00\x1e' \
                   b'\x00\x39' \
                   b'\x00' \
                   b'\x00' \
                   b'\x00' \
                   b'\x00' \
                   b'\xa0\x01\x00\x00\x00\x05\xe0\x02\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x04\xe4' \
                   b'\x00\x04' \
                   b'\x20\x10\x10\x00'

        data_dict = {
            'type': 'srv6_end_x_sid',
            'value': {
                'endpoint_behavior': 57,
                'flags': 0,
                'algorithm': 0,
                'weight': 0,
                'reserved': 0,
                'sid': 'a001:0:5:e002::',
                'sub_tlvs': [
                    {
                        'type': 'srv6_sid',
                        'value': {
                            'locator_block_length': 32,
                            'locator_node_length': 16,
                            'function_length': 16,
                            'argument_length': 0
                        }
                    }
                ]
            }
        }
        # The total of the locator block, locator node, function, and argument lengths MUST be less than or equal to 128

        # Note: data_bin[4:] means does not contains "type_code" & "length"
        self.assertEqual(data_dict, SRv6EndXSid.unpack(data_bin[4:]).dict())
