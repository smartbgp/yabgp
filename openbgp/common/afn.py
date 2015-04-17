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

"""
Address family numbers, from
http://www.iana.org/assignments/address-family-numbers
"""

AFNUM_RESERVED = 0  # Reserved
AFNUM_INET = 1  # IP (IP version 4)
AFNUM_INET6 = 2  # IP6 (IP version 6)
AFNUM_NSAP = 3  # NSAP
AFNUM_HDLC = 4  # HDLC (8-bit multidrop)
AFNUM_BBN1822 = 5  # BBN 1822
AFNUM_802 = 6  # 802 (includes all 802 media plus Ethernet "canonical format")
AFNUM_E163 = 7  # E.163
AFNUM_E164 = 8  # E.164 (SMDS, Frame Relay, ATM)
AFNUM_F69 = 9  # F.69 (Telex)
AFNUM_X121 = 10  # X.121 (X.25, Frame Relay)
AFNUM_IPX = 11  # IPX
AFNUM_ATALK = 12  # Appletalk
AFNUM_DECNET = 13  # Decnet IV
AFNUM_BANYAN = 14  # Banyan Vines
AFNUM_E164NSAP = 15  # E.164 with NSAP format subaddress
AFNUM_DNS = 16  # DNS (Domain Name System)
AFNUM_DISTNAME = 17  # Distinguished Name
AFNUM_AS_NUMBER = 18  # AS Number
AFNUM_XTP_IP4 = 19  # XTP over IP version 4
AFNUM_XTP_IP6 = 20  # XTP over IP version 6
AFNUM_XTP = 21  # XTP native mode XTP
AFNUM_FC_WWPN = 22  # Fibre Channel World-Wide Port Name
AFNUM_FC_WWNN = 23  # Fibre Channel World-Wide Node Name
AFNUM_GWID = 24  # GWID
# draft-kompella-ppvpn-l2vpn
AFNUM_L2VPN = 25
AFNUM_L2VPN_OLD = 196
AFNUM_EIGRP_COMMON = 16384  # EIGRP Common Service Family
AFNUM_EIGRP_IPV4 = 16385  # EIGRP IPv4 Service Family
AFNUM_EIGRP_IPV6 = 16386  # EIGRP IPv6 Service Family
AFNUM_LCAF = 16387  # LISP Canonical Address Format
AFNUM_BGPLS = 16388  # draft BGP-LS
