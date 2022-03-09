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


@LinkState.register(_type=1050)
class NodeMSD_1050(TLV):
    """
    node msd, type 1050
    https://tools.ietf.org/html/draft-tantsura-idr-bgp-ls-segment-routing-msd-05#section-3
    """

    TYPE_STR = 'node_msd'

    @classmethod
    def unpack(cls, data):
        _type, value = struct.unpack('!BB', data)
        return cls(value={"type": _type, "value": value})


@LinkState.register(_type=266)
class NodeMSD_266(TLV):
    """
    node msd, type 266
    https://tools.ietf.org/html/draft-tantsura-idr-bgp-ls-segment-routing-msd-05#section-3
    """

    TYPE_STR = 'node_msd'

    @classmethod
    def unpack(cls, data):

        lst = []
        for i in range(0, len(data), 2):
            # byte_type, byte_value = data[i], data[i+1]
            MSD_Type, MSD_Value = struct.unpack("!BB", data[i:i+2])
            lst.append({"MSD_Type": MSD_Type, "MSD_Value": MSD_Value})
        return cls(value=lst)
