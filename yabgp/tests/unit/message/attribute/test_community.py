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

""" Test Community attribute """

import unittest

from yabgp.common import exception as excep
from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.message.attribute.community import Community


class TestCommunity(unittest.TestCase):

    def test_parse(self):

        community = Community.parse(value=b'\xff\xff\xff\x01')
        self.assertEqual(['NO_EXPORT'], community)

        community = Community.parse(value=b'\xff\xff\xff\x01\x12\xe5&\xc9')
        self.assertEqual(['NO_EXPORT', '4837:9929'], community)

        community = Community.parse(value=b'\x12\xe5\x04\xd7\x12\xe5&\xc9')
        self.assertEqual(['4837:1239', '4837:9929'], community)

        self.assertRaises(excep.UpdateMessageError, Community.parse,
                          value=b'\xff\xff\xff\x01\x01')
        try:
            Community.parse(value=b'\xff\xff\xff\x01\x01')
        except excep.UpdateMessageError as e:
            self.assertEqual(ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

    def test_construct(self):

        community = Community.construct(value=['NO_EXPORT'])
        self.assertEqual(b'\xc0\x08\x04\xff\xff\xff\x01', community)

        community = Community.construct(value=['NO_EXPORT', '4837:9929'])
        self.assertEqual(b'\xc0\x08\x08\xff\xff\xff\x01\x12\xe5&\xc9', community)

        community = Community.construct(value=['4837:1239', '4837:9929'])
        self.assertEqual(b'\xc0\x08\x08\x12\xe5\x04\xd7\x12\xe5&\xc9', community)

    def test_construct_invalid(self):
        self.assertRaises(excep.UpdateMessageError, Community.construct, value=['111:111', 'a:b'])

if __name__ == '__main__':
    unittest.main()
