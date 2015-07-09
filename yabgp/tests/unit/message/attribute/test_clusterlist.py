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

""" Test Cluster List attribute """

import unittest

from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.common import exception as excep
from yabgp.message.attribute.clusterlist import ClusterList


class TestClusterList(unittest.TestCase):

    def test_parse(self):

        cluster_list = ClusterList.parse(value=b'\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x03')
        self.assertEqual(['1.1.1.1', '2.2.2.2', '3.3.3.3'], cluster_list)

    def test_parse_invalid_length(self):
        # invalid length
        self.assertRaises(excep.UpdateMessageError, ClusterList.parse,
                          b'\x01\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x03')
        try:
            ClusterList.parse(value=b'\x01\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x03')
        except excep.UpdateMessageError as e:
            self.assertEqual(ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

    def test_construct(self):

        cluster_list = ClusterList.construct(value=['1.1.1.1', '2.2.2.2', '3.3.3.3'])
        self.assertEqual(b'\x80\n\x0c\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x03', cluster_list)

    def test_construct_invalid_length(self):
        # invalid length
        self.assertRaises(excep.UpdateMessageError, ClusterList.construct,
                          ['a', 2, '3'])

if __name__ == '__main__':
    unittest.main()
