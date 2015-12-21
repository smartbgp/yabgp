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


class AtomicAggregate(Attribute):
    """
    ATOMIC_AGGREGATE is a well-known discretionary attribute of length 0.
    """

    ID = AttributeID.ATOMIC_AGGREGATE
    FLAG = AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value):

        """
        parse bgp ATOMIC_AGGREGATE attribute
        :param value:
        """
        if not value:
            return value
        else:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_OPTIONAL_ATTR,
                data=value)

    @classmethod
    def construct(cls, value):
        """construct a ATOMIC_AGGREGATE path attribute
        :param value:
        """

        if value:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_UPDATE_OPTIONAL_ATTR,
                data='')
        else:
            value = 0
        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
            + struct.pack('!B', value)
