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

"""Test Originator ID attribute
"""

import unittest

from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.common import exception as excep
from yabgp.message.attribute.originatorid import OriginatorID


class TestOriginatorID(unittest.TestCase):

    def test_parse(self):

        # normal
        originator_id = OriginatorID.parse(value=b'\xc0\xa8\x01\x01')
        self.assertEqual('192.168.1.1', originator_id)

        # invalid attribute length
        self.assertRaises(excep.UpdateMessageError, OriginatorID.parse,
                          b'\xc0\xa8\x01\x01\x01')
        try:
            OriginatorID.parse(value=b'\xc0\xa8\x01\x01\x01')
        except excep.UpdateMessageError as e:
            self.assertEqual(ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

    def test_construct(self):

        originator_id = OriginatorID.construct(value='192.168.1.1')
        self.assertEqual(b'\x80\x09\x04\xc0\xa8\x01\x01', originator_id)

        # invalid value
        self.assertRaises(excep.UpdateMessageError, OriginatorID.construct,
                          b'\xc0\xa8\x01\x01\x01')
        try:
            OriginatorID.construct(value=b'\xc0\xa8\x01\x01\x01')
        except excep.UpdateMessageError as e:
            self.assertEqual(ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

if __name__ == '__main__':
    unittest.main()
