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

from yabgp.message.attribute import Attribute, AttributeFlag, AttributeID


class BGPPrefixSID(Attribute):
    """
    BGP Prefix SID

    Original: https://datatracker.ietf.org/doc/html/rfc8669#section-3
    Extend: https://datatracker.ietf.org/doc/html/rfc9252#section-2
    """

    ID = AttributeID.BGP_PREFIX_SID
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    registered_tlvs = dict()

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value

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
                raise RuntimeError('Duplicated attribute type')
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
        while data:
            type_code = data[0]  # Note: Type = 1 octet
            length = struct.unpack('!H', data[1:3])[0]  # Note: Length = 2 octet
            value = data[3: 3 + length]

            if type_code in cls.registered_tlvs:
                tlvs.append(cls.registered_tlvs[type_code].unpack(value))
            else:
                tlvs.append({
                    'type': type_code,
                    'value': str(binascii.b2a_hex(value))
                })
            data = data[3 + length:]
        return tlvs
