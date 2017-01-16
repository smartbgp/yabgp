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

import binascii

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.common.tlv import TLV

import netaddr


@LinkState.register(typecode=1028, typestr='local-router-id')
@LinkState.register(typecode=1029, typestr='local-router-id')
@LinkState.register(typecode=1030, typestr='remote-router-id')
@LinkState.register(typecode=1031, typestr='remote-router-id')
class RouterID(TLV):
    """ Router ID
    """
    @classmethod
    def parse(cls, value):
        return cls(value=str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16))))
