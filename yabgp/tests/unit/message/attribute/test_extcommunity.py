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
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RT_0, '100:12']], ext_community)

    def test_construct_rt0(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_0, '100:12')])
        self.assertEqual(b'\xc0\x10\x08\x00\x02\x00\x64\x00\x00\x00\x0c', ext_community)

    def test_parse_rt1(self):
        # Route Target,Format IPv4 address(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x01\x02\x0a\x0a\x0a\x0a\x00\x0c')
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RT_1, '10.10.10.10:12']], ext_community)

    def test_construct_rt1(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_1, '10.10.10.10:12')])
        self.assertEqual(b'\xc0\x10\x08\x01\x02\x0a\x0a\x0a\x0a\x00\x0c', ext_community)

    def test_parse_rt2(self):
        # Route Target,Format AS(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x02\x02\x00\x01\x00\x01\x00\x0c')
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RT_2, '65537:12']], ext_community)

    def test_construct_rt2(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RT_2, '65537:12')])
        self.assertEqual(b'\xc0\x10\x08\x02\x02\x00\x01\x00\x01\x00\x0c', ext_community)

    def test_parse_ro0(self):
        # Route Origin,Format AS(2bytes):AN(4bytes)
        ext_community = ExtCommunity.parse(value=b'\x00\x03\x00\x64\x00\x00\x00\x0c')
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RO_0, '100:12']], ext_community)

    def test_construct_ro0(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RO_0, '100:12')])
        self.assertEqual(b'\xc0\x10\x08\x00\x03\x00\x64\x00\x00\x00\x0c', ext_community)

    def test_parse_ro1(self):
        # Route Origin,Format IPv4 address(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x01\x03\x0a\x0a\x0a\x0a\x00\x0c')
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RO_1, '10.10.10.10:12']], ext_community)

    def test_construct_ro1(self):
        ext_community = ExtCommunity.construct(value=[(bgp_cons.BGP_EXT_COM_RO_1, '10.10.10.10:12')])
        self.assertEqual(b'\xc0\x10\x08\x01\x03\x0a\x0a\x0a\x0a\x00\x0c', ext_community)

    def test_parse_ro2(self):
        # Route Origin,Format AS(4bytes):AN(2bytes)
        ext_community = ExtCommunity.parse(value=b'\x02\x03\x00\x01\x00\x01\x00\x0c')
        self.assertEqual([[bgp_cons.BGP_EXT_COM_RO_2, '65537:12']], ext_community)

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

    def test_parse_construct_flowspec_redirect_vrf(self):
        community_list = [[bgp_cons.BGP_EXT_REDIRECT_VRF, '4837:100']]
        self.assertEqual(b'\xc0\x10\x08\x80\x08\x12\xe5\x00\x00\x00d', ExtCommunity.construct(value=community_list))
        community_hex = b'\x80\x08\x12\xe5\x00\x00\x00d'
        self.assertEqual(community_list, ExtCommunity.parse(value=community_hex))

    def test_parse_construct_flowspec_redirect_nh(self):
        community_list = [[bgp_cons.BGP_EXT_REDIRECT_NH, '0.0.0.0', 0]]
        self.assertEqual(b'\xc0\x10\x08\x08\x00\x00\x00\x00\x00\x00\x00', ExtCommunity.construct(value=community_list))
        self.assertEqual([[bgp_cons.BGP_EXT_REDIRECT_NH, '0.0.0.0', 0]],
                         ExtCommunity.parse(value=b'\x08\x00\x00\x00\x00\x00\x00\x00'))

    def test_parse_construct_tarffic_rate(self):
        community_list = [[bgp_cons.BGP_EXT_TRA_RATE, "100:6250000"]]
        self.assertEqual(b'\xc0\x10\x08\x80\x06\x00dJ\xbe\xbc ', ExtCommunity.construct(value=community_list))
        self.assertEqual([[bgp_cons.BGP_EXT_TRA_RATE, "100:6250000"]],
                         ExtCommunity.parse(value=b'\x80\x06\x00dJ\xbe\xbc '))

    def test_parse_construct_transitive_opaque_encap(self):
        community_list = [[bgp_cons.BGP_EXT_COM_ENCAP, 8]]
        community_hex = b'\x03\x0c\x00\x00\x00\x00\x00\x08'
        self.assertEqual(community_list, ExtCommunity.parse(community_hex))
        self.assertEqual(community_hex, ExtCommunity.construct(community_list)[3:])

    def test_parse_construct_es_import(self):
        community_list = [[bgp_cons.BGP_EXT_COM_EVPN_ES_IMPORT, '00-11-22-33-44-55']]
        community_hex = b'\x06\x02\x00\x11\x22\x33\x44\x55'
        self.assertEqual(community_list, ExtCommunity.parse(community_hex))
        self.assertEqual(community_hex, ExtCommunity.construct(community_list)[3:])

    def test_parse_construct_els_label(self):
        community_list = [[bgp_cons.BGP_EXT_COM_EVPN_ESI_MPLS_LABEL, 1, 20]]
        community_hex = b'\x06\x01\x01\x00\x00\x00\x01\x41'
        self.assertEqual(community_hex, ExtCommunity.construct(community_list)[3:])
        self.assertEqual(community_list, ExtCommunity.parse(community_hex))

    def test_parse_construct_mac_mobil(self):
        community_list = [[bgp_cons.BGP_EXT_COM_EVPN_MAC_MOBIL, 1, 500]]
        community_hex = b'\x06\x00\x01\x00\x00\x00\x01\xf4'
        self.assertEqual(community_hex, ExtCommunity.construct(community_list)[3:])
        self.assertEqual(community_list, ExtCommunity.parse(community_hex))

    def test_parse_construct_evpn_route_mac(self):
        comunity_list = [[1539, '74-A0-2F-DE-FE-FB']]
        community_hex = b'\x06\x03\x74\xa0\x2f\xde\xfe\xfb'
        self.assertEqual(comunity_list, ExtCommunity.parse(community_hex))
        self.assertEqual(community_hex, ExtCommunity.construct(comunity_list)[3:])

if __name__ == '__main__':
    unittest.main()
