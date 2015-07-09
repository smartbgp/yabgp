# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
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

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeID
from yabgp.message.attribute import AttributeFlag
from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep


class Aggregator(Attribute):
    """
        AGGREGATOR is an optional transitive attribute of length 6.
    The attribute contains the last AS number that formed the
    aggregate route (encoded as 2 octets), followed by the IP
    address of the BGP speaker that formed the aggregate route
    (encoded as 4 octets). This SHOULD be the same address as
    the one used for the BGP Identifier of the speaker
    """

    ID = AttributeID.AGGREGATOR
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value, asn4=False):

        """
        Parse Aggregator attributes.
        :param value: raw binary value
        :param asn4: support 4 bytes asn or not
        """

        if not asn4:
            try:
                asn = struct.unpack('!H', value[:2])[0]
                aggregator = str(netaddr.IPAddress(struct.unpack('!I', value[2:])[0]))
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value)
        else:
            # 4 bytes ASN
            try:
                asn = struct.unpack('!I', value[:4])[0]
                aggregator = str(netaddr.IPAddress(struct.unpack('!I', value[4:])[0]))
            except Exception:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data=value)

        return asn, aggregator

    @classmethod
    def construct(cls, value, asn4=False):

        """
        Construct aggregator.
        :param value:
        :param asn4:
        """
        try:
            if asn4:
                agg_raw = struct.pack('!I', value[0]) + netaddr.IPAddress(value[1]).packed
            else:
                agg_raw = struct.pack('!H', value[0]) + netaddr.IPAddress(value[1]).packed

            return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', len(agg_raw)) + agg_raw
        except Exception:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)
