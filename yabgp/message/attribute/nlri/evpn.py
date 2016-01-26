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

from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri import NLRI
from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN


class EVPN(NLRI):
    """
      The format of the EVPN NLRI is as follows:
    +-----------------------------------+
    |    Route Type (1 octet)           |
    +-----------------------------------+
    |     Length (1 octet)              |
    +-----------------------------------+
    | Route Type specific (variable)    |
    +-----------------------------------+
    """

    @classmethod
    def parse(cls, nlri_data):
        nlri_list = []
        while nlri_data:
            route_type = ord(nlri_data[0:1])
            offset = ord(nlri_data[1:2])
            route_data = nlri_data[2: offset + 2]
            route = {}
            if route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY:
                route = EthernetAutoDiscovery.parse(route_data)
            elif route_type == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                route = MacIPAdvertisment.parse(route_data)
            elif route_type == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                route = InclusiveMulticastEthernetTag.parse(route_data)
            elif route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                route = EthernetSegment.parse(route_data)
            if route:
                nlri_list.append({
                    'type': route_type,
                    'value': route
                })
            nlri_data = nlri_data[offset + 2:]
        return nlri_list

    @classmethod
    def construct(cls, nlri_list):
        nlri_list_hex = b''
        for nlri in nlri_list:
            nlri_hex = b''
            if nlri['type'] == bgp_cons.BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY:
                nlri_hex = EthernetAutoDiscovery.construct(data=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                nlri_hex = MacIPAdvertisment.construct(data=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                nlri_hex = InclusiveMulticastEthernetTag.construct(data=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                nlri_hex = EthernetSegment.construct(data=nlri['value'])
            if nlri_hex:
                nlri_list_hex += struct.pack('!2B', nlri['type'], len(nlri_hex)) + nlri_hex
        return nlri_list_hex


class EthernetAutoDiscovery(MPLSVPN):
    """
    +---------------------------------------+
    |  Route Distinguisher (RD) (8 octets)  |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  MPLS Label (3 octets)                |
    +---------------------------------------+

    """
    @classmethod
    def parse(cls, data):
        route = dict()
        route['rd'] = cls.parse_rd(data[0:8])
        offset = 8
        route['esi'] = int(binascii.b2a_hex(data[offset: offset+10]), 16)
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', data[offset: offset+4])[0]
        offset += 4
        route['label'] = MPLSVPN.parse_mpls_label_stack(data[offset:])
        return route

    @classmethod
    def construct(cls, data):
        # rd
        data_hex = b''
        data_hex += MPLSVPN.construct_rd(data['rd'])
        # esi
        data_hex += b'\x00\x00' + struct.pack('!d', data['esi'])
        # ethernet tag
        data_hex += struct.pack('!I', data['eth_tag_id'])
        data_hex += MPLSVPN.construct_mpls_label_stack(data['label'])
        return data_hex


class MacIPAdvertisment(MPLSVPN):
    """
    +---------------------------------------+
    |  RD (8 octets)                        |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  MAC Address Length (1 octet)         |
    +---------------------------------------+
    |  MAC Address (6 octets)               |
    +---------------------------------------+
    |  IP Address Length (1 octet)          |
    +---------------------------------------+
    |  IP Address (0, 4, or 16 octets)      |
    +---------------------------------------+
    |  MPLS Label1 (3 octets)               |
    +---------------------------------------+
    |  MPLS Label2 (0 or 3 octets)          |
    +---------------------------------------+
    """

    @classmethod
    def parse(cls, data):
        route = dict()
        # rd
        offset = 8
        route['rd'] = cls.parse_rd(data[0:offset])
        # esi
        route['esi'] = int(binascii.b2a_hex(data[offset: offset+10]), 16)
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', data[offset: offset+4])[0]
        offset += 5
        # mac address
        route['mac'] = str(netaddr.EUI(int(binascii.b2a_hex(data[offset: offset+6]), 16)))
        offset += 6
        ip_addr_len = ord(data[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(data[offset: offset + int(ip_addr_len / 8)]), 16)))
            offset += int(ip_addr_len / 8)
        # label
        route['label'] = MPLSVPN.parse_mpls_label_stack(data[offset:])
        return route

    @classmethod
    def construct(cls, data):
        # rd
        data_hex = b''
        data_hex += MPLSVPN.construct_rd(data['rd'])
        # esi
        data_hex += b'\x00\x00' + struct.pack('!d', data['esi'])
        # ethernet tag
        data_hex += struct.pack('!I', data['eth_tag_id'])
        # mac address len and address
        mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in data['mac'].split("-")])
        data_hex += struct.pack('!B', len(mac_hex) * 8) + mac_hex
        # ip address len and address
        if data.get('ip'):
            ip_hex = netaddr.IPAddress(data['ip']).packed
            data_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            data_hex += b'\x00'
        if data.get('label'):
            data_hex += MPLSVPN.construct_mpls_label_stack(data['label'])
        return data_hex


class InclusiveMulticastEthernetTag(MPLSVPN):
    """
   +---------------------------------------+
   |  RD (8 octets)                        |
   +---------------------------------------+
   |  Ethernet Tag ID (4 octets)           |
   +---------------------------------------+
   |  IP Address Length (1 octet)          |
   +---------------------------------------+
   |  Originating Router's IP Address      |
   |          (4 or 16 octets)             |
   +---------------------------------------+
    """

    @classmethod
    def parse(cls, data):
        route = dict()
        offset = 8
        route['rd'] = MPLSVPN.parse_rd(data[0:offset])
        route['eth_tag_id'] = struct.unpack('!I', data[offset: offset+4])[0]
        offset += 4
        ip_addr_len = ord(data[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(data[offset: offset+ip_addr_len / 8]), 16)))
        return route

    @classmethod
    def construct(cls, data):
        # rd
        data_hex = b''
        data_hex += MPLSVPN.construct_rd(data['rd'])
        data_hex += struct.pack('!I', data['eth_tag_id'])
        # ip address len and address
        if data.get('ip'):
            ip_hex = netaddr.IPAddress(data['ip']).packed
            data_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            data_hex += b'\x00'
        return data_hex


class EthernetSegment(MPLSVPN):
    """
   +---------------------------------------+
   |  RD (8 octets)                        |
   +---------------------------------------+
   |Ethernet Segment Identifier (10 octets)|
   +---------------------------------------+
   |  IP Address Length (1 octet)          |
   +---------------------------------------+
   |  Originating Router's IP Address      |
   |          (4 or 16 octets)             |
   +---------------------------------------+

    """
    @classmethod
    def parse(cls, data):
        route = dict()
        offset = 8
        route['rd'] = MPLSVPN.parse_rd(data[0:offset])
        # esi
        route['esi'] = int(binascii.b2a_hex(data[offset: offset+10]), 16)
        offset += 10
        ip_addr_len = ord(data[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(data[offset: offset+ip_addr_len / 8]), 16)))
        return route

    @classmethod
    def construct(cls, data):
        # rd
        data_hex = b''
        data_hex += MPLSVPN.construct_rd(data['rd'])
        # esi
        data_hex += b'\x00\x00' + struct.pack('!d', data['esi'])
        # ip address len and address
        if data.get('ip'):
            ip_hex = netaddr.IPAddress(data['ip']).packed
            data_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            data_hex += b'\x00'
        return data_hex
