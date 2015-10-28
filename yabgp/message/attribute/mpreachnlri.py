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

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri.ipv4_mpls_vpn import IPv4MPLSVPN
from yabgp.message.attribute.nlri.ipv4_flowspec import IPv4FlowSpec


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
            nexthop_data = value[4:4 + nexthop_length]
            nlri_data = value[5 + nexthop_length:]
        except Exception:
            # error when lenght is wrong
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=repr(value))
        if afi == afn.AFNUM_INET:
            if safi == safn.SAFNUM_LAB_VPNUNICAST:
                nlri = IPv4MPLSVPN.parse(nlri_data)

            elif safi == safn.SAFNUM_FSPEC_RULE:
                # if nlri length is greater than 240 bytes, it is encoded over 2 bytes
                if len(nlri_data) >= 240:
                    nlri_data = nlri_data[2:]
                else:
                    nlri_data = nlri_data[1:]
                nlri = IPv4FlowSpec.parse(nlri_data)

            else:
                nlri = repr(nlri_data)
        else:
            nlri = repr(nlri_data)

        return dict(afi_safi=(afi, safi), nexthop=nexthop_data, nlri=nlri)

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
                pass
            elif safi == safn.SAFNUM_FSPEC_RULE:  # BGP Flow spec
                try:
                    try:
                        nexthop = netaddr.IPAddress(value['nexthop']).packed
                    except netaddr.core.AddrFormatError:
                        nexthop = ''
                    nlri = IPv4FlowSpec.construct(value=value['nlri'])
                    if nlri:
                        attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + \
                            struct.pack('!B', len(nexthop)) + nexthop + '\x00' + nlri
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
        else:
            raise excep.ConstructAttributeFailed(
                reason='unsupport this sub address family',
                data=value)
