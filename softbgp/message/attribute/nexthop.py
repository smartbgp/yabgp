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
import binascii

from ipaddr import IPv4Address

from softbgp.message.attribute import Attribute
from softbgp.message.attribute import AttributeID
from softbgp.message.attribute import AttributeFlag
from softbgp.common import constants as bgp_cons
from softbgp.common import exception as excep


class NextHop(Attribute):
    """
        This is a well-known mandatory attribute that defines the
    (unicast) IP address of the router that SHOULD be used as
    the next hop to the destinations listed in the Network Layer
    Reachability Information field of the UPDATE message.
    """

    ID = AttributeID.NEXT_HOP
    FLAG = AttributeFlag.TRANSITIVE
    MULTIPLE = False

    @staticmethod
    def parse(value):

        """
        Parse BGP nexthop.
        :param value: raw binary value
        """
        next_hop = '0.0.0.0'
        if len(value) % 4 == 0:

            while value:
                try:
                    next_hop = IPv4Address(int(binascii.b2a_hex(value[0:4]), 16)).__str__()
                except Exception:
                    # Error process
                    raise excep.UpdateMessageError(
                        sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_NEXTHOP,
                        data=value[0:4])
                value = value[4:]
        else:
            # Error process
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)
        return next_hop

    def construct(self, value, flags=None):
        """
        encode BGP nexthop attribute.
        """
        try:
            ipv4_addr = IPv4Address(value)
        except:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_NEXTHOP,
                data=value)
        ip_addr_raw = ipv4_addr.packed
        if not flags:
            flags = self.FLAG
        return struct.pack('!B', flags) + struct.pack('!B', self.ID) \
            + struct.pack('!B', len(ip_addr_raw)) + ip_addr_raw
