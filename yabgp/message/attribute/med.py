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
from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep


class MED(Attribute):
    """
    This is an optional non-transitive attribute that is a
    four-octet unsigned integer. The value of this attribute
    MAY be used by a BGP speaker's Decision Process to
    discriminate among multiple entry points to a neighboring
    autonomous system.
    """

    ID = AttributeID.MULTI_EXIT_DISC
    FLAG = AttributeFlag.OPTIONAL
    MULTIPLE = False

    @classmethod
    def parse(cls, value):
        """
        parse BGP med attributes
        :param value: raw binary value
        """
        try:
            return struct.unpack('!I', value)[0]
        except:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)

    @classmethod
    def construct(cls, value):
        """
        encode BGP med attributes
        :param value:
        """
        try:
            return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', 4) + struct.pack('!I', value)
        except Exception:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data='')
