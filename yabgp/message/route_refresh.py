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

"""BGP Route Refresh Message"""

import struct


class RouteRefresh(object):

    """
    Route Refresh message
    """

    def __init__(self, afi=None, safi=None, res=0):

        # Message Format: One <AFI, SAFI> encoded as
        # 0       7       15      23     31
        # +-------+-------+-------+-------+
        # |      AFI      | Res.  | SAFI  |
        # +-------+-------+-------+-------+
        """
        :param afi  - Address Family Identifier (16 bit)
               http://www.iana.org/assignments/address-family-numbers/address-family-numbers.xml
        :param safi: . - Reserved (8 bit) field. Should be set to 0 by the
               sender and ignored by the receiver.
        :param res:  - Subsequent Address Family Identifier (8 bit).
               http://www.iana.org/assignments/safi-namespace/safi-namespace.xml
        """
        self.afi = afi
        self.res = res
        self.safi = safi

    def parse(self, msg):

        """ Parse a route refresh message

         :param msg: raw hex message """

        self.afi, self.res, self.safi = struct.unpack("!HBB", msg)
        return self.afi, self.res, self.safi

    @staticmethod
    def construct_header(message, msg_type):

        """Prepends the mandatory header to a constructed BGP message

        :param msg_type: 5 or 128 """
        #    16-octet     2-octet  1-octet
        # ---------------+--------+---------+------+
        #    Maker      | Length |  Type   |  msg |
        # ---------------+--------+---------+------+
        return b'\xff'*16 + struct.pack('!HB',
                                        len(message) + 19,
                                        msg_type) + message

    def construct(self, msg_type):

        """
        construts a BGP Route Refresh message
        Two Types
        type = 5 (new route refresh RFC 2918)
        type = 128 (cisco route refresh before RFC 2918)
        """

        msg = struct.pack('!H', self.afi) + struct.pack('!B', self.res) + struct.pack('!B', self.safi)
        return self.construct_header(msg, msg_type)
