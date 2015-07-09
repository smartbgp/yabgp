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

""" Test Aggregator attribute """

import unittest

from yabgp.common import exception as excep
from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.message.attribute.aggregator import Aggregator


class TestAggregator(unittest.TestCase):
    def test_parse(self):

        # 4 bytes asn
        aggregator = Aggregator.parse(value=b'\x00\x00\x70\xd5\x3e\xe7\xff\x79',
                                      asn4=True)
        self.assertEqual((28885, '62.231.255.121'), aggregator)

        # 2 bytes asn
        aggregator = Aggregator.parse(value=b'\x70\xd5\x3e\xe7\xff\x79',
                                      asn4=False)
        self.assertEqual((28885, '62.231.255.121'), aggregator)

        # invalid attr len
        self.assertRaises(excep.UpdateMessageError, Aggregator.parse,
                          b'\x70\xd5\x3e\xe7\xff\x79',
                          True)
        try:
            Aggregator.parse(value=b'\x70\xd5\x3e\xe7\xff\x79',
                             asn4=True)
        except excep.UpdateMessageError as e:
            self.assertEqual(ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

    def test_construct(self):

        aggregator = Aggregator.construct(value=(28885, '62.231.255.121'))
        self.assertEqual(b'\xc0\x07\x06\x70\xd5\x3e\xe7\xff\x79', aggregator)


if __name__ == '__main__':
    unittest.main()
