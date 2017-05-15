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
        self.assertEqual(None, LinkState.unpack(data_bin).dict())
