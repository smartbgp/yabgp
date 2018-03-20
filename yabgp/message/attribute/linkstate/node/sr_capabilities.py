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

# https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.2
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |               Type            |          Length               |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |      Flags    |   RESERVED    |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                  Range Size                   |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    //                SID/Label sub-TLV (variable)                 //
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@LinkState.register()
class SRCapabilities(TLV):

    TYPE = 1034  # https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.2
    TYPE_STR = "sr_capabilities"

    @classmethod
    def unpack(cls, value):
        """
        """
        flags = ord(value[0:1])
        F = flags >> 7
        M = (flags << 1) % 256 >> 7
        S = (flags << 2) % 256 >> 7
        D = (flags << 3) % 256 >> 7
        A = (flags << 4) % 256 >> 7
        value = value[2:]
        results = []
        while True:
            if len(value) == 0:
                break
            else:
                tmp = dict()
                range_size = struct.unpack('!I', b"\x00" + value[:3])[0]
                tmp['range_size'] = range_size
                length = struct.unpack('!H', value[5:7])[0]
                if length == 3:
                    data = (struct.unpack('!I', b"\x00" + value[7:7 + length])[0] << 12) >> 12
                    value = value[7 + length:]
                    tmp['label'] = data
                elif length == 4:
                    data = struct.unpack('!I', value[7:7 + length])[0]
                    value = value[7 + length:]
                    tmp['sid'] = data
                results.append(tmp)
        return cls(value={"flag": {"F": F, "M": M, "S": S, "D": D, "A": A}, "value": results})
