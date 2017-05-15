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

import binascii


class TLV(object):
    """TLV basic class
    """
    TYPE = -1
    TYPE_STR = "UNKNOWN"

    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s: %s' % (self.TYPE_STR, self.value)

    @classmethod
    def unpack(cls, value):
        """unpack binary data
        """
        return cls(value=binascii.b2a_hex(value))

    def dict(self, str_key=True):
        """return dict format
        """
        if str_key:
            return {
                'type': self.TYPE_STR,
                'value': self.value}
        return {
            'type': self.TYPE,
            'value': self.value
        }
