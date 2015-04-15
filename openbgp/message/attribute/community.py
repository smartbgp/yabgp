# Copyright (C) 2015 Cisco Systems, Inc.
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

from openbgp.message.attribute import Attribute
from openbgp.message.attribute import AttributeID
from openbgp.message.attribute import AttributeFlag
from openbgp.common import exception as excep
from openbgp.common import constants as bgp_cons


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
    # Reserved = range(0x00000000,0xFFFEFFFF)
    PLANNED_SHUT = 0xFFFF0000
    ACCEPT_OWN = 0xFFFF0001
    ROUTE_FILTER_TRANSLATED_v4 = 0xFFFF0002
    ROUTE_FILTER_v4 = 0xFFFF0003
    ROUTE_FILTER_TRANSLATED_v6 = 0xFFFF0004
    ROUTE_FILTER_v6 = 0xFFFF0005
    NO_EXPORT = 0xFFFFFF01
    NO_ADVERTISE = 0xFFFFFF02
    NO_EXPORT_SUBCONFED = 0xFFFFFF03
    NOPEER = 0xFFFFFF04

    ID = AttributeID.COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    def parse(self, value):
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
                    if 'UNKNOW' != self.to_string(value_type):
                        community.append(self.to_string(value_type))
                    else:
                        community.append("%s:%s" % (value_list[0], value_list[1]))
                    value_list = value_list[2:]
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value)
        return community

    @staticmethod
    def to_string(community_type):

        if community_type == 0xFFFF0000:
            return 'PLANNED_SHUT'
        elif community_type == 0xFFFF0001:
            return 'ACCEPT_OWN'
        elif community_type == 0xFFFF0002:
            return 'ROUTE_FILTER_TRANSLATED_v4'
        elif community_type == 0xFFFF0003:
            return 'ROUTE_FILTER_v4'
        elif community_type == 0xFFFF0004:
            return 'ROUTE_FILTER_TRANSLATED_v6'
        elif community_type == 0xFFFF0005:
            return 'ROUTE_FILTER_v6'
        elif community_type == 0xFFFFFF01:
            return 'NO_EXPORT'
        elif community_type == 0xFFFFFF02:
            return 'NO_ADVERTISE'
        elif community_type == 0xFFFFFF03:
            return 'NO_EXPORT_SUBCONFED'
        elif community_type == 0xFFFFFF04:
            return 'NOPEER'
        # elif community_typeCode == 317000132:
        #    return "TEST"
        else:
            return 'UNKNOW'

    @staticmethod
    def to_int(value):

        if value == 'PLANNED_SHUT':
            return 0xFFFF0000
        elif value == 'ACCEPT_OWN':
            return 0xFFFF0001
        elif value == 'ROUTE_FILTER_TRANSLATED_v4':
            return 0xFFFF0002
        elif value == 'ROUTE_FILTER_v4':
            return 0xFFFF0003
        elif value == 'ROUTE_FILTER_TRANSLATED_v6':
            return 0xFFFF0004
        elif value == 'ROUTE_FILTER_v6':
            return 0xFFFF0005
        elif value == 'NO_EXPORT':
            return 0xFFFFFF01
        elif value == 'NO_ADVERTISE':
            return 0xFFFFFF02
        elif value == 'NO_EXPORT_SUBCONFED':
            return 0xFFFFFF03
        elif value == 'NOPEER':
            return 0xFFFFFF04
        
    def construct(self, value, flags=None):
        """
        construct a COMMUNITY path attribute
        :param value:
        :param flags
        """
        community_hex = ''
        for community in value:
            try:
                value = self.to_int(community.upper())
                community_hex += struct.pack('!I', value)
            except Exception:
                value = community.split(':')
                value = int(value[0]) * 16 * 16 * 16 * 16 + int(value[1])
                community_hex += struct.pack('!I', value)

        if not flags:
            flags = self.FLAG
        return struct.pack('!B', flags) + struct.pack('!B', self.ID) \
            + struct.pack('!B', len(community_hex)) + community_hex
