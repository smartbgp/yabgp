# Copyright 2016 Cisco Systems, Inc.
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

import struct
import binascii

import netaddr


class NLRI(object):

    @classmethod
    def parse(cls, *args):

        raise NotImplementedError

    @classmethod
    def construct(cls, *args):
        raise NotImplementedError

    @staticmethod
    def construct_prefix_v4(masklen, prefix_str):
        ip_hex = struct.pack('!I', netaddr.IPNetwork(prefix_str).value)
        if 16 < masklen <= 24:
            ip_hex = ip_hex[0:3]
        elif 8 < masklen <= 16:
            ip_hex = ip_hex[0:2]
        elif masklen <= 8:
            ip_hex = ip_hex[0:1]
        return ip_hex

    @staticmethod
    def construct_prefix_v6(prefix):
        mask = int(prefix.split('/')[1])
        prefix_hex = binascii.unhexlify(hex(netaddr.IPNetwork(prefix).ip)[2:])
        offset = mask / 8
        offset_re = mask % 8
        if offset == 0:
            return prefix_hex[0: 1]
        return prefix_hex[0: offset + offset_re]

    @classmethod
    def parse_mpls_label_stack(cls, data):
        labels = []
        while len(data) >= 3:
            label = struct.unpack('!L', b'\00'+data[:3])[0]
            data = data[3:]
            labels.append(label >> 4)
            if label & 0x001:
                break
        return labels

    @classmethod
    def construct_mpls_label_stack(cls, labels):
        data = b''
        last_label = labels[-1]
        for label in labels[:-1]:
            data += struct.pack('!L', label << 4)[1:]
        if last_label != 0:
            data += struct.pack('!L', (last_label << 4 | 1))[1:]
        else:
            data += b'\x00\x00\x00'
        return data
