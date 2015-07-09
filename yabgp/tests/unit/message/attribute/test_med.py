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

"""Test MED attribute
"""

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.message.attribute.med import MED


class TestMED(unittest.TestCase):

    def test_parse(self):

        med = MED.parse(value=b'\x00\x00\x00\xa0')
        self.assertEqual(med, 160)

        # invalid length
        self.assertRaises(UpdateMessageError, MED.parse,
                          b'\x0a\x0a\x0a\x01\x01')

    def test_parse_exception_attr_len(self):
        try:
            MED.parse(b'\x0a\x0a\x0a\x01\x01')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

    def test_construct(self):

        med = MED.construct(value=100)
        self.assertEqual(med, b'\x80\x04\x04\x00\x00\x00d')

    def test_construct_exception_attr_len(self):

        # invalid med value
        self.assertRaises(UpdateMessageError, MED.construct, 4294967296)
        try:
            MED.construct(value=4294967296)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_ATTR_LEN)

if __name__ == '__main__':
    unittest.main()
