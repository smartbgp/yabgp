# Copyright 2024 Cisco Systems, Inc.
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
from ..bgpprefixsid import BGPPrefixSID


# 2.  SRv6 Services TLVs
#
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |   TLV Type    |         TLV Length            |   RESERVED    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |   SRv6 Service Sub-TLVs                                      //
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
#                   Figure 1: SRv6 Service TLVs


@BGPPrefixSID.register()
class SRv6L3Service(TLV):
    """
    SRv6 L3 Service
    """
    TYPE = 5  # https://datatracker.ietf.org/doc/html/rfc9252.html#section-2
    TYPE_STR = 'srv6_l3_service'

    registered_tlvs = dict()

    @classmethod
    def register(cls, _type=None):
        """

        :param _type:
        :return:
        """

        def decorator(klass):
            """

            :param klass:
            :return:
            """
            _id = klass.TYPE if _type is None else _type
            if _id in cls.registered_tlvs:
                raise RuntimeError('Duplicated SRv6 Service Sub-TLV type')
            cls.registered_tlvs[_id] = klass
            return klass

        return decorator

    @classmethod
    def unpack(cls, data):
        """

        :param data:
        :return:
        """
        tlvs = []

        # reserved = data[0:1]  # Note: First byte is reserved
        data = data[1:]
        while data:
            srv6_service_sub_tlv_type_code = data[0]  # Note: Type = 1 octet
            srv6_service_sub_tlv_length = struct.unpack('!H', data[1:3])[0]  # Note: Length = 2 octet
            value = data[3: 3 + srv6_service_sub_tlv_length]

            if srv6_service_sub_tlv_type_code in cls.registered_tlvs:
                tlvs.append(cls.registered_tlvs[srv6_service_sub_tlv_type_code].unpack(value).dict())
            else:
                tlvs.append({
                    'type': srv6_service_sub_tlv_type_code,
                    'value': str(binascii.b2a_hex(value))
                })
            data = data[3 + srv6_service_sub_tlv_length:]
        value = {
            'srv6_service_sub_tlvs': tlvs
        }
        return cls(value=value)
