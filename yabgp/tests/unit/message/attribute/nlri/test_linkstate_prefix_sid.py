# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, version 2.0 (the "License"); you may
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

""" Test Link State attribute"""

import unittest
from yabgp.message.attribute.linkstate.linkstate import LinkState


class TestLinkStatePrefixSID(unittest.TestCase):

    def test_prefix_sid_flags_ospf(self):
        self.maxDiff = None
        data_bin = b'\x04\x86\x00\x07\xb4\x00\x00\x00\x00\x61\xa9'

        data_dict = {29: [{
            'type': 'prefix_sid',
            'value': {
                'sid': 25001,
                'flags': {
                    'NP': 0,
                    'M': 1,
                    'E': 1,
                    'V': 0,
                    'L': 1
                },
                'algorithm': 0
            }
        }]}
        self.assertEqual(data_dict, LinkState.unpack(data_bin, 3).dict())

    def test_prefix_id_flags_isis(self):
        self.maxDiff = None
        data_bin = b'\x04\x86\x00\x07\xb4\x00\x00\x00\x00\x61\xa9'

        data_dict = {29: [{
            'type': 'prefix_sid',
            'value': {
                'sid': 25001,
                'flags': {
                    'R': 1,
                    'N': 0,
                    'P': 1,
                    'E': 1,
                    'V': 0,
                    'L': 1
                },
                'algorithm': 0
            }
        }]}
        self.assertEqual(data_dict, LinkState.unpack(data_bin, 1).dict())
