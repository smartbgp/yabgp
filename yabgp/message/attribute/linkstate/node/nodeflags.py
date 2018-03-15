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

# https://tools.ietf.org/html/rfc7752#section-3.3.1.1
#      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |              Type             |             Length            |
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |O|T|E|B|R|V| Rsvd|
#     +-+-+-+-+-+-+-+-+-+
#
#     +-----------------+-------------------------+------------+
#     |       Bit       | Description             | Reference  |
#     +-----------------+-------------------------+------------+
#     |       'O'       | Overload Bit            | [ISO10589] |
#     |       'T'       | Attached Bit            | [ISO10589] |
#     |       'E'       | External Bit            | [RFC2328]  |
#     |       'B'       | ABR Bit                 | [RFC2328]  |
#     |       'R'       | Router Bit              | [RFC5340]  |
#     |       'V'       | V6 Bit                  | [RFC5340]  |
#     | Reserved (Rsvd) | Reserved for future use |            |
#     +-----------------+-------------------------+------------+


@LinkState.register()
class NodeFlags(TLV):

    TYPE = 1024  # https://tools.ietf.org/html/rfc7752#section-3.3.1.1
    TYPE_STR = "node_flags"

    @classmethod
    def unpack(cls, value):
        """
        """
        valueByte = ord(value[0:1])
        O = valueByte >> 7
        T = (valueByte << 1) % 256 >> 7
        E = (valueByte << 2) % 256 >> 7
        B = (valueByte << 3) % 256 >> 7
        R = (valueByte << 4) % 256 >> 7
        V = (valueByte << 5) % 256 >> 7
        return cls(value={"O": O, "T": T, "E": E, "B": B, "R": R, "V": V})
