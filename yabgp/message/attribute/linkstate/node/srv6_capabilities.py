# Copyright 2023 Cisco Systems, Inc.
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
class SRv6Capabilities(TLV):
    """
    SRv6 Capabilities TLV
    """
    TYPE = 1038  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-14#section-3.1
    TYPE_STR = 'srv6_capabilities'

    @classmethod
    def unpack(cls, data, bgpls_pro_id):
        """

        :param data:
        :param bgpls_pro_id:
        :return:
        """
        flags = struct.unpack('!H', data[:2])[0]
        flag = {}
        if bgpls_pro_id in (1, 2):
            # https://datatracker.ietf.org/doc/html/rfc9352#name-srv6-capabilities-sub-tlv
            flag['O-flag'] = (flags << 1) % 256 >> 15
        elif bgpls_pro_id in (3, 6):
            # https://datatracker.ietf.org/doc/html/draft-ietf-lsr-ospfv3-srv6-extensions-09#section-2
            flag['O-flag'] = (flags << 1) % 256 >> 15
        else:
            flag = flags
        # reserved = struct.unpack('!H', data[2:4])[0]

        return cls(value={
            'flags': flag
        })
