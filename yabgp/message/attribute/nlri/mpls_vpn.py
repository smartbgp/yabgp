# Copyright 2016 Cisco Systems, Inc.
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

from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri import NLRI


class MPLSVPN(NLRI):
    """
    IPv4/IPv6 MPLS VPN NLRI
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
        Label Value-20 Bits
        Experimental bits-3 Bits
        Bottom of stack bit-1 bit
    c) Prefix: different coding way according to different SAFI
    Route Distinguisher (8 bytes) plus IPv4  prefix (32 bits) or IPv6 prefix(128 bits)
    rd (Route Distinguisher) structure (RFC 4364)
    """

    WITHDARW_LABEL_HEX = b'\x80\x00\x00'
    WITHDARW_LABEL = 524288
    AFI = None
    SAFI = None

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
            if cls.AFI == afn.AFNUM_INET and cls.SAFI == safn.SAFNUM_LAB_VPNUNICAST:
                if len(prefix) < 4:
                    prefix += b'\x00' * (4 - len(prefix))
                nlri_dict['prefix'] = str(netaddr.IPAddress(struct.unpack('!I', prefix)[0])) +\
                    '/%s' % (prefix_bit_len - 88)
            elif cls.AFI == afn.AFNUM_INET6 and cls.SAFI == safn.SAFNUM_LAB_VPNUNICAST:
                if len(prefix) < 16:
                    prefix += b'\x00' * (16 - len(prefix))
                nlri_dict['prefix'] = str(netaddr.IPAddress(int(binascii.b2a_hex(prefix), 16))) +\
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
            prefix_hex = b''
            if cls.AFI == afn.AFNUM_INET and cls.SAFI == safn.SAFNUM_LAB_VPNUNICAST:
                prefix_hex = cls.construct_prefix_v4(prefix_len, prefix_str)
            elif cls.AFI == afn.AFNUM_INET6 and cls.SAFI == safn.SAFNUM_LAB_VPNUNICAST:
                prefix_hex = cls.construct_prefix_v6(nlri['prefix'])
            prefix_hex = label_hex + rd_hex + prefix_hex
            prefix_len = struct.pack('!B', prefix_len + len(label_hex + rd_hex) * 8)
            nlri_bin += prefix_len + prefix_hex
        return nlri_bin

    @classmethod
    def parse_mpls_label_stack(cls, data):
        labels = []
        while len(data) >= 3:
            label = struct.unpack('!L', b'\00'+data[:3])[0]
            data = data[3:]
            labels.append(label >> 4)
            if label & 0x001:
                break
        return labels

    @classmethod
    def construct_mpls_label_stack(cls, labels):
        data = b''
        last_label = labels[-1]
        for label in labels[:-1]:
            data += struct.pack('!L', label << 4)[1:]
        if last_label != 0:
            data += struct.pack('!L', (last_label << 4 | 1))[1:]
        else:
            data += b'\x00\x00\x00'
        return data

    @classmethod
    def parse_rd(cls, data):
        """
        For Cisco: The BGP route distinguisher can be derived automatically
        from the VNI and BGP router ID of the VTEP switch
        :param data:
        :return:
        """
        rd_type = struct.unpack('!H', data[0:2])[0]
        rd_value = data[2:8]
        if rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_0:
            asn, an = struct.unpack('!HI', rd_value)
            rd = '%s:%s' % (asn, an)
        elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_1:
            ip = str(netaddr.IPAddress(struct.unpack('!I', rd_value[0:4])[0]))
            an = struct.unpack('!H', rd_value[4:6])[0]
            rd = '%s:%s' % (ip, an)
        elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_2:
            asn, an = struct.unpack('!IH', rd_value)
            rd = '%s:%s' % (asn, an)
        else:
            # fixme(by xiaopeng163) for other rd type process
            rd = str(rd_value)
        return rd

    @classmethod
    def construct_rd(cls, data):
        # fixme(by xiaopeng163) for other rd type process
        data = data.split(':')
        if '.' in data[0]:
            return struct.pack('!H', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_1) + netaddr.IPAddress(data[0]).packed + \
                struct.pack('!H', int(data[1]))
        else:
            data = [int(x) for x in data]
            if data[0] <= 0xffff:
                return struct.pack('!HHI', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_0, data[0], data[1])
            else:
                return struct.pack('!HIH', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_2, data[0], data[1])
