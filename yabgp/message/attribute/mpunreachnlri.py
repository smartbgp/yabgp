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
from yabgp.message.attribute.nlri.ipv4_flowspec import IPv4FlowSpec
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

        nlri = value[3:]

        # for IPv4
        if afi == afn.AFNUM_INET:
            # BGP flow spec
            if safi == safn.SAFNUM_FSPEC_RULE:
                return IPv4FlowSpec().parse(value=nlri)
            else:
                return {'afi_safi': (afn.AFNUM_INET, safi),
                        'withdraw': repr(nlri)}

        return dict(afi_safi=(afi, safi), withdraw=nlri)

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
                pass
            elif safi == safn.SAFNUM_FSPEC_RULE:
                try:
                    nlri = IPv4FlowSpec().construct(value=value['withdraw'])
                    if nlri:
                        attr_value = struct.pack('!H', afi) + struct.pack('!B', safi) + \
                            nlri
                        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                            + struct.pack('!B', len(attr_value)) + attr_value
                    else:
                        return None
                    pass
                except Exception:
                    raise excep.ConstructAttributeFailed(
                        reason='failed to construct attributes',
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
