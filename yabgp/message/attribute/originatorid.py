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

import binascii
import struct

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons


class OriginatorID(Attribute):
    """
        ORIGINATOR_ID is a new optional, non-transitive BGP attribute of Type
    code 9. This attribute is 4 bytes long and it will be created by an
    RR in reflecting a route. This attribute will carry the BGP
    Identifier of the originator of the route in the local AS. A BGP
    speaker SHOULD NOT create an ORIGINATOR_ID attribute if one already
    exists. A router that recognizes the ORIGINATOR_ID attribute SHOULD
    ignore a route received with its BGP Identifier as the ORIGINATOR_ID.
    (RFC 4456 Page 6)
    """

    ID = AttributeID.ORIGINATOR_ID
    FLAG = AttributeFlag.OPTIONAL

    @classmethod
    def parse(cls, value):

        """
        Parse originator id
        :param value:
        """
        if len(value) != 4:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)
        return str(netaddr.IPAddress(int(binascii.b2a_hex(value[0:4]), 16)))

    @classmethod
    def construct(cls, value):

        """
        construct a ORIGINATOR_ID path attribute
        :param value: ipv4 format string
        """
        try:
            return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', 4) + netaddr.IPAddress(value).packed
        except Exception:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)
