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

import binascii

from yabgp.tlv import TLV
from ..linkstate import LinkState


# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |               Type            |              Length           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Flags         |     Weight    |             Reserved          |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                   SID/Label/Index (variable)                  |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#  0 1 2 3 4 5 6 7
# +-+-+-+-+-+-+-+-+
# |V|L|B|P|       |
# +-+-+-+-+-+-+-+-+


@LinkState.register()
class PeerAdjSID(TLV):
    """
    Peer Adjacency Segment Identifier (Peer-Adj-SID)
    """
    TYPE = 1102
    TYPE_STR = 'peer_adj_sid'

    @classmethod
    def unpack(cls, data):
        flags = ord(data[0:1])
        flag = {}
        flag['V'] = flags >> 7
        flag['L'] = (flags << 1) % 256 >> 7
        flag['B'] = (flags << 2) % 256 >> 7
        flag['P'] = (flags << 3) % 256 >> 7
        weight = ord(data[1:2])
        return cls(value={"flags": flag, "weight": weight, "value": int(binascii.b2a_hex(data[4:]), 16)})
