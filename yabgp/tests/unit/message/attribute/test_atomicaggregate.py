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

""" Test Atomic Aggregate attribute """

import unittest

from yabgp.common.exception import UpdateMessageError
from yabgp.common.constants import ERR_MSG_UPDATE_OPTIONAL_ATTR
from yabgp.message.attribute.atomicaggregate import AtomicAggregate


class TestAtomicAggregate(unittest.TestCase):

    def test_parse(self):

        atomicaggregate = AtomicAggregate.parse(value=b'')
        self.assertEqual(atomicaggregate, b'')

        # invalid value
        self.assertRaises(UpdateMessageError, AtomicAggregate.parse,
                          b'\x01')
        try:
            AtomicAggregate.parse(b'\x01')
        except UpdateMessageError as e:
            self.assertEqual(e.sub_error, ERR_MSG_UPDATE_OPTIONAL_ATTR)

    def test_construct(self):

        atomicaggregate = AtomicAggregate.construct(value=b'')
        self.assertEqual(b'\x40\x06\x00', atomicaggregate)

    def test_construct_exception(self):
        self.assertRaises(UpdateMessageError, AtomicAggregate.construct, b'\x00')

if __name__ == '__main__':
    unittest.main()
