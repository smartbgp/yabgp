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

# https://tools.ietf.org/html/rfc7752#section-3.3.3.1
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Type             |             Length            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |D|N|L|P| Resvd.|
# +-+-+-+-+-+-+-+-+

# +----------+---------------------------+-----------+
# |   Bit    | Description               | Reference |
# +----------+---------------------------+-----------+
# |   'D'    | IS-IS Up/Down Bit         | [RFC5305] |
# |   'N'    | OSPF "no unicast" Bit     | [RFC5340] |
# |   'L'    | OSPF "local address" Bit  | [RFC5340] |
# |   'P'    | OSPF "propagate NSSA" Bit | [RFC5340] |
# | Reserved | Reserved for future use.  |           |
# +----------+---------------------------+-----------+


@LinkState.register()
class IGPFlags(TLV):

    TYPE = 1152  # https://tools.ietf.org/html/rfc7752#section-3.3.3.1
    TYPE_STR = "igp_flags"

    @classmethod
    def unpack(cls, value):
        """
        """
        value = ord(value[0:1])
        D = value >> 7
        N = (value << 1) % 256 >> 7
        L = (value << 2) % 256 >> 7
        P = (value << 3) % 256 >> 7
        return cls(value={'D': D, 'N': N, 'L': L, 'P': P})
