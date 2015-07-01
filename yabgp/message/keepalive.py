# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
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

""" BGP KeepAlive message"""

import struct

from yabgp.common.exception import MessageHeaderError
from yabgp.common.constants import ERR_MSG_HDR_BAD_MSG_LEN


class KeepAlive(object):

    """
    KEEPALIVE messages are exchanged between peers often
    enough not to cause the Hold Timer to expire
    """
    MSG_KEEPALIVE = 4

    @staticmethod
    def parse(msg):
        """
        Parse keepalive message

        :param msg: input raw binary message data
        """
        if len(msg) != 0:
            raise MessageHeaderError(
                sub_error=ERR_MSG_HDR_BAD_MSG_LEN,
                data='')

    @staticmethod
    def construct_header():

        """Prepends the mandatory header to a constructed BGP message
        """
        #    16-octet     2-octet  1-octet
        # ---------------+--------+---------+------+
        #    Maker      | Length |  Type   |  msg |
        # ---------------+--------+---------+------+
        return b'\xff'*16 + struct.pack('!HB', 19, 4)

    def construct(self):
        """
        Construct a keepalive message
        """
        return self.construct_header()
