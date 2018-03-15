# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http:\\www.apache.org\licenses\LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest

from yabgp.message.attribute.nlri.linkstate import BGPLS


class TestBGPLS(unittest.TestCase):

    def test_parse(self):
        self.maxDiff = None
        data_bin = b"\x00\x02\x00" \
                   b"\x55\x02\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x1a\x02\x00" \
                   b"\x00\x04\x00\x00\xff\xfe\x02\x01\x00\x04\x00\x00\x00\x00\x02\x03" \
                   b"\x00\x06\x00\x00\x00\x00\x00\x03\x01\x01\x00\x1a\x02\x00\x00\x04" \
                   b"\x00\x00\xff\xfe\x02\x01\x00\x04\x00\x00\x00\x00\x02\x03\x00\x06" \
                   b"\x00\x00\x00\x00\x00\x01\x01\x03\x00\x04\x01\x03\x00\x02\x01\x04" \
                   b"\x00\x04\x01\x03\x00\x01"
        data_dict = [
            {
                'type': 'link',
                'protocol_id': 2,
                'instances_id': 0,
                'descriptors': [
                    {
                        'type': 'local_node',
                        'value': {
                            'as': 65534,
                            'bgpls_id': '0.0.0.0',
                            'igp_router_id': '0.0.0.3'}},
                    {
                        'type': 'remote_node',
                        'value': {
                            'as': 65534,
                            'bgpls_id': '0.0.0.0',
                            'igp_router_id': '0.0.0.1'}},
                    {
                        'type': 'link_local_ipv4',
                        'value': '1.3.0.2'},
                    {
                        'type': 'link_remote_ipv4',
                        'value': '1.3.0.1'},
                ]
            }
        ]
        self.assertEqual(data_dict, BGPLS.parse(data_bin))
