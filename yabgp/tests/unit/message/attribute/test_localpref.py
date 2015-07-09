# Copyright 2015 Cisco Systems, Inc.
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

"""Test LocalPreference attribute
"""

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.message.attribute.localpref import LocalPreference


class TestLocalPreference(unittest.TestCase):

    def test_parse(self):

        local_pre = LocalPreference.parse(value=b'\x00\x00\x00\xa0')
        self.assertEqual(local_pre, 160)

    def test_parse_invalid_length(self):
        # invalid length
        self.assertRaises(UpdateMessageError, LocalPreference.parse,
                          b'\x0a\x0a\x0a\x01\x01')
        try:
            LocalPreference.parse(b'\x0a\x0a\x0a\x01\x01')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_construct(self):

        local_pre = LocalPreference.construct(value=100)
        self.assertEqual(b'\x40\x05\x04\x00\x00\x00\x64', local_pre)

    def test_construct_excetion_attr_len(self):
        # invalid med value
        self.assertRaises(UpdateMessageError, LocalPreference.construct, 4294967296)
        try:
            LocalPreference.construct(value=4294967296)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

if __name__ == '__main__':
    unittest.main()
