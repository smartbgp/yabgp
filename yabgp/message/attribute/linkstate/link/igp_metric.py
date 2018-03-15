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

import struct
import binascii

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class IGPMetric(TLV):
    """
    IGP Metric
    """
    TYPE = 1095
    TYPE_STR = 'igp_metric'

    @classmethod
    def unpack(cls, data):
        if len(data) == 2:
            return cls(value=struct.unpack('!H', data)[0])
        elif len(data) == 1:
            return cls(value=ord(data[0:1]))
        elif len(data) == 3:
            return cls(value=int(binascii.b2a_hex(data), 16))
