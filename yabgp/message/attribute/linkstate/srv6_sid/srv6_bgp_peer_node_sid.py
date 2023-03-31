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
class SRv6BGPPeerNodeSID(TLV):
    """
    SRv6 BGP Peer Node SID
    """
    TYPE = 1251  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-14#section-7.2
    TYPE_STR = 'srv6_bgp_peer_node_sid'

    @classmethod
    def unpack(cls, data):
        """

        :param data:
        :return:
        """
        flags = ord(data[0:1])
        flag = {}
        flag['B'] = flags >> 7
        flag['S'] = (flags << 1) % 256 >> 7
        flag['P'] = (flags << 2) % 256 >> 7
        weight = ord(data[1:2])
        # reserved = struct.unpack('!H', data[2:4])[0]
        peer_as_number = '.'.join([str(each) for each in struct.unpack('!HH', data[4:8])])
        peer_bgp_identifier = struct.unpack('!I', data[8:12])[0]

        return cls(value={
            'flags': flag,
            'weight': weight,
            # 'reserved': reserved,
            'peer_as_number': peer_as_number,
            'peer_bgp_identifier': peer_bgp_identifier
        })
