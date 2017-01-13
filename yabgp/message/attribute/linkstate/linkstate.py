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

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.message import TLV


class LinkState(Attribute):
    """
    The BGP-LS attribute is an optional, non-transitive BGP attribute
    that is used to carry link, node, and prefix parameters and
    attributes.  It is defined as a set of Type/Length/Value (TLV)
    triplets, described in the following section.  This attribute SHOULD
    only be included with Link-State NLRIs.  This attribute MUST be
    ignored for all other address families."""

    ID = AttributeID.LINK_STATE
    ID_STR = str(AttributeID(ID))
    FLAG = AttributeFlag.OPTIONAL

    registered_tlvs = {}

    def __init__(self, ls_tlvs):
        self.ls_tlvs = ls_tlvs

    @classmethod
    def register(cls, typecode=None, typestr=None):
        def decorator(klass):
            if typecode:
                klass.TYPE = typecode
            if typestr:
                klass.TYPE_STR = typestr
            cls.registered_tlvs[klass.TYPE] = klass
            return klass

        return decorator

    @classmethod
    def parse(cls, value):
        ls_tlvs = []
        while value:
            type_code, length = struct.unpack('!HH', value[:4])
            if type_code in cls.registered_tlvs:
                klass = cls.registered_tlvs[type_code].parse(value[4:length + 4])
            else:
                klass = TLV.parse(value=value[4:length + 4])
            klass.TLV = type_code
            ls_tlvs.append(klass)
            value = value[length + 4:]

        return cls(ls_tlvs=ls_tlvs)

    def dict(self):
        return {self.ID: [tlv.dict() for tlv in self.ls_tlvs]}
