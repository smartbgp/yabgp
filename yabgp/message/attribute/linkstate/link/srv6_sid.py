# Copyright 2022 Cisco Systems, Inc.
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

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class SRv6SID(TLV):
    """
    SRv6 SID Structure
    """
    TYPE = 1252  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-09#section-8
    TYPE_STR = 'srv6_sid'

    @classmethod
    def unpack(cls, data):
        # Note: "data" is "sub_tlvs_value", does not contains "sub_tlvs_type_code" & "sub_tlvs_length"
        return cls(value={
            'locator_block_length': ord(data[:1]),
            'locator_node_length': ord(data[1:2]),
            'function_length': ord(data[2:3]),
            'argument_length': ord(data[3:4])
        })
