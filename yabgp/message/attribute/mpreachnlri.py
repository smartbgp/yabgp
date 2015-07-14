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

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri.ipv4_mpls_vpn import IPv4MPLSVPN


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

        return {
            'afi_safi': (afi, safi),
            'nexthop': nexthop_data,
            'nlri': nlri
        }

    @classmethod
    def construct(cls, value):
        pass
