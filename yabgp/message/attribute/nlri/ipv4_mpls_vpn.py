# coding=utf-8
# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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

"""IPv4 MPLS VPN NLRI
"""

import struct
import logging
import binascii

import netaddr

from yabgp.common import constants as bgp_cons

LOG = logging.getLogger(__name__)


class IPv4MPLSVPN(object):

    """
    IPv4 MPLS VPN NLRI

    +---------------------------+
    | Length (1 octet)          |
    +---------------------------+
    | Label  (3 octet)          |
    +---------------------------+
    |...........................|
    +---------------------------+
    | Prefix (variable)         |
    +---------------------------+
    a) Length: The Length field indicates the length, in bits, of the address prefix.
    b) Label: (24 bits) Carries one or more labels in a stack, although a BGP update
    has only one label. This field carries the following parts of the MPLS shim header:
        Label Value–—20 Bits
        Experimental bits—3 Bits
        Bottom of stack bit—1 bit
    c) Prefix: different coding way according to different SAFI
    Route Distinguisher (8 bytes) plus IPv4  prefix (32 bits) or IPv6 prefix(128 bits)
    rd (Route Distinguisher) structure (RFC 4364)
    """

    @classmethod
    def parse(cls, value):
        """
        parse nlri
        :param value: the raw hex nlri value
        :return: nlri list
        """
        nlri_list = []
        while value:
            nlri_dict = {}
            # for python2 and python3
            if isinstance(value[0], int):
                prefix_bit_len = value[0]
            else:
                prefix_bit_len = ord(value[0])
            if prefix_bit_len % 8 == 0:
                prefix_byte_len = int(prefix_bit_len / 8)
            else:
                prefix_byte_len = int(prefix_bit_len / 8) + 1

            label_int = int(binascii.b2a_hex(value[1:4]), 16)
            nlri_dict['label'] = (label_int >> 4, label_int & 1)

            rd = value[4:12]
            rd_type = struct.unpack('!H', rd[0:2])[0]
            rd_value = rd[2:8]
            nlri_dict['rd_type'] = rd_type
            if rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_0:
                asn, an = struct.unpack('!HI', rd_value)
                nlri_dict['rd'] = '%s:%s' % (asn, an)
            elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_1:
                ip = str(netaddr.IPAddress(struct.unpack('!I', rd_value[0:4])[0]))
                an = struct.unpack('!H', rd_value[4:6])[0]
                nlri_dict['rd'] = '%s:%s' % (ip, an)
            elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_2:
                asn, an = struct.unpack('!IH', rd_value)
                nlri_dict['rd'] = '%s:%s' % (asn, an)
            else:
                LOG.warning('unknow rd type for nlri, type=%s' % rd_type)
                nlri_dict['rd'] = '%s:%s' % (0, 0)
            prefix = value[12:prefix_byte_len + 1]
            if len(prefix) < 4:
                prefix += '\x00' * (4 - len(prefix))
            nlri_dict['str'] = str(netaddr.IPAddress(struct.unpack('!I', prefix)[0])) +\
                '/%s' % (prefix_bit_len - 88)
            value = value[prefix_byte_len + 1:]
            nlri_list.append(nlri_dict)
        return nlri_list

    @classmethod
    def contruct(cls, value):
        pass
