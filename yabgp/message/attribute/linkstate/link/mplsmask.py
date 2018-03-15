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

# https://tools.ietf.org/html/rfc7752#section-3.3.2.2
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Type             |             Length            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |L|R|  Reserved |
# +-+-+-+-+-+-+-+-+

# +------------+------------------------------------------+-----------+
# |    Bit     | Description                              | Reference |
# +------------+------------------------------------------+-----------+
# |    'L'     | Label Distribution Protocol (LDP)        | [RFC5036] |
# |    'R'     | Extension to RSVP for LSP Tunnels        | [RFC3209] |
# |            | (RSVP-TE)                                |           |
# | 'Reserved' | Reserved for future use                  |           |
# +------------+------------------------------------------+-----------+


@LinkState.register()
class MplsMask(TLV):

    TYPE = 1094  # https://tools.ietf.org/html/rfc7752#section-3.3.2.2
    TYPE_STR = "mpls_mask"

    @classmethod
    def unpack(cls, value):
        """
        """
        value = ord(value[0:1])
        L = value >> 7
        R = (value << 1) % 256 >> 7
        return cls(value={'L': L, 'R': R})
