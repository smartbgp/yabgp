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

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class NodeMSD(TLV):
    """
    node msd
    """
    TYPE = 1050  # https://tools.ietf.org/html/draft-tantsura-idr-bgp-ls-segment-routing-msd-05#section-3
    TYPE_STR = 'node_msd'

    @classmethod
    def unpack(cls, data):
        _type, value = struct.unpack('!BB', data)
        return cls(value={"type": _type, "value": value})
