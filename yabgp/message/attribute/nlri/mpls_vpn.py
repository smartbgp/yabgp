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


class MPLSVPN(object):
    """The base class for ipv4/ipv6 mpls vpn
    """
    WITHDARW_LABEL_HEX = b'\x80\x00\x00'
    WITHDARW_LABEL = 524288

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
    def construct_mpls_label_stack(cls, labels, bos=True):
        data = b''
        for label in labels:
            if bos:
                data += struct.pack('!L', (label << 4 | 1))[1:]
                continue
            data += struct.pack('!L', label << 4)[1:]
        return data
