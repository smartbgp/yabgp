# Copyright 2015-2017 Cisco Systems, Inc.
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

import unittest

from yabgp.message.attribute.tunnelencaps import TunnelEncaps


class TestTunnelEncaps(unittest.TestCase):

    def test_construct_optional_label_sid(self):
        option_sid = 16384255
        data_dict = {
            "label": 4000,
            "TC": 0,
            "S": 0,
            "TTL": 255
        }
        self.assertEqual(option_sid, TunnelEncaps.construct_optional_label_sid(data_dict))

    def test_construct_weight(self):
        data_dict = {"9": 10, "1": []}
        segment_list = dict([(int(l), r) for (l, r) in data_dict.items()])
        weight_hex = b'\x09\x06\x00\x00\x00\x00\x00\x0a'
        sid_hex = b''
        self.assertEqual((weight_hex, sid_hex), TunnelEncaps.construct_weight_and_seg(segment_list))

    def test_construct_seg(self):
        data_dict = {
            "1": [
                {
                    "1": {
                        "label": 2000
                    }
                },
                {
                    "3": {
                        "node": "10.1.1.1",
                        "SID": {
                            "label": 2000,
                            "TC": 0,
                            "S": 0,
                            "TTL": 255
                        }
                    }
                }
            ]
        }
        segment_list = dict([(int(l), r) for (l, r) in data_dict.items()])
        weight_hex = b''
        sid_hex = b'\x01\x06\x00\x00\x00\x7d\x00\xff\x03\x0a\x00\x00\x0a\x01\x01\x01\x00\x7d\x00\xff'
        self.assertEqual((weight_hex, sid_hex), TunnelEncaps.construct_weight_and_seg(segment_list))

    def test_construct_old_binding_sid(self):
        data_dict = {"0": "old", "7": 25102}
        data_hex = b'\x07\x06\x00\x00\x06\x20\xe0\x00'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[8:])

    def test_construct_old_preference(self):
        data_dict = {"0": "old", "6": 100}
        data_hex = b'\x06\x06\x00\x00\x00\x00\x00\x64'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[8:16])

    def test_construct_new_binding_sid(self):
        data_dict = {"0": "new", "13": 25102}
        data_hex = b'\x0d\x06\x00\x00\x06\x20\xe0\x00'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[8:])

    def test_construct_new_preference(self):
        data_dict = {"0": "new", "12": 100}
        data_hex = b'\x0c\x06\x00\x00\x00\x00\x00\x64'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[8:16])

    def test_construct_segement_lists(self):
        data_dict = {
            "0": "old",
            "128": [
                {
                    "9": 10,
                    "1": [
                        {
                            "1": {
                                "label": 2000
                            }
                        },
                        {
                            "3": {
                                "node": "10.1.1.1",
                                "SID": {
                                    "label": 2000,
                                    "TC": 0,
                                    "S": 0,
                                    "TTL": 255
                                }
                            }
                        }
                    ]
                }
            ]
        }
        data_hex_1 = b'\x80\x00\x1d\x00\x09\x06\x00\x00\x00\x00\x00\x0a\x01\x06\x00\x00\x00\x7d\x00' \
                     b'\xff\x03\x0a\x00\x00\x0a\x01\x01\x01\x00\x7d\x00\xff\x07\x02\x00\x00'
        data_hex_2 = b'\x07\x02\x00\x00\x80\x00\x1d\x00\x09\x06\x00\x00\x00\x00\x00\x0a\x01\x06\x00' \
                     b'\x00\x00\x7d\x00\xff\x03\x0a\x00\x00\x0a\x01\x01\x01\x00\x7d\x00\xff'
        self.assertTrue(TunnelEncaps.construct(data_dict)[8:] in [data_hex_1, data_hex_2])

    def test_construct_enlp(self):
        data_dict = {
            "0": "new",
            "14": 1
        }
        data_hex = b'\x0e\x03\x00\x00\x01'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[12:])

    def test_construct_priority(self):
        data_dict = {
            "0": "new",
            "15": 200
        }
        data_hex = data_hex = b'\x0f\x02\xc8\x00'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[12:])

    def test_construct_policy_name(self):
        data_dict = {
            "0": "new",
            "129": "test"
        }
        data_hex = data_hex = b'\x81\x00\x05\x00\x74\x65\x73\x74'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[12:])

    def test_construct_remote_endpoint_ipv4(self):
        data_dict = {
            "0": "new",
            "6": {"asn": 300, 'afi': 'ipv4', 'address': '1.1.1.1'}
        }
        data_hex = b'\x06\x0a\x00\x00\x01\x2c\x00\x01\x01\x01\x01\x01'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[12:])

    def test_construct_remote_endpoint_ipv6(self):
        data_dict = {
            "0": "new",
            "6": {"asn": 300, 'afi': 'ipv6', 'address': 'ABCD:EF01:2345:6789:ABCD:EF01:2345:6789'}
        }
        data_hex = b'\x06\x16\x00\x00\x01\x2c\x00\x02\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef' \
                   b'\x01\x23\x45\x67\x89'
        self.assertEqual(data_hex, TunnelEncaps.construct(data_dict)[12:])


if __name__ == '__main__':
    unittest.main()
