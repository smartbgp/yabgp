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

from yabgp.message.attribute.nlri import NLRI
from yabgp.message.attribute.nlri.mpls_vpn import MPLSVPN


class EVPN(MPLSVPN, NLRI):
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
        pass

    @classmethod
    def construct(cls, nlri_list):
        pass
