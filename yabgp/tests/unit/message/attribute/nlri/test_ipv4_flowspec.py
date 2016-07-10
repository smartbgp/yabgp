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

import unittest

from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri.ipv4_flowspec import IPv4FlowSpec


class TestIPv4FlowSpec(unittest.TestCase):

    def test_parse(self):
        pass
        raw_hex = '\x01\x18\x02\x02\x02\x02\x10\x03\x03\x03\x01\x00\x01\x2f\x01\x58' \
                  '\x01\x01\x01\x02\x01\x59\x81\x67\x05\x11\x1f\x92\x91\x1f\x93\x06\x01' \
                  '\x50\x11\x1f\x90\x11\x1f\x91\x11\x1f\x92\x91\x1f\x93\x07\x01\x02\x01' \
                  '\x03\x01\x05\x81\x06\x08\x81\x02\x09\x81\x28\x0a\x01\xfe\x03\xfe\xd5' \
                  '\x01\x2c\x0b\x01\x28\x81\x30\x0c\x81\x01'
        self.assertEqual(
            {1: '2.2.2.0/24', 2: '3.3.0.0/16', 3: '=0 =47 =88 =1 =2 =89 =103', 5: '=8082 =8083',
             6: '=80 =8080 =8081 =8082 =8083', 7: '=2 =3 =5 =6', 8: '=2', 9: '=40', 10: '=254 >=254&<=300',
             11: '=40 =48', 12: '=1'}, IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_prefix(self):
        raw_hex = b'\x01\x18\x6e\x01\x01'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_DST_PFIX: '110.1.1.0/24'}, IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_packet_length(self):
        raw_hex = '\x0a\x01\xfe\x03\xfe\xd5\x01\x2c'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_PCK_LEN: '=254 >=254&<=300'}, IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_ip_protocol(self):
        raw_hex = '\x03\x01\x00\x01\x2f\x01\x58\x01\x01\x01\x02\x01\x59\x81\x67'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_IP_PROTO: '=0 =47 =88 =1 =2 =89 =103'}, IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_des_port(self):
        raw_hex = '\x05\x01\x50\x11\x1f\x90\x11\x1f\x91\x11\x1f\x92\x91\x1f\x93'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_DST_PORT: '=80 =8080 =8081 =8082 =8083'},
                         IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_src_port(self):
        raw_hex = '\x06\x01\x50\x11\x1f\x90\x11\x1f\x91\x11\x1f\x92\x91\x1f\x93'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_SRC_PORT: '=80 =8080 =8081 =8082 =8083'},
                         IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_icmp_type(self):
        raw_hex = '\x07\x01\x02\x01\x03\x01\x05\x81\x06'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_ICMP_TP: '=2 =3 =5 =6'}, IPv4FlowSpec.parse(raw_hex))

    def test_parse_nlri_icmp_code(self):
        raw_hex = '\x08\x81\x02'
        self.assertEqual({bgp_cons.BGPNLRI_FSPEC_ICMP_CD: '=2'}, IPv4FlowSpec.parse(raw_hex))

    def test_construct_prefix(self):
        prefix_bin = b'\x18\xc0\x55\x02'
        prefix_str = '192.85.2.0/24'
        self.assertEqual(prefix_bin, IPv4FlowSpec.construct_prefix(prefix_str))

    def test_construct_nlri(self):
        nlri_bin = b'\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        nlri_list = {1: '192.85.2.0/24', 2: '192.85.1.0/24'}
        self.assertEqual(nlri_bin, IPv4FlowSpec.construct_nlri(nlri_list))


if __name__ == '__main__':
    unittest.main()
