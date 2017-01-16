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

from yabgp.message.attribute.linkstate.linkstate import LinkState


class TestLinkState(unittest.TestCase):

    def test_parse(self):
        ls = {
            29:
                [
                    {'local-router-id': '2.2.2.2'},
                    {'te-default-metric': 10},
                    {'igp-link-metric': 10},
                    {'UNKNOWN': {'type': 1099, 'value': '700000000061a8'}},
                    {'UNKNOWN': {'type': 1099, 'value': '300000000061a9'}}
                ]
        }
        hex_value = b'\x04\x06\x00\x04\x02\x02\x02\x02\x04\x44\x00\x04\x00\x00\x00\x0a' \
                    b'\x04\x47\x00\x03\x00\x00\x0a\x04\x4b\x00\x07\x70\x00\x00\x00\x00' \
                    b'\x61\xa8\x04\x4b\x00\x07\x30\x00\x00\x00\x00\x61\xa9'
        self.assertEqual(ls, LinkState.parse(hex_value).dict())
