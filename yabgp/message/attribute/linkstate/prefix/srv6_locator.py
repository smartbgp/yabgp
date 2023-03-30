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

import binascii

from yabgp.tlv import TLV
from ..linkstate import LinkState


@LinkState.register()
class SRv6Locator(TLV):
    """
    SRv6 Locator TLV
    """
    TYPE = 1162  # https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgpls-srv6-ext-14#section-5.1
    TYPE_STR = 'srv6_locator'

    @classmethod
    def unpack(cls, data, bgpls_pro_id):
        """

        :param data:
        :param bgpls_pro_id:
        :return:
        """
        flags = ord(data[:1])
        flag = {}
        if bgpls_pro_id in (1, 2):  # IS-IS
            # https://datatracker.ietf.org/doc/html/rfc9352#section-7.1
            flag['D'] = flags >> 7
        else:
            flag = flags  # TODO (OSPFv3 SRv6)
        algorithm = ord(data[1:2])
        # reserved = struct.unpack('!H', data[2:4])[0]
        metric = struct.unpack('!HH', data[4:8])[0]
        sub_tlvs_bin_data = data[8:]

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
            'flags': flag,
            'algorithm': algorithm,
            # 'reserved': reserved,
            'metric': metric,
            'sub_tlvs': sub_tlvs
        })
