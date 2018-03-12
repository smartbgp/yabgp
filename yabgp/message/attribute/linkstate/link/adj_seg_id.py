# Copyright 2015-2017 Cisco Systems, Inc.
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
# +---------------------------------------------------------------+

# isis
# 0 1 2 3 4 5 6 7
# +-+-+-+-+-+-+-+-+
# |F|B|V|L|S|P|   |
# +-+-+-+-+-+-+-+-+

# ospf
# 0 1 2 3 4 5 6 7
# +-+-+-+-+-+-+-+-+
# |B|V|L|G|P|     |
# +-+-+-+-+-+-+-+-+

# ospf-v3
# 0 1 2 3 4 5 6 7
# +-+-+-+-+-+-+-+-+
# |B|V|L|G|P|     |
# +-+-+-+-+-+-+-+-+


@LinkState.register()
class AdjSegID(TLV):
    """
    Adjacency Segment id
    """
    TYPE = 1099
    TYPE_STR = 'adj-segment-id'

    @classmethod
    def unpack(cls, data, pro_id):
        flags = struct.unpack('!B', data[0])[0]
        flag = {}
        if pro_id in [1, 2]:
            flag['F'] = flags >> 7
            flag['B'] = (flags << 1) % 256 >> 7
            flag['V'] = (flags << 2) % 256 >> 7
            flag['L'] = (flags << 3) % 256 >> 7
            flag['S'] = (flags << 4) % 256 >> 7
            flag['P'] = (flags << 5) % 256 >> 7
        else:  # 3, 6
            flag['B'] = flags >> 7
            flag['V'] = (flags << 1) % 256 >> 7
            flag['L'] = (flags << 2) % 256 >> 7
            flag['G'] = (flags << 3) % 256 >> 7
            flag['P'] = (flags << 4) % 256 >> 7
        weight = struct.unpack('!B', data[1])[0]
        return cls(value={"flags": flag, "weight": weight, "sid_index_label": int(binascii.b2a_hex(data[4:]), 16)})
        # return cls(value=int(binascii.b2a_hex(data[4:]), 16))
