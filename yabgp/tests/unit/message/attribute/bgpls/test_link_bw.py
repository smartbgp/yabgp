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


class TestLinkBW(unittest.TestCase):

    def test_max_link_bw_parse(self):
        hex_value = b'\x04\x41\x00\x04\x4c\xee\x6b\x28'
        ls = {29: [{'maximum-link-bandwidth': 125000000.0}]}
        self.assertEqual(ls, LinkState.parse(hex_value).dict())

    def test_max_rsvp_link_bw(self):
        hex_value = b'\x04\x42\x00\x04\x00\x00\x00\x00'
        ls = {29: [{'maximum-link-bandwidth': 0.0}]}
        self.assertEqual(ls, LinkState.parse(hex_value).dict())
