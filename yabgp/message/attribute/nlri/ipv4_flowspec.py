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
    """ipv4 flow nlri process
    """

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
            flowspec_type = ord(value[0:1])
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
                nlri_dict[flowspec_type] = cls.operator_dict_to_str(operator_list)
                value = value[offset:]
            else:
                operator_list, offset = cls.parse_operators(value[offset:])
                nlri_dict[flowspec_type] = cls.operator_dict_to_str(operator_list)
                value = value[offset:]
        return nlri_dict

    @classmethod
    def construct(cls, value):
        nlri_hex = b''
        for nlri in value:
            nlri_hex += cls.construct_nlri(nlri)
        return nlri_hex

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
            nlri_tmp += struct.pack('!B', type_tmp) + cls.construct_operators(data[type_tmp])

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
        prefix_len = ord(data[0:1])
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

    @classmethod
    def parse_operators(cls, data):
        offset = 0
        parse_operator_list = []
        while data:
            operator = cls.parse_operator_flag(ord(data[0:1]))
            offset += 1
            operator_value = int(binascii.b2a_hex(data[1:1 + operator['LEN']]), 16)
            offset += operator['LEN']
            parse_operator_list.append([operator, operator_value])
            # the end of the list
            data = data[1 + operator['LEN']:]
            if operator['EOL']:
                break
        return parse_operator_list, offset + 1

    @staticmethod
    def parse_operator_flag(data):
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

    @staticmethod
    def construct_operator_flag(data):
        """construct operator flag from dict to binary
        """
        opt_dict = {
            'EOL': 0x80,
            'AND': 0x40,
            'LEN': {
                1: 0x00,
                2: 0x10,
                4: 0x20,
                6: 0x30
            },
            'RES': 0x00,
            'LT': 0x04,
            'GT': 0x02,
            'EQ': 0x01
        }
        b_data = 0x00
        for opt in opt_dict:
            if opt in data and opt != 'LEN':
                if data[opt] == 1:
                    b_data += opt_dict[opt]
            elif opt == 'LEN' and data[opt]:
                b_data += opt_dict['LEN'][data['LEN']]
        return b_data

    @staticmethod
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
        =254|>=254&<=300
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
                    return_str += '|'
            if operator_dict['GT']:
                return_str += '>'
            if operator_dict['LT']:
                return_str += '<'
            if operator_dict['EQ']:
                return_str += '='
            return_str += str(value)
        return return_str

    @classmethod
    def construct_operators(cls, data):
        """
        from "=254|>=254&<=300" to binary data
        :param data:
        :return:
        """
        data_bin = b''
        data_list = data.split('|')
        eol = 0
        for i, data in enumerate(data_list):
            if i == len(data_list) - 1:
                eol = 1
            if '&' not in data:
                flag_dict = {'EOL': eol}
                if data[0] == '=':
                    off_set = 1
                    flag_dict['EQ'] = 1
                elif '>=' in data:
                    off_set = 2
                    flag_dict['EQ'] = 1
                    flag_dict['GT'] = 1
                elif '<=' in data:
                    off_set = 2
                    flag_dict['EQ'] = 1
                    flag_dict['LT'] = 1
                elif '>' in data:
                    off_set = 1
                    flag_dict['GT'] = 1
                elif '<' in data:
                    off_set = 1
                    # value_hex = str(bytearray.fromhex(hex(int(data[2:]))[2:]))
                    flag_dict['LT'] = 1
                hex_str = hex(int(data[off_set:]))[2:]
                if len(hex_str) == 1:
                    hex_str = '0' + hex_str
                value_hex = str(bytearray.fromhex(hex_str))
                flag_dict['LEN'] = len(value_hex)
                opt_flag_bin = cls.construct_operator_flag(flag_dict)
                data_bin += struct.pack('!B', opt_flag_bin)
                data_bin += value_hex

        return data_bin
