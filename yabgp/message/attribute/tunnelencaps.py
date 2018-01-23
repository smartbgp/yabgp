# Copyright 2015-2017 Cisco Systems, Inc.
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

"""BGP Attribute MP_REACH_NLRI
"""

import struct

import netaddr

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID
from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep


class TunnelEncaps(Attribute):
    """
        Tunnel_Encapsulation_Attribute coding information
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |    Tunnel Type (2 Octets)     |        Length (2 Octets)      |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                                                               |
        |                             Value                             |
        |                                                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        the field of Value consists of sub-TLVs

        sub-TLVs coding information
        +-----------------------------------+
        |      Sub-TLV Type (1 Octet)       |
        +-----------------------------------+
        |     Sub-TLV Length (1 Octet)      |
        +-----------------------------------+
        |     Sub-TLV Value (Variable)      |
        |                                   |
        +-----------------------------------+
    """

    ID = AttributeID.Tunnel_Encapsulation_Attribute
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def construct_optional_label_sid(cls, value):
        items = value.keys()
        label = value['label'] << 12
        tra_cls = 0
        btt_stack = 0
        ttl = 0
        if 'TC' in items:
            tra_cls = value['TC'] << 9
        else:
            tra_cls = 0
        if 'S' in items:
            btt_stack = value['S'] << 8
        else:
            btt_stack = 0
        if 'TTL' in items:
            ttl = value['TTL']
        else:
            ttl = 255
        return label + tra_cls + btt_stack + ttl

    @classmethod
    def construct_weight_and_seg(cls, segment_list):
        weight_hex = b''
        if bgp_cons.BGPSUB_TLV_WEIGHTED in segment_list.keys():
            weight_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_WEIGHTED) + struct.pack('!B', 6) + b'\x00\x00' +\
                struct.pack('!I', segment_list[bgp_cons.BGPSUB_TLV_WEIGHTED])
        seg_hex = b''
        for seg in segment_list[bgp_cons.BGPSUB_TLV_SID]:
            seg_type = int(seg.keys()[0])
            if seg_type == bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_MPLS:
                value = seg[seg.keys()[0]]
                sum_value = cls.construct_optional_label_sid(value)
                seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_MPLS) + struct.pack('!B', 6) + b'\x00\x00' +\
                    struct.pack('!I', sum_value)
            # 3
            elif seg_type == bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_SID:
                value = seg[seg.keys()[0]]
                ipv4_node = value['node']
                if "SID" not in value.keys():
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_SID) + struct.pack('!B', 6) + b'\x00\x00' +\
                        netaddr.IPAddress(ipv4_node).packed
                else:
                    opt_sid = value['SID']
                    sum_value = cls.construct_optional_label_sid(opt_sid)
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_SID) + struct.pack('!B', 10) + b'\x00\x00' +\
                        netaddr.IPAddress(ipv4_node).packed + struct.pack('!I', sum_value)
            # 5
            elif seg_type == bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_INDEX_SID:
                value = seg[seg.keys()[0]]
                local_int = value['interface']
                ipv4_node = value['node']
                if "SID" not in value.keys():
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_INDEX_SID) +\
                        struct.pack('!B', 10) + b'\x00\x00' + struct.pack('!I', local_int) +\
                        netaddr.IPAddress(ipv4_node).packed
                else:
                    opt_sid = value['SID']
                    sum_value = cls.construct_optional_label_sid(opt_sid)
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_INDEX_SID) +\
                        struct.pack('!B', 14) + b'\x00\x00' + struct.pack('!I', local_int) +\
                        netaddr.IPAddress(ipv4_node).packed + struct.pack('!I', sum_value)
            # 6
            elif seg_type == bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_ADDR_SID:
                value = seg[seg.keys()[0]]
                local_ipv4 = value['local']
                remote_ipv4 = value['remote']
                if "SID" not in value.keys():
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_ADDR_SID) + struct.pack('!B', 10) +\
                        b'\x00\x00' + netaddr.IPAddress(local_ipv4).packed + netaddr.IPAddress(remote_ipv4).packed
                else:
                    opt_sid = value['SID']
                    sum_value = cls.construct_optional_label_sid(opt_sid)
                    seg_hex += struct.pack('!B', bgp_cons.BGP_SRTE_SEGMENT_SUBTLV_IPV4_ADDR_SID) + struct.pack('!B', 14) +\
                        b'\x00\x00' + netaddr.IPAddress(local_ipv4).packed + netaddr.IPAddress(remote_ipv4).packed +\
                        struct.pack('!I', sum_value)
        return weight_hex, seg_hex

    @classmethod
    def construct(cls, value):

        """Construct a attribute

        :param value: python dictionary
        {
            "0": "old",
            "6": 100,
            "7": 25102,
            "128": [
                {
                    "9": 10,
                    "1": [
                        {
                            "1": {
                                "label": 2000
                            }
                        },
                        {
                            "3": {
                                "node": "10.1.1.1",
                                "SID": {
                                    "label": 3000,
                                    "TC": 0,
                                    "S": 0,
                                    "TTL": 255
                                }
                            }
                        }
                    ]
                }
            ]
        }
        """
        policy_hex = b''
        policy = value
        data = dict([(int(l), r) for (l, r) in policy.items()])
        policy_value_hex = b''
        items = data.keys()
        if bgp_cons.BGP_BSID_PREFERENCE_OLD_OR_NEW not in items:
            raise excep.ConstructAttributeFailed(
                reason='failed to construct attributes: %s' % 'please provide the value of TLV encoding',
                data={}
            )
        for type_tmp in items:
            if type_tmp == bgp_cons.BGP_BSID_PREFERENCE_OLD_OR_NEW:
                # format of binding sid is same with the mpls label
                # the high order 20 bit was truly used as the bsid
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |          Label                        |           ...         |
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # old ios
                if data[type_tmp] == 'old':
                    # Preference Sub-TLV
                    if bgp_cons.BGPSUB_TLV_PREFERENCE not in items:
                        if bgp_cons.BGPSUB_TLV_PREFERENCE_NEW in items:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_PREFERENCE) + struct.pack('!B', 6) + \
                                b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_PREFERENCE_NEW])
                    else:
                        policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_PREFERENCE) + struct.pack('!B', 6) + \
                            b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_PREFERENCE])
                    # Binding SID Sub-TLV
                    if bgp_cons.BGPSUB_TLV_BINDGINGSID not in items:
                        if bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW not in items:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID) + struct.pack('!B', 2) +\
                                b'\x00\x00'
                        else:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID) + struct.pack('!B', 6) +\
                                b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW] << 12)
                    else:
                        policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID) + struct.pack('!B', 6) +\
                            b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_BINDGINGSID] << 12)
                # new ios
                elif data[type_tmp] == 'new':
                    # Preference Sub-TLV
                    if bgp_cons.BGPSUB_TLV_PREFERENCE not in items:
                        if bgp_cons.BGPSUB_TLV_PREFERENCE_NEW in items:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_PREFERENCE_NEW) + struct.pack('!B', 6) + \
                                b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_PREFERENCE_NEW])
                    else:
                        policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_PREFERENCE_NEW) + struct.pack('!B', 6) + \
                            b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_PREFERENCE])
                    # Binding SID Sub-TLV
                    if bgp_cons.BGPSUB_TLV_BINDGINGSID not in items:
                        if bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW not in items:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW) + struct.pack('!B', 2) +\
                                b'\x00\x00'
                        else:
                            policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW) + struct.pack('!B', 6) +\
                                b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW] << 12)
                    else:
                        policy_value_hex += struct.pack('!B', bgp_cons.BGPSUB_TLV_BINDGINGSID_NEW) + struct.pack('!B', 6) +\
                            b'\x00\x00' + struct.pack('!I', data[bgp_cons.BGPSUB_TLV_BINDGINGSID] << 12)
                else:
                    raise excep.ConstructAttributeFailed(
                        reason='failed to construct attributes: %s' % 'TLV encoding must be one value of new or old',
                        data={}
                    )
            if type_tmp == bgp_cons.BGPSUB_TLV_SIDLIST:
                # Sub_TLV segment list
                seg_list_hex = b''
                for seg_list in data[type_tmp]:
                    segment_list = dict([(int(l), r) for (l, r) in seg_list.items()])
                    weight_hex, seg_hex = cls.construct_weight_and_seg(segment_list)
                    seg_list_hex += struct.pack('!B', type_tmp) + struct.pack('!H', len(weight_hex) + len(seg_hex) + 1) +\
                        b'\x00' + weight_hex + seg_hex
                policy_value_hex += seg_list_hex
        policy_hex += struct.pack('!H', bgp_cons.BGP_TUNNEL_ENCAPS_SR_TE_POLICY_TYPE) +\
            struct.pack('!H', len(policy_value_hex)) + policy_value_hex
        return struct.pack('!B', cls.FLAG) + struct.pack('!B', cls.ID) + struct.pack('!B', len(policy_hex)) + policy_hex
