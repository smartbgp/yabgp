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

import binascii

from yabgp.tlv import TLV
from ..linkstate import LinkState

# https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-ls-segment-routing-ext/?include_text=1

#     0                   1                   2                   3
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |               Type            |            Length             |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |     Flags     |   Algorithm   |           Reserved            |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                       SID/Index/Label (variable)              |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# isis
#  0 1 2 3 4 5 6 7
#  +-+-+-+-+-+-+-+-+

#  |R|N|P|E|V|L|   |
#  +-+-+-+-+-+-+-+-+

# ospf
#  0 1  2 3 4 5 6 7
# +-+--+-+-+-+-+-+-+
# | |NP|M|E|V|L| | |
# +-+--+-+-+-+-+-+-+

# ospfv3
#  0 1  2 3 4 5 6 7
# +-+--+-+-+-+-+-+-+
# | |NP|M|E|V|L| | |
# +-+--+-+-+-+-+-+-+


@LinkState.register()
class PrefixSID(TLV):
    """
    prefix sid
    """
    TYPE = 1158
    TYPE_STR = 'prefix_sid'

    @classmethod
    def unpack(cls, data, pro_id):

        flags = ord(data[0:1])
        flag = {}
        if pro_id in [1, 2]:
            flag['R'] = flags >> 7
            flag['N'] = (flags << 1) % 256 >> 7
            flag['P'] = (flags << 2) % 256 >> 7
            flag['E'] = (flags << 3) % 256 >> 7
            flag['V'] = (flags << 4) % 256 >> 7
            flag['L'] = (flags << 5) % 256 >> 7
        else:  # 3, 6
            flag['NP'] = (flags << 1) % 256 >> 7
            flag['M'] = (flags << 2) % 256 >> 7
            flag['E'] = (flags << 3) % 256 >> 7
            flag['V'] = (flags << 4) % 256 >> 7
            flag['L'] = (flags << 5) % 256 >> 7

        algorithm = ord(data[1:2])
        return cls(value={"flags": flag, "algorithm": algorithm, "sid": int(binascii.b2a_hex(data[4:]), 16)})
