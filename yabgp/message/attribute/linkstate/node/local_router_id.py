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

from yabgp.net import IPAddress
from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register(_type=1028)
class LocalRouterID(TLV):
    """
    local ipv4 router id
    """
    TYPE_STR = 'local_router_id'

    @classmethod
    def unpack(cls, data):
        router_id = IPAddress.unpack(data)
        return cls(value=router_id)


@LinkState.register(_type=1029)
class LocalRouterIDIPv6(TLV):
    """
    local ipv6 router id
    """
    TYPE_STR = 'local_router_id_ipv6'

    @classmethod
    def unpack(cls, data):
        router_id = IPAddress.unpack(data)
        return cls(value=router_id)
