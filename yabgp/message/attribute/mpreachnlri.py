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

"""BGP Attribute MP_REACH_NLRI
"""

import struct
import binascii

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri.ipv4_mpls_vpn import IPv4MPLSVPN
from yabgp.message.attribute.nlri.ipv6_mpls_vpn import IPv6MPLSVPN
from yabgp.message.attribute.nlri.ipv4_flowspec import IPv4FlowSpec
from yabgp.message.attribute.nlri.ipv6_unicast import IPv6Unicast
from yabgp.message.attribute.nlri.evpn import EVPN


class MpReachNLRI(Attribute):
    """
        MP_REACH_NLRI (type code 14) is used to carry the set of reachable
    destinations together with the next hop information to be used for
    forwarding to these destinations (RFC 4760 page 2).

        MP_REACH_NLRI coding information
        +---------------------------------------------------------+
        | Address Family Identifier (2 octets)                    |
        +---------------------------------------------------------+
        | Subsequent Address Family Identifier (1 octet)          |
        +---------------------------------------------------------+
        | Length of Next Hop Network Address (1 octet)            |
        +---------------------------------------------------------+
        | Network Address of Next Hop (variable)                  |
        +---------------------------------------------------------+
        | Reserved (1 octet)                                      |
        +---------------------------------------------------------+
        | Network Layer Reachability Information (variable)       |
        +---------------------------------------------------------+
    """

    ID = AttributeID.MP_REACH_NLRI
    FLAG = AttributeFlag.OPTIONAL

    @classmethod
    def parse(cls, value):

        try:
            afi, safi, nexthop_length = struct.unpack('!HBB', value[0:4])
            nexthop_bin = value[4:4 + nexthop_length]
            nlri_bin = value[5 + nexthop_length:]
        except Exception:
            # error when lenght is wrong
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=repr(value))

        #  Address Family IPv4
        if afi == afn.AFNUM_INET:
            if safi == safn.SAFNUM_LAB_VPNUNICAST:
                # MPLS VPN
                # parse nexthop
                rd_bin = nexthop_bin[0:8]
                rd_type = struct.unpack('!H', rd_bin[0:2])[0]
                rd_value_bin = rd_bin[2:]
                if rd_type == 0:
                    asn, an = struct.unpack('!HI', rd_value_bin)
                    ipv4 = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin[8:]), 16)))
                    nexthop = {'rd': '%s:%s' % (asn, an), 'str': ipv4}
                # TODO(xiaoquwl) for other RD type decoding
                else:
                    nexthop = repr(nexthop_bin[8:])
                # parse nlri
                nlri = IPv4MPLSVPN.parse(nlri_bin)
                return dict(afi_safi=(afi, safi), nexthop=nexthop, nlri=nlri)
            elif safi == safn.SAFNUM_FSPEC_RULE:
                # if nlri length is greater than 240 bytes, it is encoded over 2 bytes
                nlri_list = []
                while nlri_bin:
                    length = ord(nlri_bin[0])
                    if length >> 4 == 0xf and len(nlri_bin) > 2:
                        length = struct.unpack('!H', nlri_bin[:2])[0]
                        nlri_tmp = nlri_bin[2: length + 2]
                        nlri_bin = nlri_bin[length + 2:]
                    else:
                        nlri_tmp = nlri_bin[1: length + 1]
                        nlri_bin = nlri_bin[length + 1:]
                    nlri = IPv4FlowSpec.parse(nlri_tmp)
                    if nlri:
                        nlri_list.append(nlri)
                if nexthop_bin:
                    nexthop = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin), 16)))
                else:
                    nexthop = ''
                return dict(afi_safi=(afi, safi), nexthop=nexthop, nlri=nlri_list)
            else:
                nlri = repr(nlri_bin)

        # #  Address Family IPv6
        elif afi == afn.AFNUM_INET6:
            # IPv6 unicast
            if safi == safn.SAFNUM_UNICAST:
                # decode nexthop
                # RFC 2545
                # The value of the Length of Next Hop Network Address field on a
                # MP_REACH_NLRI attribute shall be set to 16, when only a global
                # address is present, or 32 if a link-local address is also included in
                # the Next Hop field.
                #
                # The link-local address shall be included in the Next Hop field if and
                # only if the BGP speaker shares a common subnet with the entity
                # identified by the global IPv6 address carried in the Network Address
                # of Next Hop field and the peer the route is being advertised to.
                nexthop_addrlen = 16
                has_link_local = False
                nexthop = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin[:nexthop_addrlen]), 16)))
                if len(nexthop_bin) == 2 * nexthop_addrlen:
                    # has link local address
                    has_link_local = True
                    linklocal_nexthop = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin[nexthop_addrlen:]), 16)))
                nlri = IPv6Unicast.parse(nlri_bin)
                if has_link_local:
                    return dict(afi_safi=(afi, safi), nexthop=nexthop, linklocal_nexthop=linklocal_nexthop, nlri=nlri)
                else:
                    return dict(afi_safi=(afi, safi), nexthop=nexthop, nlri=nlri)
            elif safi == safn.SAFNUM_LAB_VPNUNICAST:
                # IPv6 MPLS VPN
                # parse nexthop
                rd_bin = nexthop_bin[0:8]
                rd_type = struct.unpack('!H', rd_bin[0:2])[0]
                rd_value_bin = rd_bin[2:]
                if rd_type == 0:
                    asn, an = struct.unpack('!HI', rd_value_bin)
                    ipv6 = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin[8:]), 16)))
                    nexthop = {'rd': '%s:%s' % (asn, an), 'str': ipv6}
                # TODO(xiaoquwl) for other RD type decoding
                else:
                    nexthop = repr(nexthop_bin[8:])
                # parse nlri
                nlri = IPv6MPLSVPN.parse(nlri_bin)
                return dict(afi_safi=(afi, safi), nexthop=nexthop, nlri=nlri)
            else:
                return dict(afi_safi=(afi, safi), nexthop=nexthop_bin, nlri=nlri_bin)

        # for l2vpn
        elif afi == afn.AFNUM_L2VPN:
            if safi == safn.SAFNUM_EVPN:
                nexthop = str(netaddr.IPAddress(int(binascii.b2a_hex(nexthop_bin), 16)))
                nlri = EVPN.parse(nlri_bin)
                return dict(afi_safi=(afi, safi), nexthop=nexthop, nlri=nlri)
            else:
                nlri = repr(nlri_bin)

        else:
            nlri = repr(nlri_bin)

        return dict(afi_safi=(afi, safi), nexthop=nexthop_bin, nlri=nlri_bin)

    @classmethod
    def construct_mpls_vpn_nexthop(cls, nexthop):
        """
        construct nexthop to bin
        :param nexthop:
        :return:
        """
        asn, an = map(int, nexthop['rd'].split(':'))
        return struct.pack('!H', 0) + struct.pack('!HI', asn, an) + netaddr.IPAddress(nexthop['str']).packed

    @classmethod
    def construct(cls, value):

        """Construct a attribute

        :param value: python dictionary
        {'afi_safi': (1,128),
         'nexthop': {},
         'nlri': []
        """
        afi, safi = value['afi_safi']
        if afi == afn.AFNUM_INET:
            if safi == safn.SAFNUM_LAB_VPNUNICAST:  # MPLS VPN
                nexthop_hex = cls.construct_mpls_vpn_nexthop(value['nexthop'])
                nlri_hex = IPv4MPLSVPN.construct(value['nlri'])
                attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) +\
                    struct.pack('!B', len(nexthop_hex)) + nexthop_hex + b'\x00' + nlri_hex
                return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                    + struct.pack('!B', len(attr_value)) + attr_value
            elif safi == safn.SAFNUM_FSPEC_RULE:  # BGP Flow spec
                try:
                    try:
                        nexthop = netaddr.IPAddress(value['nexthop']).packed
                    except netaddr.core.AddrFormatError:
                        nexthop = ''
                    nlri_hex = b''
                    for nlri in value['nlri']:
                        nlri_hex += IPv4FlowSpec.construct(value=nlri)
                    if nlri_hex:
                        attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + \
                            struct.pack('!B', len(nexthop)) + nexthop + b'\x00' + nlri_hex
                        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                            + struct.pack('!B', len(attr_value)) + attr_value
                except Exception as e:
                    raise excep.ConstructAttributeFailed(
                        reason='failed to construct attributes: %s' % e,
                        data=value
                    )
            else:
                raise excep.ConstructAttributeFailed(
                    reason='unsupport this sub address family',
                    data=value)

        # ipv6 unicast
        elif afi == afn.AFNUM_INET6:

            if safi == safn.SAFNUM_LAB_VPNUNICAST:  # MPLS VPN
                nexthop_hex = cls.construct_mpls_vpn_nexthop(value['nexthop'])
                nlri_hex = IPv6MPLSVPN.construct(value['nlri'])
                attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) +\
                    struct.pack('!B', len(nexthop_hex)) + nexthop_hex + b'\x00' + nlri_hex
                return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                    + struct.pack('!B', len(attr_value)) + attr_value

            elif safi == safn.SAFNUM_UNICAST:
                nexthop_len = 16
                nexthop_bin = netaddr.IPAddress(value['nexthop']).packed
                if value.get('linklocal_nexthop'):
                    nexthop_len *= 2
                    nexthop_bin += netaddr.IPAddress(value['linklocal_nexthop']).packed

                nlri_bin = IPv6Unicast.construct(nlri_list=value['nlri'])

                attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + struct.pack('!B', nexthop_len) + \
                    nexthop_bin + b'\x00' + nlri_bin
                return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID)\
                    + struct.pack('!B', len(attr_value)) + attr_value
        # for l2vpn
        elif afi == afn.AFNUM_L2VPN:
            if safi == safn.SAFNUM_EVPN:
                nexthop_bin = netaddr.IPAddress(value['nexthop']).packed
                nlri_bin = EVPN.construct(nlri_list=value['nlri'])
                attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + struct.pack('!B', len(nexthop_bin)) + \
                    nexthop_bin + b'\x00' + nlri_bin
                return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID)\
                    + struct.pack('!B', len(attr_value)) + attr_value
        else:
            raise excep.ConstructAttributeFailed(
                reason='unsupport this sub address family',
                data=value)
