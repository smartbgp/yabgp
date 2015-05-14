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

"""BGP Notification Message"""

import struct

from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons


class Notification(object):

    """
    notification
    """
    MSG_NOTIFICATION = 3

    @staticmethod
    def parse(message):
        """
        parse notification message

        :param message: input raw binary message data
        """
        try:
            error, suberror = struct.unpack('!BB', message[:2])
            data = message[2:]
        except:
            raise excep.UpdateMessageError(
                sub_error=bgp_cons.ERR_MSG_HDR_BAD_MSG_LEN,
                data=repr(message))
        return error, suberror, data

    def construct_header(self, message):

        """Prepends the mandatory header to a constructed BGP message

        :param message:
        """
        #    16-octet     2-octet  1-octet
        # ---------------+--------+---------+------+
        #    Maker      | Length |  Type   |  msg |
        # ---------------+--------+---------+------+
        return struct.pack('!16sHB',
                           chr(255) * 16,
                           len(message) + 19,
                           self.MSG_NOTIFICATION) + message

    def construct(self, error, suberror=0, data=''):

        """Constructs a BGP Notification message

        :param error:
        :param suberror:
        :param data:
        """

        msg = struct.pack('!BB', error, suberror) + data
        return self.construct_header(msg)
