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

"""IPv4 Flowspec NLRI
"""
import binascii
import math
import struct

import netaddr

from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri import NLRI


class IPv4FlowSpec(NLRI):
    @classmethod
    def parse(cls, value):
        """
        parse IPv4 flowspec NLRI
        :param value:
        :return:
        """
        # +------------------------------+
        # |    length (0xnn or 0xfn nn)  |
        # +------------------------------+
        # |    NLRI value  (variable)    |
        # +------------------------------+
        nlri_dict = {}
        while value:
            offset = 0
            flowspec_type = struct.unpack('!B', value[0])[0]
            offset += 1
            # decode all kinds of flow spec
            if flowspec_type in [bgp_cons.BGPNLRI_FSPEC_DST_PFIX, bgp_cons.BGPNLRI_FSPEC_SRC_PFIX]:
                prefix, offset_tmp = cls.parse_prefix(value[offset:])
                offset += offset_tmp
                nlri_dict[flowspec_type] = prefix
                value = value[offset:]
            elif flowspec_type in [bgp_cons.BGPNLRI_FSPEC_IP_PROTO, bgp_cons.BGPNLRI_FSPEC_DST_PORT,
                                   bgp_cons.BGPNLRI_FSPEC_SRC_PORT, bgp_cons.BGPNLRI_FSPEC_ICMP_TP,
                                   bgp_cons.BGPNLRI_FSPEC_ICMP_CD, bgp_cons.BGPNLRI_FSPEC_DSCP,
                                   bgp_cons.BGPNLRI_FSPEC_PCK_LEN]:
                operator_list, offset = cls.parse_operators(value[offset:])
                nlri_dict[flowspec_type] = operator_dict_to_str(operator_list)
                value = value[offset:]
            else:
                operator_list, offset = cls.parse_operators(value[offset:])
                nlri_dict[flowspec_type] = operator_dict_to_str(operator_list)
                value = value[offset:]
        return nlri_dict

    @classmethod
    def construct(cls, value):
        return cls.construct_nlri(value)

    @classmethod
    def construct_nlri(cls, data):
        """ Construct NLRI """
        # there may have many filters in each nlri
        data = dict([(int(l), r) for (l, r) in data.items()])
        nlri_tmp = b''
        for type_tmp in [bgp_cons.BGPNLRI_FSPEC_DST_PFIX, bgp_cons.BGPNLRI_FSPEC_SRC_PFIX]:
            if data.get(type_tmp):
                nlri_tmp += struct.pack('!B', type_tmp) + cls.construct_prefix(data[type_tmp])
        for type_tmp in [bgp_cons.BGPNLRI_FSPEC_IP_PROTO, bgp_cons.BGPNLRI_FSPEC_DST_PORT,
                         bgp_cons.BGPNLRI_FSPEC_SRC_PORT, bgp_cons.BGPNLRI_FSPEC_ICMP_TP,
                         bgp_cons.BGPNLRI_FSPEC_ICMP_CD, bgp_cons.BGPNLRI_FSPEC_PCK_LEN,
                         bgp_cons.BGPNLRI_FSPEC_DSCP]:
            if not data.get(type_tmp):
                continue

            # translate from expression to binary
            # expr = '>8080&<8088|=3128'
            if data[type_tmp] > 255:
                nlri_tmp += struct.pack('!B', type_tmp) + '\x91' + struct.pack('!H', data[type_tmp])
            else:
                nlri_tmp += struct.pack('!B', type_tmp) + '\x81' + struct.pack('!B', data[type_tmp])
                # TODO(penxiao) other flow type
        if len(nlri_tmp) >= 240:
            return struct.pack('!H', len(nlri_tmp)) + nlri_tmp
        elif nlri_tmp:
            return struct.pack('!B', len(nlri_tmp)) + nlri_tmp

    @staticmethod
    def parse_prefix(data):
        """
        Prefixes are encoded as in BGP UPDATE messages, a length in bits is followed by
        enough octets to contain the prefix information.

        Encoding: <prefix-length (1 octet), prefix>
        """
        prefix_len = struct.unpack('!B', data[0])[0]
        octet_len = int(math.ceil(prefix_len / 8.0))
        tmp = data[1:octet_len + 1]
        prefix_data = [ord(i) for i in tmp]
        prefix_data = prefix_data + list(str(0)) * 4
        prefix = "%s.%s.%s.%s" % (tuple(prefix_data[0:4])) + '/' + str(prefix_len)
        return prefix, octet_len + 1

    @classmethod
    def construct_prefix(cls, prefix):
        """
        construct a prefix string from '1.1.1.0/24' to '\x18\x01\x01\x01'
        """
        ip, masklen = prefix.split('/')
        ip_hex = netaddr.IPAddress(ip).packed
        masklen = int(masklen)
        if 16 < masklen <= 24:
            ip_hex = ip_hex[0:3]
        elif 8 < masklen <= 16:
            ip_hex = ip_hex[0:2]
        elif 0 < masklen <= 8:
            ip_hex = ip_hex[0:1]
        elif masklen == 0:
            ip_hex = ''
        return struct.pack('!B', masklen) + ip_hex

    @staticmethod
    def parse_operators(data):
        offset = 0
        parse_operator_list = []
        while data:
            operator = parse_operator(struct.unpack('!B', data[0])[0])
            offset += 1
            operator_value = int(binascii.b2a_hex(data[1:1 + operator['LEN']]), 16)
            offset += operator['LEN']
            parse_operator_list.append([operator, operator_value])
            # the end of the list
            data = data[1 + operator['LEN']:]
            if operator['EOL']:
                break
        return parse_operator_list, offset + 1


def parse_operator(data):
    """
    The operator byte is encoded as:
      0    1   2   3   4  5   6   7
    +---+---+---+---+---+---+---+---+
    |EOL|AND|  LEN  |RES|LT |GT |EQ |
    +---+---+---+---+---+---+---+---+
    """
    bit_list = []
    for i in xrange(8):
        bit_list.append((data >> i) & 1)
    bit_list.reverse()
    result = {
        'EOL': bit_list[0],
        'AND': bit_list[1],
        'LEN': 1 << (bit_list[2] * 2 + bit_list[3]),
        'LT': bit_list[5],
        'GT': bit_list[6],
        'EQ': bit_list[7]
    }
    return result


def operator_dict_to_str(data):
    """

    from
    [
        [
            {'AND': 0, 'GT': 0, 'LEN': 1, 'EOL': 0, 'LT': 0, 'EQ': 1},
            254
        ],
        [
            {'AND': 0, 'GT': 1, 'LEN': 1, 'EOL': 0, 'LT': 0, 'EQ': 1},
            254
        ],
        [
            {'AND': 1, 'GT': 0, 'LEN': 2, 'EOL': 1, 'LT': 1, 'EQ': 1},
            300
        ]
    ]
    to
    =254 >=254&<=300
    :param data: dict
    :return: string format
    """
    return_str = ''
    for item in data:
        operator_dict, value = item
        if operator_dict['AND']:
            return_str += '&'
        else:
            if return_str != '':
                return_str += ' '
        if operator_dict['GT']:
            return_str += '>'
        if operator_dict['LT']:
            return_str += '<'
        if operator_dict['EQ']:
            return_str += '='
        return_str += str(value)
    return return_str


def operator_str_dict(data):
    """
    from =254 >=254&<=300 to dict
    :param data:
    :return:
    """
    # operator_list = []
    # pattern1 = re.compile('^(\D+)(\d+)(&)(\D+)(\d+)$')
    # pattern2 = re.compile('^(\D+)(\d+)$')
    #
    # operator = data.strip().split(' ')
    #
    # for item in operator:
    #     first_match = pattern1.match(item)
    #     if first_match:
    #         print first_match.group(1, 2, 3, 4, 5)
    #     second_match = pattern2.match(item)
    #     if second_match:
    #         operator_type, value = second_match.group(1, 2)
    #         if operator_type == '=':
    #             pass
