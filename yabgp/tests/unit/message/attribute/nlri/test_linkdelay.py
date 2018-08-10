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


class TestLinkDelay(unittest.TestCase):

    def test_unpack(self):
        self.maxDiff = None
        data_bin = b"\x04\x04\x00\x04\x03\x03\x03\x03\x04\x40\x00\x04\x00\x00\x00\x00" \
                   b"\x04\x41\x00\x04\x4c\xee\x6b\x28\x04\x42\x00\x04\x00\x00\x00\x00" \
                   b"\x04\x43\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x04\x44\x00\x04\x00\x00\x00\x01\x04\x47\x00\x03" \
                   b"\x00\x00\x01\x04\x4b\x00\x07\x60\x00\x00\x00\x00\x5d\xc1\x01\x0b" \
                   b"\x00\x02\x01\x0a\x04\x5a\x00\x04\x00\x0f\x42\x40\x04\x5b\x00\x08" \
                   b"\x00\x0f\x42\x40\x00\x0f\x42\x40\x04\x5c\x00\x04\x00\x00\x00\x00" \
                   b"\x04\x5d\x00\x04\x11\x11\x11\x11\x04\x5e\x00\x04\x11\x11\x11\x11" \
                   b"\x04\x5f\x00\x04\x11\x11\x11\x11\x04\x60\x00\x04\x11\x11\x11\x11"

        data_dict = {29: [{
            "type": "local_router_id",
            "value": "3.3.3.3"
        }, {
            "type": "admin_group",
            "value": 0
        }, {
            "type": "max_bandwidth",
            "value": 125000000.0
        }, {
            "type": "max_rsv_bandwidth",
            "value": 0.0
        }, {
            "type": "unrsv_bandwidth",
            "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }, {
            "type": "te_metric",
            "value": 1
        }, {
            "type": "igp_metric",
            "value": 1
        }, {
            "type": "adj_sid",
            "value": {
                "flags": {
                    "P": 0,
                    "B": 0,
                    "L": 1,
                    "G": 0,
                    "V": 1
                },
                "value": 24001,
                "weight": 0
            }
        }, {
            "type": "link_msd",
            "value": {
                "type": 1,
                "value": 10
            }
        }, {
            "type": "unidirect_link_delay",
            "value": 1000000
        }, {
            "type": "min_max_unidirect_link_delay",
            "value": {
                "max_link_delay": 1000000,
                "min_link_delay": 1000000
            }
        }, {
            "type": "unidirect_delay_var",
            "value": 0
        }, {
            "type": "unidirect_packet_loss",
            "value": 286331153
        }, {
            "type": "unidirect_residual_bw",
            "value": 286331153
        }, {
            "type": "unidirect_avail_bw",
            "value": 286331153
        }, {
            "type": "unidirect_bw_util",
            "value": 286331153
        }]}

        self.assertEqual(data_dict, LinkState.unpack(data_bin).dict())
