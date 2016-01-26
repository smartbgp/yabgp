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

import netaddr

from yabgp.common import constants as bgp_cons


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

    @classmethod
    def parse_rd(cls, data):
        rd_type = struct.unpack('!H', data[0:2])[0]
        rd_value = data[2:8]
        if rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_0:
            asn, an = struct.unpack('!HI', rd_value)
            rd = '%s:%s' % (asn, an)
        elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_1:
            ip = str(netaddr.IPAddress(struct.unpack('!I', rd_value[0:4])[0]))
            an = struct.unpack('!H', rd_value[4:6])[0]
            rd = '%s:%s' % (ip, an)
        elif rd_type == bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_2:
            asn, an = struct.unpack('!IH', rd_value)
            rd = '%s:%s' % (asn, an)
        else:
            # fixme(by xiaopeng163) for other rd type process
            rd = str(rd_value)
        return rd

    @classmethod
    def construct_rd(cls, data):
        # fixme(by xiaopeng163) for other rd type process
        data = data.split(':')
        if '.' in data[0]:
            return struct.pack('!H', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_1) + netaddr.IPAddress(data[0]).packed + \
                struct.pack('!H', int(data[1]))
        else:
            data = [int(x) for x in data]
            if data[0] <= 0xffff:
                return struct.pack('!HHI', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_0, data[0], data[1])
            else:
                return struct.pack('!HIH', bgp_cons.BGP_ROUTE_DISTINGUISHER_TYPE_2, data[0], data[1])
