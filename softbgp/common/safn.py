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

"""RFC 2858 subsequent address family numbers"""

SAFNUM_UNICAST = 1
SAFNUM_MULCAST = 2
SAFNUM_UNIMULC = 3
SAFNUM_MPLS_LABEL = 4  # rfc3107
SAFNUM_MCAST_VPN = 5  # draft-ietf-l3vpn-2547bis-mcast-bgp-08.txt
SAFNUM_ENCAPSULATION = 7  # rfc5512
SAFNUM_TUNNEL = 64  # draft-nalawade-kapoor-tunnel-safi-02.txt
SAFNUM_VPLS = 65
SAFNUM_MDT = 66  # rfc6037
SAFNUM_BGPLS = 71
SAFNUM_LAB_VPNUNICAST = 128  # Draft-rosen-rfc2547bis-03
SAFNUM_LAB_VPNMULCAST = 129
SAFNUM_LAB_VPNUNIMULC = 130
SAFNUM_ROUTE_TARGET = 132  # RFC 4684 Constrained Route Distribution for BGP/MPLS IP VPN
SAFNUM_FSPEC_RULE = 133  # RFC 5575 BGP flow spec SAFI
SAFNUM_FSPEC_VPN_RULE = 134  # RFC 5575 BGP flow spec SAFI VPN
