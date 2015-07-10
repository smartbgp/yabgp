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

""" Test extended Community attribute """

import unittest

from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep
from yabgp.message.attribute.extcommunity import ExtCommunity


class TestExtCommunity(unittest.TestCase):

    def test_parse_rt0(self):
        # Route Target,Format AS(2bytes):AN(4bytes)
        ext_community = ExtCommunity.parse(value=b'\x00\x02\x00\x64\x00\x00\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RT_0, '100:12')], ext_community)

    def test_construct_rt0(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_0, '100:12')])
        self.assertEqual(b'\xc0\x10\x08\x00\x02\x00\x64\x00\x00\x00\x0c', ext_community)

    def test_parse_rt1(self):
        # Route Target,Format IPv4 address(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x01\x02\x0a\x0a\x0a\x0a\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RT_1, '10.10.10.10:12')], ext_community)

    def test_construct_rt1(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_1, '10.10.10.10:12')])
        self.assertEqual(b'\xc0\x10\x08\x01\x02\x0a\x0a\x0a\x0a\x00\x0c', ext_community)

    def test_parse_rt2(self):
        # Route Target,Format AS(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x02\x02\x00\x01\x00\x01\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RT_2, '65537:12')], ext_community)

    def test_construct_rt2(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_2, '65537:12')])
        self.assertEqual(b'\xc0\x10\x08\x02\x02\x00\x01\x00\x01\x00\x0c', ext_community)

    def test_parse_ro0(self):
        # Route Origin,Format AS(2bytes):AN(4bytes)
        ext_community = ExtCommunity.parse(value=b'\x00\x03\x00\x64\x00\x00\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RO_0, '100:12')], ext_community)

    def test_construct_ro0(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RO_0, '100:12')])
        self.assertEqual(b'\xc0\x10\x08\x00\x03\x00\x64\x00\x00\x00\x0c', ext_community)

    def test_parse_ro1(self):
        # Route Origin,Format IPv4 address(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x01\x03\x0a\x0a\x0a\x0a\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RO_1, '10.10.10.10:12')], ext_community)

    def test_construct_ro1(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RO_1, '10.10.10.10:12')])
        self.assertEqual(b'\xc0\x10\x08\x01\x03\x0a\x0a\x0a\x0a\x00\x0c', ext_community)

    def test_parse_ro2(self):
        # Route Origin,Format AS(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x02\x03\x00\x01\x00\x01\x00\x0c')
        self.assertEqual([(bgp_cons.BGP_EXT_COM_RO_2, '65537:12')], ext_community)

    def test_construct_ro2(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RO_2, '65537:12')])
        self.assertEqual(b'\xc0\x10\x08\x02\x03\x00\x01\x00\x01\x00\x0c', ext_community)

    def test_parse_invalid_length(self):
        # invalid length
        self.assertRaises(excep.UpdateMessageError, ExtCommunity.parse,
                          b'\x00\x00\x02\x00\x64\x00\x00\x00\x0c')
        try:
            ExtCommunity.parse(value=b'\x00\x00\x02\x00\x64\x00\x00\x00\x0c')
        except excep.UpdateMessageError as e:
            self.assertEqual(bgp_cons.ERR_MSG_UPDATE_ATTR_LEN, e.sub_error)

    def test_parse_unknow(self):
        # unknow
        hex_tmp = b'\x09\x03\x00\x01\x00\x01\x00\x0c'
        ext_community = ExtCommunity.parse(value=hex_tmp)
        self.assertEqual(bgp_cons.BGP_EXT_COM_UNKNOW, ext_community[0][0])

if __name__ == '__main__':
    unittest.main()
