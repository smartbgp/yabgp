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

import struct
import binascii

from yabgp.message.attribute import Attribute, AttributeFlag, AttributeID


class LinkState(Attribute):
    """BGP linksate attribute
    """
    ID = AttributeID.LINKSTATE
    FLAG = AttributeFlag.OPTIONAL

    registered_tlvs = dict()

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value

    @classmethod
    def register(cls, _type=None):
        """register tlvs
        """
        def decorator(klass):
            """decorator
            """
            _id = klass.TYPE if _type is None else _type
            if _id in cls.registered_tlvs:
                raise RuntimeError('duplicated attribute type')
            cls.registered_tlvs[_id] = klass
            return klass
        return decorator

    def dict(self):
        """return dict
        """
        return {self.ID: self.value}

    @classmethod
    def unpack(cls, data, bgpls_pro_id=None):
        """unpack binary data
        """
        tlvs = []
        while data:
            type_code, length = struct.unpack('!HH', data[:4])
            value = data[4: 4+length]
            if type_code in [1099, 1100] and type_code in cls.registered_tlvs:
                tlvs.append(cls.registered_tlvs[type_code].unpack(value, bgpls_pro_id).dict())
            elif type_code in cls.registered_tlvs:
                tlvs.append(cls.registered_tlvs[type_code].unpack(value).dict())
            else:
                tlvs.append(
                    {
                        'type': type_code,
                        'value': binascii.b2a_hex(value)

                    }
                )
            data = data[4+length:]

        return cls(value=tlvs)
