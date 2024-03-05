# Copyright 2024 Cisco Systems, Inc.
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

from yabgp.tlv import TLV
from .sidinformation import SRv6SIDInformation


# 3.2.1.  SRv6 SID Structure Sub-Sub-TLV
#
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | SRv6 Service  |    SRv6 Service               | Locator Block |
# | Data Sub-Sub  |    Data Sub-Sub-TLV           | Length        |
# | -TLV Type=1   |    Length                     |               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Locator Node  | Function      | Argument      | Transposition |
# | Length        | Length        | Length        | Length        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Transposition |
# | Offset        |
# +-+-+-+-+-+-+-+-+
#
#           Figure 5: SRv6 SID Structure Sub-Sub-TLV


@SRv6SIDInformation.register()
class SRv6SIDStructure(TLV):
    """
    SRv6 SID Structure
    """
    TYPE = 1  # https://datatracker.ietf.org/doc/html/rfc9252.html#section-3.2.1
    TYPE_STR = 'srv6_sid_structure'

    @classmethod
    def unpack(cls, data):
        """

        :param data:
        :return:
        """
        locator_block_length = ord(data[0])
        locator_node_length = ord(data[1])
        function_length = ord(data[2])
        argument_length = ord(data[3])
        transposition_length = ord(data[4])
        transposition_offset = ord(data[5])
        value = {
            'locator_block_length': locator_block_length,
            'locator_node_length': locator_node_length,
            'function_length': function_length,
            'argument_length': argument_length,
            'transposition_length': transposition_length,
            'transposition_offset': transposition_offset
        }
        return cls(value=value)
