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

"""BGP Attribute MP_UNREACH_NLRI
"""

import struct

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.message.attribute.nlri.ipv4_mpls_vpn import IPv4MPLSVPN
from yabgp.message.attribute.nlri.ipv6_mpls_vpn import IPv6MPLSVPN
from yabgp.message.attribute.nlri.ipv4_flowspec import IPv4FlowSpec
from yabgp.message.attribute.nlri.ipv6_unicast import IPv6Unicast
from yabgp.message.attribute.nlri.evpn import EVPN
from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons


class MpUnReachNLRI(Attribute):

    """
        This is an optional non-transitive attribute that can be used for the
    purpose of withdrawing multiple unfeasible routes from service.
        An UPDATE message that contains the MP_UNREACH_NLRI is not required
    to carry any other path attributes.

        MP_UNREACH_NLRI coding information
        +---------------------------------------------------------+
        | Address Family Identifier (2 octets)                    |
        +---------------------------------------------------------+
        | Subsequent Address Family Identifier (1 octet)          |
        +---------------------------------------------------------+
        | Withdrawn Routes (variable)                             |
        +---------------------------------------------------------+
    """

    ID = AttributeID.MP_UNREACH_NLRI
    FLAG = AttributeFlag.OPTIONAL

    @classmethod
    def parse(cls, value):
        try:
            afi, safi = struct.unpack('!HB', value[0:3])
        except Exception:
            raise excep.UpdateMessageError(sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                                           data='')

        nlri_bin = value[3:]

        # for IPv4
        if afi == afn.AFNUM_INET:

            # VPNv4
            if safi == safn.SAFNUM_LAB_VPNUNICAST:
                nlri = IPv4MPLSVPN.parse(nlri_bin, iswithdraw=True)
                return dict(afi_safi=(afi, safi), withdraw=nlri)
            # BGP flow spec
            elif safi == safn.SAFNUM_FSPEC_RULE:
                # if nlri length is greater than 240 bytes, it is encoded over 2 bytes
                withdraw_list = []
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
                        withdraw_list.append(nlri)

                return dict(afi_safi=(afi, safi), withdraw=withdraw_list)
            else:
                return dict(afi_safi=(afn.AFNUM_INET, safi), withdraw=repr(nlri_bin))
        # for ipv6
        elif afi == afn.AFNUM_INET6:
            # for ipv6 unicast
            if safi == safn.SAFNUM_UNICAST:
                return dict(afi_safi=(afi, safi), withdraw=IPv6Unicast.parse(nlri_data=nlri_bin))
            elif safi == safn.SAFNUM_LAB_VPNUNICAST:
                return dict(afi_safi=(afi, safi), withdraw=IPv6MPLSVPN.parse(value=nlri_bin, iswithdraw=True))
            else:
                return dict(afi_safi=(afi, safi), withdraw=repr(nlri_bin))
        # for l2vpn
        elif afi == afn.AFNUM_L2VPN:
            # for evpn
            if safi == safn.SAFNUM_EVPN:
                return dict(afi_safi=(afi, safi), withdraw=EVPN.parse(nlri_data=nlri_bin))
            else:
                return dict(afi_safi=(afi, safi), withdraw=repr(nlri_bin))

        else:
            return dict(afi_safi=(afi, safi), withdraw=repr(nlri_bin))

    @classmethod
    def construct(cls, value):

        """Construct a attribute

        :param value: python dictionary
        {'afi_safi': (1,128),
         'withdraw': []
        """
        afi, safi = value['afi_safi']
        if afi == afn.AFNUM_INET:
            if safi == safn.SAFNUM_LAB_VPNUNICAST:  # MPLS VPN
                nlri = IPv4MPLSVPN.construct(value['withdraw'], iswithdraw=True)
                if nlri:
                    attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + nlri
                    return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                        + struct.pack('!B', len(attr_value)) + attr_value
                else:
                    return None
            elif safi == safn.SAFNUM_FSPEC_RULE:
                try:
                    nlri_list = value.get('withdraw') or []
                    if not nlri_list:
                        return None
                    nlri_hex = b''
                    for nlri in nlri_list:
                        nlri_hex += IPv4FlowSpec.construct(value=nlri)
                    attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + nlri_hex
                    return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                        + struct.pack('!B', len(attr_value)) + attr_value

                except Exception:
                    raise excep.ConstructAttributeFailed(
                        reason='failed to construct attributes',
                        data=value
                    )
            else:
                raise excep.ConstructAttributeFailed(
                    reason='unsupport this sub address family',
                    data=value)
        elif afi == afn.AFNUM_INET6:
            if safi == safn.SAFNUM_UNICAST:
                nlri = IPv6Unicast.construct(nlri_list=value['withdraw'])
                if nlri:
                    attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + nlri
                    return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                        + struct.pack('!B', len(attr_value)) + attr_value
            elif safi == safn.SAFNUM_LAB_VPNUNICAST:
                nlri = IPv6MPLSVPN.construct(value=value['withdraw'], iswithdraw=True)
                if nlri:
                    attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + nlri
                    return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                        + struct.pack('!B', len(attr_value)) + attr_value
                else:
                    return None
        # for l2vpn
        elif afi == afn.AFNUM_L2VPN:
            # for evpn
            if safi == safn.SAFNUM_EVPN:
                nlri = EVPN.construct(nlri_list=value['withdraw'])
                if nlri:
                    attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + nlri
                    return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                        + struct.pack('!B', len(attr_value)) + attr_value
            else:
                return None
        else:
            raise excep.ConstructAttributeFailed(
                reason='unsupport this sub address family',
                data=value)
