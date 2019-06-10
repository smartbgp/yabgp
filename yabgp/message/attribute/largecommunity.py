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


class LargeCommunity(Attribute):
    """
        LARGE COMMUNITIES path attribute is an optional
    transitive attribute of variable length. The attribute consists of a
    set of 12 octet values, each of which specify a community. All
    routes with this attribute belong to the communities listed in the
    attribute.
        The LARGE COMMUNITIES attribute has Type Code 32.
        https://tools.ietf.org/html/rfc8092#page-3
    """

    ID = AttributeID.LARGE_COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE + AttributeFlag.PARTIAL

    @classmethod
    def parse(cls, value):
        """
        parse BGP large community.
        :param value:
        """
        large_community = []
        if value:
            try:
                length = len(value) / 4
                value_list = list(struct.unpack('!%di' % length, value))
                while value_list:
                    large_community.append("%s:%s:%s" % (value_list[0], value_list[1], value_list[2]))
                    value_list = value_list[3:]
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value)
        return large_community

    @classmethod
    def construct(cls, value):
        """
        construct a LARGE COMMUNITY path attribute
        :param value:
        """
        large_community_hex = b''
        for large_community in value:
            try:
                value = large_community.split(':')
                for sub_value in value:
                    large_community_hex += struct.pack('!I', int(sub_value))
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value
                )

        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
            + struct.pack('!B', len(large_community_hex)) + large_community_hex
