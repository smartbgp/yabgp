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
"""linkstate
"""

import struct
import binascii

import netaddr

from yabgp.message.attribute.nlri import NLRI


class BGPLS(NLRI):
    """BGPLS
    """
    NODE_NLRI = 1
    LINK_NLRI = 2
    IPv4_TOPO_PREFIX_NLRI = 3
    IPv6_TOPO_PREFIX_NLRI = 4

    @classmethod
    def parse(cls, nlri_data):
        nlri_list = []
        while nlri_data:
            _type, length = struct.unpack('!HH', nlri_data[0:4])
            value = nlri_data[4: 4 + length]
            nlri_data = nlri_data[4+length:]
            nlri = dict()
            if _type == cls.LINK_NLRI:
                nlri['type'] = 'link'
            elif _type == cls.NODE_NLRI:
                nlri['type'] = 'node'
            elif _type == cls.IPv4_TOPO_PREFIX_NLRI:
                nlri['type'] = 'ipv4-topo-prefix'
            elif _type == cls.IPv6_TOPO_PREFIX_NLRI:
                nlri['type'] = 'ipv6-topo-prefix'
            else:
                nlri['type'] = 'unknown'
                continue
            nlri['value'] = cls.parse_nlri(value)
            nlri_list.append(nlri)
        return nlri_list

    @classmethod
    def parse_nlri(cls, data):
        """parse nlri: node, link, prefix
        """
        #      0                   1                   2                   3
        #      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #     +-+-+-+-+-+-+-+-+
        #     |  Protocol-ID  |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     |                           Identifier                          |
        #     |                            (64 bits)                          |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //               Local Node Descriptors (variable)             //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //               Remote Node Descriptors (variable)            //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //                  Link Descriptors (variable)                //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #                     Figure 8: The Link NLRI format
        return_data = []
        # proto_id = struct.unpack('!B', data[0])[0]
        descriptors = data[9:]
        while descriptors:
            _type, length = struct.unpack('!HH', descriptors[0:4])
            value = descriptors[4: 4+length]
            descriptors = descriptors[4+length:]
            descriptor = dict()
            if _type == 256:  # local node
                descriptor['type'] = 'local-node'
                descriptor['value'] = cls.parse_node_descriptor(value)

            elif _type == 257:  # remote node
                descriptor['type'] = 'remote-node'
                descriptor['value'] = cls.parse_node_descriptor(value)
            # elif _type == 258:  # link local/remote identifier
            #     pass
            elif _type == 259:  # ipv4 interface address
                ipv4_addr = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
                descriptor['type'] = 'link-local-ipv4'
                descriptor['value'] = ipv4_addr
            elif _type == 260:  # ipv4 neighbor address
                ipv4_neighbor_addr = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
                descriptor['type'] = 'link-remote-ipv4'
                descriptor['value'] = ipv4_neighbor_addr
            elif _type == 265:   # IP Reachability Information
                descriptor['type'] = 'prefix'
                mask = struct.unpack('!B', value[0])[0]
                if value[1:]:
                    ip_str = str(netaddr.IPAddress(int(binascii.b2a_hex(value[1:]), 16)))
                else:
                    ip_str = '0.0.0.0'
                descriptor['value'] = "%s/%s" % (ip_str, mask)
            else:
                descriptor['type'] = _type
                descriptor['value'] = binascii.b2a_hex(value)
            return_data.append(descriptor)
        return return_data

    @classmethod
    def parse_node_descriptor(cls, data):

        # +--------------------+-------------------+----------+
        # | Sub-TLV Code Point | Description       |   Length |
        # +--------------------+-------------------+----------+
        # |        512         | Autonomous System |        4 |
        # |        513         | BGP-LS Identifier |        4 |
        # |        514         | OSPF Area-ID      |        4 |
        # |        515         | IGP Router-ID     | Variable |
        # +--------------------+-------------------+----------+
        return_data = dict()
        while data:
            _type, length = struct.unpack('!HH', data[0: 4])
            value = data[4: 4+length]
            data = data[4+length:]
            if _type == 512:
                return_data['as'] = int(binascii.b2a_hex(value), 16)
            elif _type == 513:
                return_data['bgpls-id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
            elif _type == 514:
                return_data['ospf-id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
            elif _type == 515:
                return_data['igp-id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
        return return_data

    @classmethod
    def parse_link_descriptor(cls, data):

        # +-----------+---------------------+--------------+------------------+
        # |  TLV Code | Description         |  IS-IS TLV   | Reference        |
        # |   Point   |                     |   /Sub-TLV   | (RFC/Section)    |
        # +-----------+---------------------+--------------+------------------+
        # |    258    | Link Local/Remote   |     22/4     | [RFC5307]/1.1    |
        # |           | Identifiers         |              |                  |
        # |    259    | IPv4 interface      |     22/6     | [RFC5305]/3.2    |
        # |           | address             |              |                  |
        # |    260    | IPv4 neighbor       |     22/8     | [RFC5305]/3.3    |
        # |           | address             |              |                  |
        # |    261    | IPv6 interface      |    22/12     | [RFC6119]/4.2    |
        # |           | address             |              |                  |
        # |    262    | IPv6 neighbor       |    22/13     | [RFC6119]/4.3    |
        # |           | address             |              |                  |
        # |    263    | Multi-Topology      |     ---      | Section 3.2.1.5  |
        # |           | Identifier          |              |                  |
        pass
