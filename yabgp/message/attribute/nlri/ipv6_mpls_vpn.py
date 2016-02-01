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

from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN
from yabgp.common.afn import AFNUM_INET6
from yabgp.common.safn import SAFNUM_LAB_VPNUNICAST


class IPv6MPLSVPN(MPLSVPN):
    """
    IPv6 MPLS VPN NLRI
    """
    AFI = AFNUM_INET6
    SAFI = SAFNUM_LAB_VPNUNICAST

    @classmethod
    def parse(cls, value, iswithdraw=False):
        return super(IPv6MPLSVPN, cls).parse(value, iswithdraw=iswithdraw)

    @classmethod
    def construct(cls, value, iswithdraw=False):
        return super(IPv6MPLSVPN, cls).construct(value, iswithdraw=iswithdraw)
