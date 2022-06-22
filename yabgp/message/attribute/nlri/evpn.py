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

from __future__ import division
import struct
import binascii

import netaddr
from yabgp.common import afn
from yabgp.common import safn
from yabgp.common import constants as bgp_cons
from yabgp.message.attribute.nlri import NLRI
# from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN


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
            route_value = nlri_data[2: offset + 2]
            route = {}
            if route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY:
                route = EthernetAutoDiscovery.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                route = MacIPAdvertisment.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                route = InclusiveMulticastEthernetTag.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                route = EthernetSegment.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_IP_ROUTE_PREFIX:
                route = IPRoutePrefix.parse(route_value)
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
                nlri_hex = EthernetAutoDiscovery.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                nlri_hex = MacIPAdvertisment.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                nlri_hex = InclusiveMulticastEthernetTag.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                nlri_hex = EthernetSegment.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_IP_ROUTE_PREFIX:
                nlri_hex = IPRoutePrefix.construct(value=nlri['value'])
            if nlri_hex:
                nlri_list_hex += struct.pack('!2B', nlri['type'], len(nlri_hex)) + nlri_hex
        return nlri_list_hex

    @staticmethod
    def signal_evpn_overlay(attr_dict):
        """
        draft-ietf-bess-evpn-overlay-10 changes label encoding if EVPN and encapsulation EC set

        :param attr_dict: bgp attribute dictionary
        """
        evpn_overlay = {'evpn': False, 'encap_ec': False}
        try:
            afi_safi = tuple(attr_dict.get(bgp_cons.BGPTYPE_MP_REACH_NLRI).get('afi_safi'))
            community_ext = attr_dict.get(bgp_cons.BGPTYPE_EXTENDED_COMMUNITY)
        except:
            return evpn_overlay
        if afi_safi == (afn.AFNUM_L2VPN, safn.SAFNUM_EVPN):
            evpn_overlay['evpn'] = True
        if community_ext:
            for ec in community_ext:
                if bgp_cons.BGP_EXT_COM_DICT['encapsulation'] == ec[0]:
                    evpn_overlay['encap_ec'] = True
                    evpn_overlay['encap_value'] = int(ec[1])
        return evpn_overlay

    @classmethod
    def parse_rd(cls, data):
        """
        For Cisco: The BGP route distinguisher can be derived automatically
        from the VNI and BGP router ID of the VTEP switch
        :param data:
        :return:
        """
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

    @classmethod
    def parse_esi(cls, esi):
        """
            The ESI has the following format:
            +---+---+---+---+---+---+---+---+---+---+
            | T |           ESI Value               |
            +---+---+---+---+---+---+---+---+---+---+
        """
        esi_type, esi_value = struct.unpack("!B", esi[:1])[0], {}
        if esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_0:
            esi_value = int.from_bytes(esi[1:], byteorder='big')
        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_1:
            esi_value = {
                "ce_mac_addr": str(netaddr.EUI(int(binascii.b2a_hex(esi[1:7]), 16))),
                "ce_port_key": int.from_bytes(esi[7:9], byteorder='big')
            }
        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_2:
            esi_value = {
                "rb_mac_addr": str(netaddr.EUI(int(binascii.b2a_hex(esi[1:7]), 16))),
                "rb_priority": int.from_bytes(esi[7:9], byteorder='big')
            }
        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_3:
            esi_value = {
                "sys_mac_addr": str(netaddr.EUI(int(binascii.b2a_hex(esi[1:7]), 16))),
                "ld_value": int.from_bytes(esi[7:], byteorder='big')
            }
        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_4:
            esi_value = {
                "router_id": int.from_bytes(esi[1:5], byteorder='big'),
                "ld_value": int.from_bytes(esi[5:9], byteorder='big')
            }
        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_5:
            esi_value = {
                "as_num": int.from_bytes(esi[1:5], byteorder='big'),
                "ld_value": int.from_bytes(esi[5:9], byteorder='big')
            }
        return {"type": esi_type, "value": esi_value}

    @classmethod
    def construct_esi(cls, esi_data):
        esi_type, esi_value = esi_data["type"], esi_data["value"]
        esi_data_hex = b''
        if esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_0:
            esi_bytes = esi_value.to_bytes(9, byteorder='big')
            esi_data_hex = b'\x00' + esi_bytes

        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_1:
            ce_mac_addr, ce_port_key = esi_value["ce_mac_addr"], esi_value["ce_port_key"]
            ce_mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in ce_mac_addr.split("-")])
            ce_port_hex = ce_port_key.to_bytes(2, byteorder='big')
            esi_data_hex = b'\x01' + ce_mac_hex + ce_port_hex + b'\x00'

        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_2:
            rb_mac_addr, rb_priority = esi_value["rb_mac_addr"], esi_value["rb_priority"]
            rb_mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in rb_mac_addr.split("-")])
            rb_priority_hex = rb_priority.to_bytes(2, byteorder='big')
            esi_data_hex = b'\x02' + rb_mac_hex + rb_priority_hex + b'\x00'

        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_3:
            sys_mac_addr, ld_value = esi_value["sys_mac_addr"], esi_value["ld_value"]
            sys_mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in sys_mac_addr.split("-")])
            ld_value_hex = ld_value.to_bytes(3, byteorder='big')
            esi_data_hex = b'\x03' + sys_mac_hex + ld_value_hex

        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_4:
            router_id, ld_value = esi_value["router_id"], esi_value["ld_value"]
            router_id_hex = router_id.to_bytes(4, byteorder='big')
            ld_value_hex = ld_value.to_bytes(4, byteorder='big')
            esi_data_hex = b'\x04' + router_id_hex + ld_value_hex + b'\x00'

        elif esi_type == bgp_cons.ESI_BGPNLRI_EVPN_TYPE_5:
            as_num, ld_value = esi_value["as_num"], esi_value["ld_value"]
            as_num_hex = as_num.to_bytes(4, byteorder='big')
            ld_value_hex = ld_value.to_bytes(4, byteorder='big')
            esi_data_hex = b'\x05' + as_num_hex + ld_value_hex + b'\x00'

        return esi_data_hex


class EthernetAutoDiscovery(EVPN):
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
    def parse(cls, value, iswithdraw=False):
        route = dict()
        route['rd'] = cls.parse_rd(value[0:8])
        offset = 8
        route['esi'] = cls.parse_esi(value[offset: offset + 10])
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset + 4])[0]
        offset += 4
        route['label'] = cls.parse_mpls_label_stack(value[offset:])
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ethernet tag
        value_hex += struct.pack('!I', value['eth_tag_id'])
        value_hex += cls.construct_mpls_label_stack(value['label'])
        return value_hex


class MacIPAdvertisment(EVPN):
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
    def parse(cls, value, iswithdraw=False):
        route = dict()
        # rd
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        # esi
        route['esi'] = cls.parse_esi(value[offset: offset + 10])
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset + 4])[0]
        offset += 5
        # mac address
        route['mac'] = str(netaddr.EUI(int(binascii.b2a_hex(value[offset: offset + 6]), 16)))
        offset += 6
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(
                int(binascii.b2a_hex(value[offset: offset + int(ip_addr_len / 8)]), 16)))
            offset += int(ip_addr_len / 8)
        # label
        route['label'] = cls.parse_mpls_label_stack(value[offset:])
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ethernet tag
        value_hex += struct.pack('!I', value['eth_tag_id'])
        # mac address len and address
        mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in value['mac'].split("-")])
        value_hex += struct.pack('!B', len(mac_hex) * 8) + mac_hex
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        if value.get('label'):
            value_hex += cls.construct_mpls_label_stack(value['label'])
        return value_hex


class InclusiveMulticastEthernetTag(EVPN):
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
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset + 4])[0]
        offset += 4
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(
                netaddr.IPAddress(int(binascii.b2a_hex(value[offset: int(offset + ip_addr_len / 8)]), 16)))
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        value_hex += struct.pack('!I', value['eth_tag_id'])
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        return value_hex


class EthernetSegment(EVPN):
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
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        # esi
        route['esi'] = cls.parse_esi(value[offset: offset + 10])
        offset += 10
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[offset: offset + ip_addr_len // 8]), 16)))
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        return value_hex


class IPRoutePrefix(EVPN):
    """
    # http://tools.ietf.org/html/draft-ietf-bess-evpn-prefix-advertisement-01
    +---------------------------------------+
    |      RD   (8 octets)                  |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  IP Prefix Length (1 octet)           |
    +---------------------------------------+
    |  IP Prefix (4 or 16 octets)           |
    +---------------------------------------+
    |  GW IP Address (4 or 16 octets)       |
    +---------------------------------------+
    |  MPLS Label (3 octets)                |
    +---------------------------------------+
    """
    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        # esi
        route['esi'] = cls.parse_esi(value[offset: offset + 10])
        offset += 10

        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset + 4])[0]
        offset += 4

        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1

        value = value[offset:]
        # The IP Prefix Length can be set to a value between 0 and 32
        #   (bits) for ipv4 and between 0 and 128 for ipv6.
        # The IP Prefix will be a 32 or 128-bit field (ipv4 or ipv6).

        # # ip address
        if len(value) == 11:
            # ipv4
            offset = 4
        elif len(value) == 35:
            # ipv6
            offset = 16

        route['prefix'] = '%s/%s' % (str(netaddr.IPAddress(int(binascii.b2a_hex(value[0: offset]), 16))), ip_addr_len)
        value = value[offset:]
        route['gateway'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[0: offset]), 16)))
        value = value[offset:]

        route['label'] = cls.parse_mpls_label_stack(value)
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        value_hex += struct.pack('!I', value['eth_tag_id'])
        value_hex += struct.pack('!B', int(value['prefix'].split('/')[1]))
        value_hex += netaddr.IPAddress(value['prefix'].split('/')[0]).packed
        value_hex += netaddr.IPAddress(value['gateway']).packed
        value_hex += cls.construct_mpls_label_stack(value['label'])
        return value_hex
