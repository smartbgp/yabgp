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
import netaddr

from yabgp.tlv import TLV
from .l3service import SRv6L3Service


# 3.1.  SRv6 SID Information Sub-TLV
#
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | SRv6 Service  |    SRv6 Service               |               |
# | Sub-TLV       |    Sub-TLV                    |               |
# | Type=1        |    Length                     |  RESERVED1    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  SRv6 SID Value (16 octets)                                  //
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Svc SID Flags |   SRv6 Endpoint Behavior      |   RESERVED2   |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  SRv6 Service Data Sub-Sub-TLVs                              //
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#            Figure 3: SRv6 SID Information Sub-TLV


@SRv6L3Service.register()
class SRv6SIDInformation(TLV):
    """
    SRv6 SID Information
    """
    TYPE = 1  # https://datatracker.ietf.org/doc/html/rfc9252.html#section-3.1
    TYPE_STR = 'srv6_sid_information'

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
                raise RuntimeError('Duplicated SRv6 Service Data Sub-Sub-TLV type')
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

        # reserved_1 = data[0:1]  # Note: First byte is reserved
        srv6_sid_value = str(netaddr.IPAddress(int(binascii.b2a_hex(data[1:17]), 16)))
        srv6_service_sid_flags = ord(data[17:18])
        srv6_endpoint_behavior = struct.unpack('!H', data[18:20])[0]
        # reserved_2 = data[20:21]  # Note: Also reserved
        data = data[21:]
        while data:
            srv6_service_data_sub_sub_tlv_type_code = data[0]  # Note: Type = 1 octet
            srv6_service_data_sub_sub_tlv_length = struct.unpack('!H', data[1:3])[0]  # Note: Length = 2 octet
            value = data[3: 3 + srv6_service_data_sub_sub_tlv_length]

            if srv6_service_data_sub_sub_tlv_type_code in cls.registered_tlvs:
                tlvs.append(cls.registered_tlvs[srv6_service_data_sub_sub_tlv_type_code].unpack(value))
            else:
                tlvs.append({
                    'type': srv6_service_data_sub_sub_tlv_type_code,
                    'value': str(binascii.b2a_hex(value))
                })
            data = data[3 + srv6_service_data_sub_sub_tlv_length:]
        value = {
            'srv6_sid_value': srv6_sid_value,
            'srv6_service_sid_flags': srv6_service_sid_flags,
            'srv6_endpoint_behavior': srv6_endpoint_behavior,

            'srv6_service_data_sub_sub_tlvs': tlvs
        }
        return {cls.TYPE_STR: value}
