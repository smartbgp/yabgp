# Copyright 2025 Cisco Systems, Inc.
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
from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class MultiTopologyIdentifier(TLV):
    """MultiTopologyIdentifier TLV (Type 263)

    RFC 7752 Section 3.2.1.5:
    https://datatracker.ietf.org/doc/html/rfc7752#section-3.2.1.5

    Format:
      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |              Type             |          Length=2*n           |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |R R R R|  Multi-Topology ID 1  |             ....             //
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     //             ....             |R R R R|  Multi-Topology ID n  |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    The MT-ID field is a 12-bit field (with 4 reserved bits).
    Multiple MT-IDs can be present in the TLV (each 2 bytes).
    """
    TYPE = 263
    TYPE_STR = 'mt_id'

    @classmethod
    def unpack(cls, data):
        mt_id = []
        while data:
            mt_id.append(struct.unpack('!H', data[:2])[0])
            data = data[2:]
        return cls(value=mt_id)
