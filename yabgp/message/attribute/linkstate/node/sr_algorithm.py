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

#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |            Type               |            Length             |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |  Algorithm 1  |  Algorithm... |  Algorithm N |                |
#    +-                                                             -+
#    |                                                               |
#    +                                                               +


@LinkState.register()
class SRAlgorithm(TLV):
    """
    sr algorithm
    """
    TYPE = 1035  # https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.3
    TYPE_STR = 'sr_algorithm'

    @classmethod
    def unpack(cls, data):
        if type(data) is str:
            results = [struct.unpack('!B', value)[0] for value in data]
        else:
            results = list(data)
        return cls(value=results)
