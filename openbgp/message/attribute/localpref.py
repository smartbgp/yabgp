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

from openbgp.message.attribute import Attribute
from openbgp.message.attribute import AttributeID
from openbgp.message.attribute import AttributeFlag
from openbgp.common import constants as bgp_cons
from openbgp.common import exception as excep


class LocalPreference(Attribute):
    """LOCAL_PREF is a well-known attribute that is a four-octet
    unsigned integer. A BGP speaker uses it to inform its other
    internal peers of the advertising speaker's degree of
    preference for an advertised route.
    """

    ID = AttributeID.LOCAL_PREF
    FLAG = AttributeFlag.TRANSITIVE
    MULTIPLE = False

    @staticmethod
    def parse(value):

        """
        parse bgp local preference attribute
        :param value: raw binary value
        """
        try:
            return struct.unpack('!I', value)[0]
        except:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data=value)

    def construct(self, value, flags=None):
        """
        encode bgp local preference attribute
        :param value:
        :param flags:
        """
        if not flags:
            flags = self.FLAG
        try:
            return struct.pack('!B', flags) + struct.pack('!B', self.ID) \
                + struct.pack('!B', 4) + struct.pack('!I', value)
        except Exception:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                data='')
