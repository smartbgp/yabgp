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

# https://tools.ietf.org/html/rfc7752#section-3.3.1.5
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Type             |             Length            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# //               Opaque node attributes (variable)             //
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@LinkState.register()
class OpaNodeAttr(TLV):

    TYPE = 1025  # https://tools.ietf.org/html/rfc7752#section-3.3.1.5
    TYPE_STR = "opa_node_attr"

    @classmethod
    def unpack(cls, value):
        """
        """
        return cls(value=struct.unpack("!%ds" % len(value), value)[0])
