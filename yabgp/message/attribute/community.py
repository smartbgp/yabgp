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

import struct

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeID
from yabgp.message.attribute import AttributeFlag
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons


class Community(Attribute):
    """
        COMMUNITIES path attribute is an optional
    transitive attribute of variable length. The attribute consists of a
    set of four octet values, each of which specify a community. All
    routes with this attribute belong to the communities listed in the
    attribute.
        The COMMUNITIES attribute has Type Code 8.
        http://www.iana.org/assignments/bgp-well-known-communities/bgp-well-known-communities.xml
    """

    ID = AttributeID.COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value):
        """
        parse BGP community.
        :param value:
        """
        community = []
        if value:
            try:
                length = len(value) / 2
                value_list = list(struct.unpack('!%dH' % length, value))
                while value_list:
                    value_type = value_list[0] * 16 * 16 * 16 * 16 + value_list[1]
                    if value_type in bgp_cons.WELL_KNOW_COMMUNITY_INT_2_STR:
                        community.append(bgp_cons.WELL_KNOW_COMMUNITY_INT_2_STR[value_type])
                    else:
                        community.append("%s:%s" % (value_list[0], value_list[1]))
                    value_list = value_list[2:]
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value)
        return community

    @classmethod
    def construct(cls, value):
        """
        construct a COMMUNITY path attribute
        :param value:
        """
        community_hex = b''
        for community in value:
            if community.upper() in bgp_cons.WELL_KNOW_COMMUNITY_STR_2_INT:
                value = bgp_cons.WELL_KNOW_COMMUNITY_STR_2_INT[community.upper()]
                community_hex += struct.pack('!I', value)
            else:
                try:
                    value = community.split(':')
                    value = int(value[0]) * 16 * 16 * 16 * 16 + int(value[1])
                    community_hex += struct.pack('!I', value)
                except Exception:
                    raise excep.UpdateMessageError(
                        sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                        data=value
                    )

        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
            + struct.pack('!B', len(community_hex)) + community_hex
