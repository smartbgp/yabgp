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
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep


class Origin(Attribute):
    """
        ORIGIN is a well-known mandatory attribute that defines the
    origin of the path information. The data octet can assume
    the following values:
    Value       Meaning
        0        IGP  -  Network Layer Reachability Information
                  is interior to the originating AS
        1        EGP - Network Layer Reachability Information
                  learned via the EGP protocol [RFC904]
        2        INCOMPLETE - Network Layer Reachability
                 Information learned by some other means
    """
    ID = AttributeID.ORIGIN
    FLAG = AttributeFlag.TRANSITIVE
    MULTIPLE = False

    IGP = 0x00
    EGP = 0x01
    INCOMPLETE = 0x02

    @classmethod
    def parse(cls, value):
        """
        Error process:
        (1) the falgs of the ORIGIN attribute must be "well-know,transitive"
        (2) If the ORIGIN attribute has an undefined value, then the Error Sub-code
        MUST be set to Invalid Origin Attribute. The Data field MUST contain the
        unrecognized attribute (type,length, and vlaue)
        :param value: raw binary value
        """
        orgin = struct.unpack('!B', value)[0]
        if orgin not in [cls.IGP, cls.EGP, cls.INCOMPLETE]:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_ORIGIN,
                data=value)
        return orgin

    @classmethod
    def construct(cls, value):

        """
        construct a origin attribute
        :param value: 0,1,2
        """
        if value not in [cls.IGP, cls.EGP, cls.INCOMPLETE]:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_ORIGIN,
                data='')
        length = 1
        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
            + struct.pack('!B', length) + struct.pack('!B', value)
