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
import struct
import netaddr
from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV

# https://tools.ietf.org/html/draft-gredler-idr-bgp-ls-segment-routing-ext-03#section-2.2.2
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Type             |            Length             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |     Flags     |     Weight    |            Reserved           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |             OSPF Neighbor ID / IS-IS System-ID                |
# +                               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    SID/Label/Index (variable)                 |
# +---------------------------------------------------------------+

#   Flags: 1 octet field of following flags:
#       0 1 2 3 4 5 6 7
#      +-+-+-+-+-+-+-+-+
#      |F|B|V|L|S|P|   |
#      +-+-+-+-+-+-+-+-+


@LinkState.register()
class LanAdjSegID(TLV):
    """
    Adjacency Segment id
    """
    TYPE = 1100
    TYPE_STR = 'lan-adj-segment-id'

    @classmethod
    def unpack(cls, data):
        flags = struct.unpack('!B', data[0])[0]
        F = flags >> 7
        B = (flags << 1) % 256 >> 7
        V = (flags << 2) % 256 >> 7
        L = (flags << 3) % 256 >> 7
        S = (flags << 4) % 256 >> 7
        P = (flags << 5) % 256 >> 7
        weight = struct.unpack('!B', data[1])[0]
        # nei_or_sys_id = struct.unpack('!6B', data[4:10])
        nei_or_sys_id = str(netaddr.IPAddress(int(binascii.b2a_hex(data[4:10]), 16)))
        sid_index_label = int(binascii.b2a_hex(data[10:]), 16)
        # if len(data) == 3:
        #     sid_index_label = (struct.unpack('!I', "\x00" + data)[0] << 12) >> 12
        # elif len(data) == 4:
        #     sid_index_label = struct.unpack('!I', data)[0]
        return cls(value={
            "flags": {"F": F, "B": B, "V": V, "L": L, "S": S, "P": P},
            "weight": weight,
            "nei_or_sys_id": nei_or_sys_id,
            "sid_index_label": sid_index_label
        })
