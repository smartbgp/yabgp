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

import struct
from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV

# https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.1
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |               Type            |            Length             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                      SID/Label (variable)                     |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# If length is set to 3, then the 20 rightmost bits represent a label.
# If length is set to 4, then the value represents a 32 bit SID.


@LinkState.register()
class SIDorLabel(TLV):

    TYPE = 1161  # https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.1
    TYPE_STR = "sid_or_label"

    @classmethod
    def unpack(cls, value):
        """
        """
        length = len(value)
        if length == 3:
            return cls(value={"type": "sid", "value": (struct.unpack('!I', "\x00" + value)[0] << 12) >> 12})
        elif length == 4:
            return cls(value={"type": "label", "value": struct.unpack('!I', value)[0]})
