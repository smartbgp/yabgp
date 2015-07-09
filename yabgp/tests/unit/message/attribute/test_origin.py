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

""" Test Origin attribute"""

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_INVALID_ORIGIN
from yabgp.message.attribute.origin import Origin


class TestOrigin(unittest.TestCase):

    def test_origin_igp(self):
        self.assertEqual(Origin.IGP, Origin.parse(value=b'\x00'))

    def test_origin_egp(self):
        self.assertEqual(Origin.EGP, Origin.parse(value=b'\x01'))

    def test_origin_incomplete(self):
        self.assertEqual(Origin.INCOMPLETE, Origin.parse(value=b'\x02'))

    def test_invalid_origin(self):

        self.assertRaises(UpdateMessageError, Origin.parse, b'\x03')
        try:
            Origin.parse(b'\x03')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_INVALID_ORIGIN)

    def test_construct(self):

        self.assertEqual(b'\x40\x01\x01\x00', Origin.construct(value=0))
        self.assertEqual(b'\x40\x01\x01\x00', Origin.construct(value=0))
        self.assertEqual(b'\x40\x01\x01\x01', Origin.construct(value=1))
        self.assertEqual(b'\x40\x01\x01\x02', Origin.construct(value=2))

        self.assertRaises(UpdateMessageError, Origin.construct, 3)
        try:
            Origin.construct(3)
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_INVALID_ORIGIN)

if __name__ == '__main__':
    unittest.main()
