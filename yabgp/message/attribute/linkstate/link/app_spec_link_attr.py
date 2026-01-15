# Copyright 2025 Cisco Systems, Inc.
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
from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV


@LinkState.register()
class AppSpecLinkAttr(TLV):
    """
    Application-Specific Link Attributes TLV (Type 1122)
    RFC 9294 Section 3: https://www.rfc-editor.org/rfc/rfc9294.html#section-3

    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | SABM Length   | UDABM Length  |            Reserved           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Standard Application Identifier Bit Mask (variable)      //
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |    User-Defined Application Identifier Bit Mask (variable)   //
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                      Link Attribute sub-TLVs                 //
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Fields:
        - SABM Length (1 octet): Standard Application Identifier Bit Mask Length
        - UDABM Length (1 octet): User-Defined Application Identifier Bit Mask Length
        - Reserved (2 octets): Must be zero
        - SABM (variable, 0/4/8 octets): Standard Application Identifier Bit Mask
        - UDABM (variable, 0/4/8 octets): User-Defined Application Identifier Bit Mask
        - Link Attribute sub-TLVs (variable): Application-specific link attributes
    """
    TYPE = 1122
    TYPE_STR = 'ASLA'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Application-Specific Link Attributes TLV

        :param data: binary data (without type and length)
        :return: AppSpecLinkAttr instance
        """
        # Parse fixed header (4 bytes)
        sabm_len = data[0]
        udabm_len = data[1]
        # reserved = struct.unpack('!H', data[2:4])[0]

        offset = 4

        # Parse SABM (Standard Application Identifier Bit Mask)
        sabm = None
        if sabm_len > 0:
            sabm_bytes = data[offset:offset + sabm_len]
            if sabm_len == 4:
                sabm_int = struct.unpack('!I', sabm_bytes)[0]
                sabm = '0x{:08x}'.format(sabm_int)
            elif sabm_len == 8:
                sabm_int = struct.unpack('!Q', sabm_bytes)[0]
                sabm = '0x{:016x}'.format(sabm_int)
            else:
                sabm = '0x' + binascii.b2a_hex(sabm_bytes).decode('ascii')
            offset += sabm_len

        # Parse UDABM (User-Defined Application Identifier Bit Mask)
        udabm = None
        if udabm_len > 0:
            udabm_bytes = data[offset:offset + udabm_len]
            if udabm_len == 4:
                udabm_int = struct.unpack('!I', udabm_bytes)[0]
                udabm = '0x{:08x}'.format(udabm_int)
            elif udabm_len == 8:
                udabm_int = struct.unpack('!Q', udabm_bytes)[0]
                udabm = '0x{:016x}'.format(udabm_int)
            else:
                udabm = '0x' + binascii.b2a_hex(udabm_bytes).decode('ascii')
            offset += udabm_len

        # Parse Link Attribute sub-TLVs
        sub_tlvs_bin_data = data[offset:]
        sub_tlvs = []

        while sub_tlvs_bin_data:
            sub_tlv_type, sub_tlv_len = struct.unpack('!HH', sub_tlvs_bin_data[:4])
            sub_tlv_value = sub_tlvs_bin_data[4:4 + sub_tlv_len]

            if sub_tlv_type in LinkState.registered_tlvs:
                sub_tlvs.append(LinkState.registered_tlvs[sub_tlv_type].unpack(sub_tlv_value).dict())
            else:
                sub_tlvs.append({
                    'type': sub_tlv_type,
                    'value': str(binascii.b2a_hex(sub_tlv_value))
                })
            sub_tlvs_bin_data = sub_tlvs_bin_data[4 + sub_tlv_len:]

        return cls(value={
            'sabm': {'len': sabm_len, 'value': sabm},
            'udabm': {'len': udabm_len, 'value': udabm},
            'sub_tlvs': sub_tlvs
        })
