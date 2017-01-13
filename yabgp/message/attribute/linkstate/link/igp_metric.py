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

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.message import TLV


# The IGP Metric TLV carries the metric for this link.  The length of
#    this TLV is variable, depending on the metric width of the underlying
#    protocol.  IS-IS small metrics have a length of 1 octet (the two most
#    significant bits are ignored).  OSPF link metrics have a length of 2
#    octets.  IS-IS wide metrics have a length of 3 octets.
#
#       0                   1                   2                   3
#       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#      |              Type             |             Length            |
#      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#      //      IGP Link Metric (variable length)      //
#      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@LinkState.register()
class IGPMetric(TLV):

    TYPE = 1095
    TYPE_STR = "igp-link-metric"

    @classmethod
    def parse(cls, value):
        """
        """
        return cls(value=int(binascii.b2a_hex(value), 16))
