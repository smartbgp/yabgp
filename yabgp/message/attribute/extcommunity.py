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

"""BGP extended community
"""

import struct
import logging
import binascii

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeID
from yabgp.message.attribute import AttributeFlag
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons

LOG = logging.getLogger()


class ExtCommunity(Attribute):
    """
        The Extended Communities Attribute is a transitive optional BGP
    attribute, with the Type Code 16. The attribute consists of a set of
    "extended communities". All routes with the Extended Communities
    attribute belong to the communities listed in the attribute.
    (RFC 4360 Page2)
    http://www.iana.org/assignments/bgp-extended-communities
    """

    # Extended Community Type
    # IANA    0x0000 - 0x7fff
    # private 0x8000 - 0xffff

    ID = AttributeID.EXTENDED_COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value):

        """
        Each Extended Community is encoded as an 8-octet quantity, as
        follows:
        - Type Field : 1 or 2 octets
        - Value Field : Remaining octets
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Type high | Type low(*) |                                     |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ Value                         |
        |                                                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        Parse Extended Community attributes.
        :param value : value
        """
        # devide every ext community
        if len(value) % 8 != 0:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)

        ext_community = []
        while value:
            comm_type, subtype = struct.unpack('!BB', value[0:2])
            value_tmp = value[2:8]

            comm_code = comm_type * 256 + subtype

            # Route Target
            if comm_code == bgp_cons.BGP_EXT_COM_RT_0:
                # Route Target, Format AS(2bytes):AN(4bytes)
                asn, an = struct.unpack('!HI', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_COM_RT_0, '%s:%s' % (asn, an)])

            elif comm_code == bgp_cons.BGP_EXT_COM_RT_1:
                # Route Target,Format IPv4 address(4bytes):AN(2bytes)
                ipv4 = str(netaddr.IPAddress(struct.unpack('!I', value_tmp[0:4])[0]))
                an = struct.unpack('!H', value_tmp[4:])[0]
                ext_community.append([bgp_cons.BGP_EXT_COM_RT_1, '%s:%s' % (ipv4, an)])

            elif comm_code == bgp_cons.BGP_EXT_COM_RT_2:
                # Route Target,Format AS(4bytes):AN(2bytes)
                asn, an = struct.unpack('!IH', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_COM_RT_2, '%s:%s' % (asn, an)])

            # Route Origin
            elif comm_code == bgp_cons.BGP_EXT_COM_RO_0:
                # Route Origin,Format AS(2bytes):AN(4bytes)
                asn, an = struct.unpack('!HI', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_COM_RO_0, '%s:%s' % (asn, an)])

            elif comm_code == bgp_cons.BGP_EXT_COM_RO_1:
                # Route Origin,Format IP address:AN(2bytes)
                ipv4 = str(netaddr.IPAddress(struct.unpack('!I', value_tmp[0:4])[0]))
                an = struct.unpack('!H', value_tmp[4:])[0]
                ext_community.append([bgp_cons.BGP_EXT_COM_RO_1, '%s:%s' % (ipv4, an)])

            elif comm_code == bgp_cons.BGP_EXT_COM_RO_2:
                # Route Origin,Format AS(2bytes):AN(4bytes)
                asn, an = struct.unpack('!IH', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_COM_RO_2, '%s:%s' % (asn, an)])

            # BGP Flow spec
            elif comm_code == bgp_cons.BGP_EXT_REDIRECT_NH:
                ipv4 = str(netaddr.IPAddress(int(binascii.b2a_hex(value_tmp[0:4]), 16)))
                copy_flag = struct.unpack('!H', value_tmp[4:])[0]
                ext_community.append([bgp_cons.BGP_EXT_REDIRECT_NH, ipv4, copy_flag])
            elif comm_code == bgp_cons.BGP_EXT_TRA_RATE:
                asn, rate = struct.unpack('!Hf', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_TRA_RATE, '%s:%s' % (asn, int(rate))])

            elif comm_code == bgp_cons.BGP_EXT_TRA_ACTION:
                bit_value = parse_bit(value_tmp[-1])
                ext_community.append([bgp_cons.BGP_EXT_TRA_ACTION, {'S': bit_value['6'], 'T': bit_value['7']}])
            elif comm_code == bgp_cons.BGP_EXT_REDIRECT_VRF:
                asn, an = struct.unpack('!HI', value_tmp)
                ext_community.append([bgp_cons.BGP_EXT_REDIRECT_VRF, '%s:%s' % (asn, an)])
            elif comm_code == bgp_cons.BGP_EXT_TRA_MARK:
                mark = struct.unpack('!B', value_tmp[-1])[0]
                ext_community.append([bgp_cons.BGP_EXT_TRA_MARK, mark])

            # Transitive Opaque
            elif comm_code == bgp_cons.BGP_EXT_COM_ENCAP:
                ext_community.append([bgp_cons.BGP_EXT_COM_ENCAP, struct.unpack('!I', value_tmp[2:])[0]])
            # EVPN
            elif comm_code == bgp_cons.BGP_EXT_COM_EVPN_ES_IMPORT:
                mac = str(netaddr.EUI(int(binascii.b2a_hex(value_tmp), 16)))
                ext_community.append([comm_code, mac])
            elif comm_code == bgp_cons.BGP_EXT_COM_EVPN_MAC_MOBIL:
                flag = ord(value_tmp[0:1])
                seq = struct.unpack('!I', value_tmp[2:])[0]
                ext_community.append([comm_code, flag, seq])
            elif comm_code == bgp_cons.BGP_EXT_COM_EVPN_ESI_MPLS_LABEL:
                flag = ord(value_tmp[0:1])
                label = struct.unpack('!L', b'\00'+value_tmp[3:])[0]
                label >>= 4
                ext_community.append([comm_code, flag, label])
            elif comm_code == bgp_cons.BGP_EXT_COM_EVPN_ROUTE_MAC:
                ext_community.append([comm_code, str(netaddr.EUI(int(binascii.b2a_hex(value_tmp), 16)))])
            else:
                ext_community.append([bgp_cons.BGP_EXT_COM_UNKNOW, repr(value_tmp)])
                LOG.warn('unknow bgp extended community, type=%s, value=%s', comm_code, repr(value_tmp))

            value = value[8:]

        return ext_community

    @classmethod
    def construct(cls, value):

        """
        Construct Extended Community attributes.
        :param value: value list like [('RT':4837:9929),('RT': 1239:9929)]
        """
        ext_community_hex = b''
        for item in value:
            # for Route Target
            if item[0] == bgp_cons.BGP_EXT_COM_RT_0:
                # Route Target, Format AS(2bytes):AN(4bytes)
                asn, an = item[1].split(':')
                ext_community_hex += struct.pack('!HHI', bgp_cons.BGP_EXT_COM_RT_0, int(asn), int(an))
            elif item[0] == bgp_cons.BGP_EXT_COM_RT_1:
                ip, an = item[1].split(':')
                ext_community_hex += struct.pack('!H', bgp_cons.BGP_EXT_COM_RT_1) + netaddr.IPAddress(ip).packed + \
                    struct.pack('!H', int(an))
            elif item[0] == bgp_cons.BGP_EXT_COM_RT_2:
                asn, an = item[1].split(':')
                ext_community_hex += struct.pack('!HIH', bgp_cons.BGP_EXT_COM_RT_2, int(asn), int(an))

            # for Route Origin
            elif item[0] == bgp_cons.BGP_EXT_COM_RO_0:
                asn, an = item[1].split(':')
                ext_community_hex += struct.pack('!HHI', bgp_cons.BGP_EXT_COM_RO_0, int(asn), int(an))
            elif item[0] == bgp_cons.BGP_EXT_COM_RO_1:
                ip, an = item[1].split(':')
                ext_community_hex += struct.pack('!H', bgp_cons.BGP_EXT_COM_RO_1) + netaddr.IPAddress(ip).packed + \
                    struct.pack('!H', int(an))
            elif item[0] == bgp_cons.BGP_EXT_COM_RO_2:
                asn, an = item[1].split(':')
                ext_community_hex += struct.pack('!HIH', bgp_cons.BGP_EXT_COM_RO_2, int(asn), int(an))

            # for bgp flow spec
            elif item[0] == bgp_cons.BGP_EXT_REDIRECT_VRF:
                asn, an = item[1].split(':')
                ext_community_hex += struct.pack('!HHI', bgp_cons.BGP_EXT_REDIRECT_VRF, int(asn), int(an))
            elif item[0] == bgp_cons.BGP_EXT_REDIRECT_NH:
                nexthop = netaddr.IPAddress(item[1]).packed
                copy_flag = struct.pack('!H', item[2])
                type_hex = struct.pack('!H', bgp_cons.BGP_EXT_REDIRECT_NH)
                com_hex = type_hex + nexthop + copy_flag
                ext_community_hex += com_hex
            elif item[0] == bgp_cons.BGP_EXT_TRA_MARK:
                ext_community_hex += struct.pack('!HIBB', bgp_cons.BGP_EXT_TRA_MARK, 0, 0, item[1])
            elif item[0] == bgp_cons.BGP_EXT_TRA_RATE:
                asn, rate = item[1].split(':')
                ext_community_hex += struct.pack('!HHf', bgp_cons.BGP_EXT_TRA_RATE, int(asn), int(rate))

            # Transitive Opaque
            elif item[0] == bgp_cons.BGP_EXT_COM_ENCAP:
                ext_community_hex += struct.pack('!HHI', bgp_cons.BGP_EXT_COM_ENCAP, 0, item[1])
            # EVPN
            elif item[0] == bgp_cons.BGP_EXT_COM_EVPN_ES_IMPORT:
                mac = b''.join([struct.pack('!B', (int(i, 16))) for i in item[1].split("-")])
                ext_community_hex += struct.pack('!H', item[0]) + mac
            elif item[0] == bgp_cons.BGP_EXT_COM_EVPN_ESI_MPLS_LABEL:
                flag = struct.pack('!B', item[1])
                label = struct.pack('!L', (item[2] << 4 | 1))[1:]
                ext_community_hex += struct.pack('!H', item[0]) + flag + b'\x00\x00' + label
            elif item[0] == bgp_cons.BGP_EXT_COM_EVPN_MAC_MOBIL:
                flag = struct.pack('!B', item[1])
                seq = struct.pack('!I', item[2])
                ext_community_hex += struct.pack('!H', item[0]) + flag + b'\x00' + seq
            elif item[0] == bgp_cons.BGP_EXT_COM_EVPN_ROUTE_MAC:
                ext_community_hex += struct.pack('!H', item[0]) + \
                    b''.join([struct.pack('!B', (int(i, 16))) for i in item[1].split("-")])
            else:
                LOG.warn('unknow bgp extended community for construct, type=%s, value=%s', item[0], item[1])

        if ext_community_hex:
            return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', len(ext_community_hex)) + ext_community_hex
        else:
            LOG.error('construct error, value=%s' % value)
            return None


def parse_bit(data):
    """
    The operator byte is encoded as:
      0    1   2   3   4  5   6   7
    +---+---+---+---+---+---+---+---+
    | e | a |  len  | 0 |lt |gt |eq |
    +---+---+---+---+---+---+---+---+
    """
    bit_list = []
    for i in xrange(8):
        bit_list.append((data >> i) & 1)
    bit_list.reverse()
    result = {
        '0': bit_list[0],
        '1': bit_list[1],
        '2': bit_list[2],
        '3': bit_list[3],
        '4': bit_list[4],
        '5': bit_list[5],
        '6': bit_list[6],
        '7': bit_list[7]
    }
    return result
