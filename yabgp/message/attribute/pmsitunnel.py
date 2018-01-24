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

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import constants as bgp_cons


class PMSITunnel(Attribute):
    """
    RFC 6514#section-5
    """
    ID = AttributeID.PMSI_TUNNEL
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value, evpn_overlay=False):
        """
        +---------------------------------+
        |  Flags (1 octet)                |
        +---------------------------------+
        |  Tunnel Type (1 octets)         |
        +---------------------------------+
        |  MPLS Label (3 octets)          |
        +---------------------------------+
        |  Tunnel Identifier (variable)   |
        +---------------------------------+
        :param value raw hex value
        """
        flag = ord(value[0:1])
        tunnel_type = ord(value[1:2])
        if evpn_overlay:
            mpls_label = cls.parse_vni(value[2: 5])
        else:
            mpls_label = cls.parse_mpls_label(value[2: 5])
        tunnel_id = cls.parse_tunnel_id(tunel_type=tunnel_type, tunel_data=value[5:])
        return {
            'leaf_info_required': flag,
            'tunnel_type': tunnel_type,
            'mpls_label': [mpls_label],
            'tunnel_id': tunnel_id
        }

    @staticmethod
    def parse_mpls_label(data):
        label = struct.unpack('!L', b'\00'+data[:3])[0]
        return label >> 4

    @staticmethod
    def parse_vni(data):
        label = struct.unpack('!L', b'\00'+data[:3])[0]
        return label

    @staticmethod
    def parse_tunnel_id(tunel_type, tunel_data):
        if tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_NO_TUNNEL:
            # When the Tunnel Type is set to "No tunnel information present", the
            # PMSI Tunnel attribute carries no tunnel information (no Tunnel
            # Identifier).
            return None
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_RSVP_TE_P2MP:
            # When the Tunnel Type is set to RSVP - Traffic Engineering (RSVP-TE)
            # Point-to-Multipoint (P2MP) Label Switched Path (LSP), the Tunnel
            # Identifier is <Extended Tunnel ID, Reserved, Tunnel ID, P2MP ID> as
            # carried in the RSVP-TE P2MP LSP SESSION Object [RFC4875].
            pass
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_MLDP_P2MP:
            # When the Tunnel Type is set to multipoint Label Distribution Protocol
            # (mLDP) P2MP LSP, the Tunnel Identifier is a P2MP Forwarding
            # Equivalence Class (FEC) Element [mLDP].
            pass
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_PIM_SSM_TREE:
            # When the Tunnel Type is set to PIM-SSM tree, the Tunnel Identifier is
            # <P-Root Node Address, P-Multicast Group>.  The node that originates
            # the attribute MUST use the address carried in the P-Root Node Address
            # as the source IP address for the IP/GRE encapsulation of the MVPN
            # data.  The P-Multicast Group in the Tunnel Identifier of the Tunnel
            # attribute MUST NOT be expected to be the same group for all Intra-AS
            # A-D routes for the same MVPN.  According to [RFC4607], the group
            # address can be locally allocated by the originating PE without any
            # consideration for the group address used by other PE on the same
            # MVPN.
            pass
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_PIM_SM_TREE:
            # When the Tunnel Type is set to Protocol Independent Multicast -
            # Sparse Mode (PIM-SM) tree, the Tunnel Identifier is <Sender Address,
            # P-Multicast Group>.  The node that originated the attribute MUST use
            # the address carried in the Sender Address as the source IP address
            # for the IP/GRE (Generic Routing Encapsulation) encapsulation of the
            # MVPN data.
            pass
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_BIDIR_PIM_TREE:
            # When the Tunnel Type is set to BIDIR-PIM tree, the Tunnel Identifier
            # is <Sender Address, P-Multicast Group>.  The node that originated the
            # attribute MUST use the address carried in the Sender Address as the
            # source IP address for the IP/GRE encapsulation of the MVPN data.
            pass
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_INGRESS_REPL:
            # When the Tunnel Type is set to Ingress Replication, the Tunnel
            # Identifier carries the unicast tunnel endpoint IP address of the
            # local PE that is to be this PE's receiving endpoint address for the
            # tunnel.
            return str(netaddr.IPAddress(int(binascii.b2a_hex(tunel_data), 16)))
        elif tunel_type == bgp_cons.PMSI_TUNNEL_TYPE_MLDP_MP2MP:
            # When the Tunnel Type is set to mLDP Multipoint-to-Multipoint (MP2MP)
            # LSP, the Tunnel Identifier is an MP2MP FEC Element [mLDP].
            pass
        return 'not supported'

    @classmethod
    def construct(cls, value, evpn_overlay=False):
        """
        :param value:
            {
                "mpls_label": [1234],
                "tunnel_id": "192.168.10.10",
                "tunnel_type": 6,
                "leaf_info_required": 0
            }
        """
        pmsi_tunnel_hex = b''
        # Flags: (currently only Leaf Info Required is defined)
        pmsi_tunnel_hex += struct.pack('!B', int(value['leaf_info_required']))
        # Tunnel Type
        pmsi_tunnel_hex += struct.pack('!B', int(value['tunnel_type']))
        # MPLS Label
        pmsi_tunnel_hex += cls.construct_pmsi_label(evpn_overlay, value)
        # tunnel_type dictates the tunnel_id structure
        pmsi_tunnel_hex += cls.construct_tunnel_type(value)
        if pmsi_tunnel_hex:
            return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', len(pmsi_tunnel_hex)) + pmsi_tunnel_hex

    @staticmethod
    def construct_pmsi_label(evpn_overlay, value):
        if not evpn_overlay:
            # MPLS Label
            return struct.pack('!L', value['mpls_label'][0] << 4)[1:]
        else:
            # draft-ietf-bess-evpn-overlay-10#section-5.1.3 - label is used for 24 bit VNI
            if evpn_overlay['evpn'] & evpn_overlay['encap_ec']:
                if evpn_overlay['encap_value'] == bgp_cons.BGP_TUNNEL_ENCAPS_VXLAN:
                    return struct.pack('!L', value['mpls_label'][0])[1:]
                elif evpn_overlay['encap_value'] == bgp_cons.BGP_TUNNEL_ENCAPS_NVGRE:
                    return struct.pack('!L', value['mpls_label'][0])[1:]
            else:
                # MPLS Label
                return struct.pack('!L', value['mpls_label'][0] << 4)[1:]

    @staticmethod
    def construct_tunnel_type(value):
        if value['tunnel_type'] == bgp_cons.PMSI_TUNNEL_TYPE_INGRESS_REPL:
            return netaddr.IPAddress(value['tunnel_id']).packed
        else:
            return ''
