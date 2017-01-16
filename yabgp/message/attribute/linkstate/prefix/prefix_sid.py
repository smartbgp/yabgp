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

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.common.tlv import TLV

# https://tools.ietf.org/html/draft-ietf-isis-segment-routing-extensions-09


@LinkState.register()
class PrefixSID(TLV):

    TYPE = 1158
    TYPE_STR = "prefix-segment-identifier "

    # @classmethod
    # def parse(cls, value):
    #     """
    #     """
    #     flags = ['R', 'N', 'P', 'E', 'V', 'L']
    #     flags_int = struct.unpack('!B', value[0])[0]
    #     bit_list = []
    #     for i in xrange(8):
    #         bit_list.append((flags_int >> i) & 1)
    #     bit_list.reverse()
    #
    #     return cls(value=dict(zip(flags, bit_list[0:6])))
    #
    # @classmethod
    # def algorithm(cls, value):
    #     pass
