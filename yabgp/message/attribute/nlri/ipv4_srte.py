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

"""IPv4 SR TE Policy NLRI
"""
import struct
import netaddr

from yabgp.message.attribute.nlri import NLRI


class IPv4SRTE(NLRI):
    """
    """
    # +------------------+
    # |  NLRI Length     |    1 octet
    # +------------------+
    # |  Distinguisher   |    4 octets
    # +------------------+
    # |  Policy Color    |    4 octets
    # +------------------+
    # |  Endpoint        |    4 or 16 octets
    # +------------------+
    @classmethod
    def construct(cls, data):
        """ Construct NLRI """
        nlri_tmp = b'' + struct.pack('!I', data['distinguisher']) + \
            struct.pack('!I', data['color']) + \
            netaddr.IPAddress(data['endpoint']).packed
        return struct.pack('!B', len(nlri_tmp) * 8) + nlri_tmp
