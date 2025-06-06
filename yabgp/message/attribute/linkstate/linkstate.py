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
import logging
import struct

import binascii
import traceback
from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep
from yabgp.message.attribute import Attribute, AttributeFlag, AttributeID

LOG = logging.getLogger()


class LinkState(Attribute):
    """BGP link-state attribute
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
            value = data[4: 4 + length]
            try:
                if type_code in [1099, 1100, 1158, 1162, 1038] and type_code in cls.registered_tlvs:
                    tlvs.append(cls.registered_tlvs[type_code].unpack(value, bgpls_pro_id).dict())
                elif type_code in cls.registered_tlvs:
                    tlvs.append(cls.registered_tlvs[type_code].unpack(value).dict())
                else:
                    tlvs.append(
                        {
                            'type': type_code,
                            'value': str(binascii.b2a_hex(value))
                        }
                    )
            except Exception as e:
                LOG.error(e)
                error_str = traceback.format_exc()
                LOG.debug(error_str)
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_MALFORMED_ATTR_LIST,
                    data=value,
                    sub_results=cls(value=tlvs))

            data = data[4 + length:]

        return cls(value=tlvs)
