# Copyright 2015 Cisco Systems, Inc.
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

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeID
from yabgp.message.attribute import AttributeFlag


class LinkState(Attribute):
    """BGP Link State
    """

    ID = AttributeID.LINKSTATE
    FLAG = AttributeFlag.OPTIONAL
    MULTIPLE = False

    MUTI_TOPO_ID = 263
    NODE_FLAG = 1024
    OPA_NODE = 1025
    NODE_NAME = 1026
    ISIS_AREA_ID = 1027
    IPV4_ROUTER_ID = 1028
    IPV6_ROUTER_ID = 1029

    @classmethod
    def parse(cls, value):

        """
        parse linkstate
        :param value: raw binary value
        """
        value_dict = dict()
        while value:
            _type, _len = struct.unpack('!HH', value[0:2])
            _value = value[2: 2+_len]

            if _type == cls.NODE_NAME:
                value_dict[_type] = _value.decode('ascii')

            else:
                value_dict[_type] = binascii.b2a_hex(_value)

            value = value[3+_len:]

        return value_dict

    @classmethod
    def construct(cls, value):
        """
        :param value: interger value
        """
        pass
