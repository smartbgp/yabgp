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

""" IPv6 Unicast """

import struct
import binascii
import netaddr

from yabgp.message.attribute.nlri import NLRI


class IPv6Unicast(NLRI):

    @classmethod
    def parse(cls, nlri_data):
        """
        decode IPv6 NLRI data
        :param nlri_data: NLRI raw hex data
        :return: return the results after decoding.
        """
        nlri_list = []
        while nlri_data:
            if isinstance(nlri_data[0], int):
                prefix_bit_len = int(nlri_data[0])
            else:
                prefix_bit_len = struct.unpack('!B', nlri_data[0])[0]
            if prefix_bit_len % 8 == 0:
                prefix_byte_len = prefix_bit_len / 8
            else:
                prefix_byte_len = prefix_bit_len / 8 + 1
            offset = int(prefix_byte_len + 1)
            prefix_addr = str(netaddr.IPAddress(int(binascii.b2a_hex(nlri_data[1:offset]), 16))) \
                + '/%s' % prefix_bit_len
            nlri_list.append(prefix_addr)
            nlri_data = nlri_data[int(prefix_byte_len) + 1:]

        return nlri_list

    @classmethod
    def construct(cls, nlri_list):
        """
        Construct NLRI from list to hex data
        :param nlri_list:
        :return:
        """
        nlri_hex = b''
        for prefix in nlri_list:
            prefix = netaddr.IPNetwork(prefix)
            nlri_hex += struct.pack('!B', prefix.prefixlen)
            nlri_hex += binascii.unhexlify(hex(prefix.ip)[2:])
        return nlri_hex
