# Copyright 2015-2016 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
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

from yabgp.message.attribute.nlri.labeled_unicast.ipv4 import IPv4LabeledUnicast


class TestIPv4LabeledUnicast(unittest.TestCase):

    def test_construct(self):
        nlri_list = [
            {'prefix': '34.1.41.0/24', 'label': [321]},
            {'prefix': '34.1.42.0/24', 'label': [322]}
        ]
        nlri_hex = b'\x30\x00\x14\x11\x22\x01\x29\x30\x00\x14\x21\x22\x01\x2a'
        self.assertEqual(nlri_hex, IPv4LabeledUnicast.construct(nlri_list))

    def test_construct_with_multi_label(self):
        nlri_list = [
            {'prefix': '34.1.41.0/24', 'label': [321, 322]},
            {'prefix': '34.1.42.0/24', 'label': [321, 322]}
        ]
        nlri_hex = b'\x48\x00\x14\x10\x00\x14\x21\x22\x01\x29\x48\x00\x14\x10\x00\x14\x21\x22\x01\x2a'
        self.assertEqual(nlri_hex, IPv4LabeledUnicast.construct(nlri_list))

    def test_parse(self):
        nlri_list = [
            {'prefix': '34.1.41.0/24', 'label': [321]},
            {'prefix': '34.1.42.0/24', 'label': [322]}
        ]
        nlri_hex = b'\x30\x00\x14\x11\x22\x01\x29\x30\x00\x14\x21\x22\x01\x2a'
        self.assertEqual(nlri_list, IPv4LabeledUnicast.parse(nlri_hex))

    def test_parse_with_multi_label(self):
        nlri_list = [
            {'prefix': '34.1.41.0/24', 'label': [321, 322]},
            {'prefix': '34.1.42.0/24', 'label': [321, 322]}
        ]
        nlri_hex = b'\x48\x00\x14\x10\x00\x14\x21\x22\x01\x29\x48\x00\x14\x10\x00\x14\x21\x22\x01\x2a'
        self.assertEqual(nlri_list, IPv4LabeledUnicast.parse(nlri_hex))


if __name__ == '__main__':
    unittest.main()
