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

import binascii
import struct

import netaddr

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class SRv6EndXSID(TLV):
    """
    SRv6 End.X SID
    """
    TYPE = 1106  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-09#section-4.1
    TYPE_STR = 'srv6_end_x_sid'

    @classmethod
    def unpack(cls, data):
        endpoint_behavior = struct.unpack('!H', data[:2])[0]
        flags = ord(data[2:3])

        # Use the same unpacking method for IS-IS or OSPFv3
        # IS-IS: https://datatracker.ietf.org/doc/html/rfc9352#name-srv6-endx-sid-sub-tlv
        # OSPFv3: https://datatracker.ietf.org/doc/html/draft-ietf-lsr-ospfv3-srv6-extensions-09#section-9.1
        flag = {}
        flag['B'] = flags >> 7
        flag['S'] = (flags << 1) % 256 >> 7
        flag['P'] = (flags << 2) % 256 >> 7

        algorithm = ord(data[3:4])
        weight = ord(data[4:5])
        # reserved = ord(data[5:6])
        sid = str(netaddr.IPAddress(int(binascii.b2a_hex(data[6:22]), 16)))
        sub_tlvs_bin_data = data[22:]

        sub_tlvs = []
        while sub_tlvs_bin_data:
            sub_tlvs_type_code, sub_tlvs_length = struct.unpack('!HH', sub_tlvs_bin_data[:4])
            sub_tlvs_value = sub_tlvs_bin_data[4: 4 + sub_tlvs_length]

            if sub_tlvs_type_code in LinkState.registered_tlvs:
                # Note: "sub_tlvs_value" does not contains "sub_tlvs_type_code" & "sub_tlvs_length"
                sub_tlvs.append(LinkState.registered_tlvs[sub_tlvs_type_code].unpack(sub_tlvs_value).dict())
            else:
                sub_tlvs.append({
                    'type': sub_tlvs_type_code,
                    'value': str(binascii.b2a_hex(sub_tlvs_value))
                })
            sub_tlvs_bin_data = sub_tlvs_bin_data[4 + sub_tlvs_length:]

        return cls(value={
            'endpoint_behavior': endpoint_behavior,
            'flags': flag,
            'algorithm': algorithm,
            'weight': weight,
            'sid': sid,
            'sub_tlvs': sub_tlvs
        })
