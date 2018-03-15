# Copyright 2015-2018 Cisco Systems, Inc.
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

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV

# https://tools.ietf.org/html/rfc5307#section-1.2
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |Protection Cap |    Reserved   |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# 0x01  Extra Traffic
# 0x02  Unprotected
# 0x04  Shared
# 0x08  Dedicated 1:1
# 0x10  Dedicated 1+1
# 0x20  Enhanced
# 0x40  Reserved
# 0x80  Reserved


@LinkState.register()
class ProtectionType(TLV):

    TYPE = 1093  # https://tools.ietf.org/html/rfc5307#section-1.2
    TYPE_STR = "protection_type"

    @classmethod
    def unpack(cls, value):
        """
        """
        value = ord(value[0])
        if value == 0x01:
            return cls(value='Extra Traffic')
        if value == 0x02:
            return cls(value='Unprotected')
        if value == 0x04:
            return cls(value='Shared')
        if value == 0x08:
            return cls(value='Dedicated 1:1')
        if value == 0x10:
            return cls(value='Dedicated 1+1')
        if value == 0x20:
            return cls(value='Enhanced')
