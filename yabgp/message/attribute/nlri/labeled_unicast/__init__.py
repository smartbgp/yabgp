# Copyright 2015-2016 Cisco Systems, Inc.
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

import struct
import binascii

import netaddr

from yabgp.message.attribute.nlri import NLRI
from yabgp.common.afn import AFNUM_INET6, AFNUM_INET
from yabgp.common.safn import SAFNUM_MPLS_LABEL


class LabeledUnicast(NLRI):

    """
    +---------------------------+
    |   Length (1 octet)        |
    +---------------------------+
    |   Label (3 octets)        |
    +---------------------------+
    .............................
    +---------------------------+
    |   Prefix (variable)       |
    +---------------------------+
    """

    SAFI = SAFNUM_MPLS_LABEL

    @classmethod
    def parse(cls, nlri_data):
        nlri_list = []
        while nlri_data:
            nlri_bit_len = ord(nlri_data[0])
            # get the byte lenght of label stack + prefix
            if nlri_bit_len % 8 == 0:
                nlri_byte_len = nlri_bit_len / 8
            else:
                nlri_byte_len = nlri_bit_len / 8 + 1

            offset = nlri_byte_len + 1
            label = cls.parse_mpls_label_stack(nlri_data[1:])
            label_byte_len = len(label) * 3
            prefix_byte_len = nlri_byte_len - label_byte_len
            prefix_mask = nlri_bit_len - label_byte_len * 8
            if cls.AFI == AFNUM_INET:
                prefix_hex = nlri_data[offset - prefix_byte_len: offset] + (4 - prefix_byte_len) * '\x00'
                prefix_data = [ord(i) for i in prefix_hex]
                prefix_data = prefix_data
                prefix = "%s.%s.%s.%s" % (tuple(prefix_data[0:4])) + '/' + str(prefix_mask)
            elif cls.AFI == AFNUM_INET6:  # ipv6
                prefix_hex = nlri_data[offset - prefix_byte_len: offset]
                prefix = str(netaddr.IPAddress(int(binascii.b2a_hex(prefix_hex), 16))) + '/' + str(prefix_mask)
            nlri_data = nlri_data[offset:]
            nlri_list.append({'prefix': prefix, 'label': label})
        return nlri_list

    @classmethod
    def construct(cls, nlri_list):
        nlri_list_hex = b''
        for nlri in nlri_list:
            label_hex = cls.construct_mpls_label_stack(nlri['label'])
            if cls.AFI == AFNUM_INET:
                prefixstr, prefixlen = nlri['prefix'].split('/')
                prefixlen = int(prefixlen)
                prefix_hex = cls.construct_prefix_v4(prefixlen, prefixstr)
            elif cls.AFI == AFNUM_INET6:
                prefixlen = int(nlri['prefix'].split('/')[1])
                prefix_hex = cls.construct_prefix_v6(nlri['prefix'])
            nlri_list_hex += struct.pack('!B', 8 * len(label_hex) + prefixlen) + label_hex + prefix_hex
        return nlri_list_hex
