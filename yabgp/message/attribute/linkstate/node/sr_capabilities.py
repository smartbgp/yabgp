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

# https://tools.ietf.org/html/draft-previdi-isis-segment-routing-extensions-04#section-3.1
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |   Type        |     Length    |    Flags      |    Range      |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Range (cont.) |      SID/Label Sub-TLV (variable size)        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@LinkState.register()
class SRCapabilities(TLV):

    TYPE = 1034
    TYPE_STR = "sr-capabilities"
    #
    # @classmethod
    # def parse(cls, value):
    #     """
    #     """
    #     results = dict()
    #     if ord(value[0]) == 0x80:
    #         results['ipv4'] = True
    #     else:
    #         results['ipv6'] = True
    #     results['range-size'] = struct.unpack('!L', value[1:5])[0]
    #     return cls(value=results)
