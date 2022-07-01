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


class TestLinkState(unittest.TestCase):

    def test_unpack(self):
        data_bin = b'\x04\x04\x00\x04\x02\x02\x02\x02\x04\x06\x00\x04\x01\x01\x01\x01' \
                   b'\x04\x40\x00\x04\x00\x00\x00\x00\x04\x41\x00\x04\x4c\xee\x6b\x28' \
                   b'\x04\x42\x00\x04\x00\x00\x00\x00\x04\x43\x00\x20\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x44\x00\x04' \
                   b'\x00\x00\x00\x0a\x04\x47\x00\x03\x00\x00\x0a\x04\x4b\x00\x07\x70' \
                   b'\x00\x00\x00\x00\x61\xa8\x04\x4b\x00\x07\x30\x00\x00\x00\x00\x61' \
                   b'\xa9'
        data_dict = {29: [
            {
                'type': 'local_router_id',
                'value': '2.2.2.2'
            },
            {
                'type': 'remote_router_id',
                'value': '1.1.1.1'
            },
            {
                'type': 'admin_group',
                'value': 0
            },
            {
                'type': 'max_bandwidth',
                'value': 125000000.0
            },
            {
                'type': 'max_rsv_bandwidth',
                'value': 0.0
            },
            {
                'type': 'unrsv_bandwidth',
                'value': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            },
            {
                'type': 'te_metric',
                'value': 10
            },
            {
                'type': 'igp_metric',
                'value': 10
            },
            {
                'type': 'adj_sid',
                'value': {
                    'flags': {'B': 0, 'G': 1, 'L': 1, 'P': 0, 'V': 1},
                    'value': 25000,
                    'weight': 0
                }
            },
            {
                'type': 'adj_sid',
                'value': {
                    'flags': {'B': 0, 'G': 1, 'L': 1, 'P': 0, 'V': 0},
                    'value': 25001,
                    'weight': 0
                }
            }
        ]}
        self.assertEqual(data_dict, LinkState.unpack(data_bin).dict())
