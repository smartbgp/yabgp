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
class SRv6EndpointBehavior(TLV):
    """
    SRv6 Endpoint Behavior
    """
    TYPE = 1250  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-14#section-7.1
    TYPE_STR = 'srv6_endpoint_behavior'

    @classmethod
    def unpack(cls, data):
        """

        :param data:
        :return:
        """
        endpoint_behavior = struct.unpack('!H', data[0:2])[0]
        flags = ord(data[2:3])
        algorithm = ord(data[3:4])

        return cls(value={
            'endpoint_behavior': endpoint_behavior,
            'flags': flags,
            'algorithm': algorithm
        })
