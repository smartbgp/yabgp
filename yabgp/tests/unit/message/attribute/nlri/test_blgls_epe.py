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


class TestBGPLSEPE(unittest.TestCase):

    def test_parse(self):
        self.maxDiff = None
        data_bin = b"\x00\x02\x00\x51\x07\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00" \
                   b"\x18\x02\x00\x00\x04\x00\x00\x00\xc8\x02\x01\x00\x04\x00\x00\x00" \
                   b"\x00\x02\x05\x00\x04\x00\x00\x00" \
                   b"\xc8\x01\x01\x00\x18\x02\x00\x00\x04\x00\x00\x01\x2c\x02\x01\x00" \
                   b"\x04\x00\x00\x00\x00\x02\x05\x00" \
                   b"\x04\x00\x00\x01\x2c\x01\x03\x00\x04\xc0\xa8\x04\x03\x01\x04\x00" \
                   b"\x04\xc0\xa8\x04\x04"
        data_dict = [
            {
                'type': 'link',
                'protocol_id': 7,
                'instances_id': 0,
                'descriptors': [
                    {
                        'type': 'local_node',
                        'value': {
                            'as_num': 200,
                            'bgpls_id': '0.0.0.0',
                            # 'bgp_router_id': '3.3.3.3',
                            'member_as_num': 200}},
                    {
                        'type': 'remote_node',
                        'value': {
                            'as_num': 300,
                            'bgpls_id': '0.0.0.0',
                            # 'bgp_router_id': '4.4.4.4',
                            'member_as_num': 300}},
                    {
                        'type': 'link_local_ipv4',
                        'value': '192.168.4.3'},
                    {
                        'type': 'link_remote_ipv4',
                        'value': '192.168.4.4'},
                ]
            }
        ]
        self.assertEqual(data_dict, BGPLS.parse(data_bin))
