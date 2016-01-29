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

import netaddr

from yabgp.message.attribute.nlri import NLRI
from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN

LOG = logging.getLogger(__name__)


class IPv4MPLSVPN(MPLSVPN, NLRI):

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
    def parse(cls, value, iswithdraw=False):
        """
        parse nlri
        :param value: the raw hex nlri value
        :param iswithdraw: if this is parsing withdraw
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

            if not iswithdraw:
                nlri_dict['label'] = cls.parse_mpls_label_stack(value[1:])
            else:
                nlri_dict['label'] = [MPLSVPN.WITHDARW_LABEL]

            nlri_dict['rd'] = MPLSVPN.parse_rd(value[4:12])
            prefix = value[12:prefix_byte_len + 1]
            if len(prefix) < 4:
                prefix += b'\x00' * (4 - len(prefix))
            nlri_dict['prefix'] = str(netaddr.IPAddress(struct.unpack('!I', prefix)[0])) +\
                '/%s' % (prefix_bit_len - 88)
            value = value[prefix_byte_len + 1:]
            nlri_list.append(nlri_dict)
        return nlri_list

    @classmethod
    def construct(cls, value, iswithdraw=False):
        nlri_bin = b''
        for nlri in value:
            # construct label
            if iswithdraw:
                label_hex = MPLSVPN.WITHDARW_LABEL_HEX
            else:
                label_hex = MPLSVPN.construct_mpls_label_stack(nlri['label'])
            # construct rd
            rd_hex = MPLSVPN.construct_rd(nlri['rd'])
            # construct prefix
            prefix_str, prefix_len = nlri['prefix'].split('/')
            prefix_len = int(prefix_len)
            prefix_hex = cls.construct_prefix_v4(prefix_len, prefix_str)
            prefix_hex = label_hex + rd_hex + prefix_hex

            prefix_len = struct.pack('!B', prefix_len + len(label_hex + rd_hex) * 8)
            nlri_bin += prefix_len + prefix_hex
        return nlri_bin
