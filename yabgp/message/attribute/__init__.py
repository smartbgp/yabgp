# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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

from struct import pack


class AttributeFlag(int):
    """
    +-------------------------------------------+
    | bit 0 | bit 1 | bit 2 | bit 3 | bit 4 - 7 |
    +-------------------------------------------+
    bit 0:
        It defines whether the attribute is optional (if set to 1)
    or well-known (if set to 0).
    bit 1:
        It defines whether an optional attribute is transitive
    (if set to 1) or non-transitive (if set to 0).
        For well-known attributes, the Transitive bit MUST be set to 1.
    bit 2:
        It defines whether the information contained in the optional
    transitive attribute is partial (if set to 1) or complete (if set to 0).
    For well-known attributes and for optional non-transitive attributes,
    the Partial bit MUST be set to 0.
    bit 3:
        It defines whether the Attribute Length is one octet
    (if set to 0) or two octets (if set to 1).
    bit 4 - 7
        The lower-order four bits of the Attribute Flags octet are
    unused. They MUST be zero when sent and MUST be ignored when
    received.
    """

    EXTENDED_LENGTH = 0x10  # 16  RFC 4271
    PARTIAL = 0x20  # 32  RFC 4271
    TRANSITIVE = 0x40  # 64  RFC 4271
    OPTIONAL = 0x80  # 128 RFC 4271

    def __str_(self):
        r = []
        v = int(self)
        if v & 0x10:
            r.append("EXTENDED_LENGTH")
            v -= 0x10
        if v & 0x20:
            r.append("PARTIAL")
            v -= 0x20
        if v & 0x40:
            r.append("TRANSITIVE")
            v -= 0x40
        if v & 0x80:
            r.append("OPTIONAL")
            v -= 0x80
        if v:
            r.append("UNKNOWN %s" % hex(v))
        return " ".join(r)


# ============================================ Attribute Type code
#  http://www.iana.org/assignments/bgp-parameters/bgp-parameters.xml
#  update 2011-9-26


class AttributeID(int):
    """
    Attribute Type Code
    """

    ORIGIN = 0x01  # 1   [RFC4271]
    AS_PATH = 0x02  # 2   [RFC4271]
    NEXT_HOP = 0x03  # 3   [RFC4271]
    MULTI_EXIT_DISC = 0x04  # 4   [RFC4271]
    LOCAL_PREF = 0x05  # 5   [RFC4271]
    ATOMIC_AGGREGATE = 0x06  # 6   [RFC4271]
    AGGREGATOR = 0x07  # 7   [RFC4271]
    COMMUNITY = 0x08  # 8   [RFC1997]
    ORIGINATOR_ID = 0x09  # 9   [RFC4456]
    CLUSTER_LIST = 0x0a  # 10  [RFC4456]
    # DPA                                     = 0x0b  # 11  [Chen, E., Bates, T., "Destination Preference Attribute for
    # BGP", Work in progress, March 1996.]
    # ADVERTISER (Historic)                   = 0x0c  # 12  [RFC1863][RFC4223]
    # RCID_PATH / CLUSTER_ID (Historic)       = 0x0d  # 13  [RFC1863][RFC4223]
    MP_REACH_NLRI = 0x0e  # 14  [RFC4760]
    MP_UNREACH_NLRI = 0x0f  # 15  [RFC4760]
    EXTENDED_COMMUNITY = 0x10  # 16  [Eric_Rosen][draft-ramachandra-bgp-ext-communities-00][RFC4360]
    AS4_PATH = 0x11  # 17  [RFC4893]
    AS4_AGGREGATOR = 0x12  # 18  [RFC4893]
    # SAFI_Specific_Attribute                 = 0x13  # 19  [Gargi_Nalawade]
    # [draft-kapoor-nalawade-idr-bgp-ssa-00][draft-nalawade-idr-mdt-safi-00][draft-wijnands-mt-discovery-00]
    # (SSA)(deprecated)
    # Connector_Attribute                     = 0x14  # 20  [RFC6037] (deprecated)
    # AS_PATHLIMIT (deprecated)               = 0x15  # 21  [draft-ietf-idr-as-pathlimit]
    PMSI_TUNNEL = 0x16  # 22  [RFC-ietf-l3vpn-2547bis-mcast-bgp-08]
    Tunnel_Encapsulation_Attribute = 0x17  # 23  [RFC5512]
    Traffic_Engineering = 0x18  # 24  [RFC5543]
    IPv6_Address_Specific_Extended_Community = 0x19  # 25  [RFC5701]
    # AIGP                                    = 0x1a  # 26  [draft-ietf-idr-aigp](TEMPORARY - expires 2012-03-14)

    ATTR_SET = 0x80  # 128 [RFC6368]

    Unassigned = list(range(27, 127)) + list(range(129, 254))
    Reserved_For_Development = 255

    def __str__(self):

        # This should move within the classes and not be here
        if self == 0x01:
            return "ORIGIN"
        if self == 0x02:
            return "AS_PATH"
        if self == 0x03:
            return "NEXT_HOP"
        if self == 0x04:
            return "MULTI_EXIT_DISC"
        if self == 0x05:
            return "LOCAL_PREFERENCE"
        if self == 0x06:
            return "ATOMIC_AGGREGATE"
        if self == 0x07:
            return "AGGREGATOR"
        if self == 0x08:
            return "COMMUNITY"
        if self == 0x09:
            return "ORIGINATOR_ID"
        if self == 0x0a:
            return "CLUSTER_LIST"
        if self == 0x10:
            return "EXTENDED_COMMUNITY"
        if self == 0x11:
            return "AS4_PATH"
        if self == 0x12:
            return "AS4_AGGREGATOR"
        if self == 0x0e:
            return "MP_REACH_NLRI"
        if self == 0x0f:
            return "MP_UNREACH_NLRI"
        if self == 0xffff:
            return "INTERNAL SPLIT"
        return 'UNKNOWN ATTRIBUTE (%s)' % hex(self)


class Attribute(object):
    """
    Base class for all BGP attribute classes
    Attribute instances are (meant to be) immutable once initialized
    """
    ID = 0x00
    FLAG = 0x00

    def _attribute(self, value):
        flag = self.FLAG
        if flag & AttributeFlag.OPTIONAL and not value:
            return ''
        length = len(value)
        if length > 0xFF:
            flag &= AttributeFlag.EXTENDED_LENGTH
        if flag & AttributeFlag.EXTENDED_LENGTH:
            len_value = pack('!H', length)[0]
        else:
            len_value = chr(length)
        return "%s%s%s%s" % (chr(flag), chr(self.ID), len_value, value)

    def __eq__(self, other):
        return self.ID == other.ID
