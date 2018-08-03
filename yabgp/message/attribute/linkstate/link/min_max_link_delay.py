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

import binascii

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register(_type=1115)
class MinMaxUnidirectLinkDelay(TLV):
    """
     Min/Max Unidirectional Link Delay
    """
    # TYPE = 1115  # https://tools.ietf.org/html/draft-ietf-idr-te-pm-bgp-10#section-3.2
    TYPE_STR = 'min_max_unidirect_link_delay'

    @classmethod
    def unpack(cls, data):
        min_value = int(binascii.b2a_hex(data[:4]), 16)
        max_value = int(binascii.b2a_hex(data[4:]), 16)
        return cls(value={
            "min_link_delay": min_value,
            "max_link_delay": max_value,
        })
