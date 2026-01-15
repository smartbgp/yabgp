# Copyright 2025 Cisco Systems, Inc.
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

import struct
import binascii

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV


@LinkState.register()
class FlexAlgorithmDefine(TLV):
    """
    Flex Algorithm Definition TLV (Type 1039)
    RFC 9351 Section 3: https://www.rfc-editor.org/rfc/rfc9351.html#section-3

    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Flex-Algo   |  Metric-Type  |   Calc-Type   |    Priority   |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    +                      Sub-TLVs (variable)                      +
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Fields:
        - Flex-Algo (1 octet): Flexible Algorithm number (128-255)
        - Metric-Type (1 octet): 0=IGP Metric, 1=Min Unidirectional Link Delay, 2=TE Default Metric
        - Calc-Type (1 octet): 0=SPF, 1=Strict SPF
        - Priority (1 octet): Priority of the FAD definition (0-255)
        - Sub-TLVs: Optional sub-TLVs (1040-1044)
    """
    TYPE = 1039
    TYPE_STR = 'flex_algo_defn'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Flex Algorithm Definition TLV

        :param data: binary data (without type and length)
        :return: FlexAlgorithmDefine instance
        """
        # Parse fixed fields (4 bytes)
        flex_algo, metric_type, calc_type, priority = struct.unpack('!BBBB', data[:4])

        # Parse sub-TLVs if present
        sub_tlvs_bin_data = data[4:]
        sub_tlvs = []

        while sub_tlvs_bin_data:
            sub_tlvs_type_code, sub_tlvs_length = struct.unpack('!HH', sub_tlvs_bin_data[:4])
            sub_tlvs_value = sub_tlvs_bin_data[4: 4 + sub_tlvs_length]

            if sub_tlvs_type_code in LinkState.registered_tlvs:
                sub_tlvs.append(LinkState.registered_tlvs[sub_tlvs_type_code].unpack(sub_tlvs_value).dict())
            else:
                sub_tlvs.append({
                    'type': sub_tlvs_type_code,
                    'value': str(binascii.b2a_hex(sub_tlvs_value))
                })
            sub_tlvs_bin_data = sub_tlvs_bin_data[4 + sub_tlvs_length:]

        return cls(value={
            'flex_algo': flex_algo,
            'metric_type': metric_type,
            'calc_type': calc_type,
            'priority': priority,
            'sub_tlvs': sub_tlvs
        })


@LinkState.register()
class FlexAlgoExcludeAdminGroup(TLV):
    """
    Flex-Algorithm Exclude Admin Group TLV (Type 1040)
    RFC 9351 Section 3.1: https://www.rfc-editor.org/rfc/rfc9351.html#section-3.1

    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                  Extended Admin Group                         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              ...                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Contains Extended Admin Group bitmask (variable length, 4 octets per group).
    Links with any bit set that matches any bit in this bitmask are excluded.
    """
    TYPE = 1040
    TYPE_STR = 'flex_algo_excl_admin_group'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Extended Admin Group

        :param data: binary data
        :return: list of 32-bit admin group values
        """
        admin_groups = []
        for i in range(0, len(data), 4):
            admin_groups.append(struct.unpack('!I', data[i:i+4])[0])
        return cls(value=admin_groups)


@LinkState.register()
class FlexAlgoIncludeAnyAdminGroup(TLV):
    """
    Flex-Algorithm Include-Any Admin Group TLV (Type 1041)
    RFC 9351 Section 3.2: https://www.rfc-editor.org/rfc/rfc9351.html#section-3.2

    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                  Extended Admin Group                         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              ...                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Contains Extended Admin Group bitmask (variable length, 4 octets per group).
    Links with any bit set that matches any bit in this bitmask are included.
    """
    TYPE = 1041
    TYPE_STR = 'flex_algo_incl_any_admin_group'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Extended Admin Group

        :param data: binary data
        :return: list of 32-bit admin group values
        """
        admin_groups = []
        for i in range(0, len(data), 4):
            admin_groups.append(struct.unpack('!I', data[i:i+4])[0])
        return cls(value=admin_groups)


@LinkState.register()
class FlexAlgoIncludeAllAdminGroup(TLV):
    """
    Flex-Algorithm Include-All Admin Group TLV (Type 1042)
    RFC 9351 Section 3.3: https://www.rfc-editor.org/rfc/rfc9351.html#section-3.3


    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                  Extended Admin Group                         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              ...                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Contains Extended Admin Group bitmask (variable length, 4 octets per group).
    Links must have all bits set that match all bits in this bitmask to be included.
    """
    TYPE = 1042
    TYPE_STR = 'flex_algo_incl_all_admin_group'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Extended Admin Group

        :param data: binary data
        :return: list of 32-bit admin group values
        """
        admin_groups = []
        for i in range(0, len(data), 4):
            admin_groups.append(struct.unpack('!I', data[i:i+4])[0])
        return cls(value=admin_groups)


@LinkState.register()
class FlexAlgoDefinitionFlags(TLV):
    """
    Flex-Algorithm Definition Flags TLV (Type 1043)
    RFC 9351 Section 3.4: https://www.rfc-editor.org/rfc/rfc9351.html#section-3.4


    Format:
     0                   1
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |M|          Reserved           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Flags:
        M-flag (bit 0): If set, the Flex-Algorithm specific prefix and ASBR metric
                        MUST be used for inter-area and external prefix calculation.
        Reserved: Must be zero on transmission and ignored on reception.
    """
    TYPE = 1043
    TYPE_STR = 'flex_algo_defn_flags'

    @classmethod
    def unpack(cls, data):
        """
        Unpack Flex-Algorithm Definition Flags

        :param data: binary data (2 bytes)
        :return: dict with flag values
        """
        flags = struct.unpack('!H', data[:2])[0]
        flag = {
            'M': flags >> 15  # M-flag is the most significant bit
        }
        return cls(value=flag)


@LinkState.register()
class FlexAlgoExcludeSRLG(TLV):
    """
    Flex-Algorithm Exclude SRLG TLV (Type 1044)
    RFC 9351 Section 3.5: https://www.rfc-editor.org/rfc/rfc9351.html#section-3.5


    Format:
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         SRLG Value 1                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         SRLG Value 2                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              ...                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         SRLG Value N                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Contains list of 32-bit SRLG (Shared Risk Link Group) values.
    Links with any SRLG value matching any value in this list are excluded.
    """
    TYPE = 1044
    TYPE_STR = 'flex_algo_excl_srlg'

    @classmethod
    def unpack(cls, data):
        """
        Unpack SRLG list

        :param data: binary data
        :return: list of 32-bit SRLG values
        """
        srlg_list = []
        for i in range(0, len(data), 4):
            srlg_list.append(struct.unpack('!I', data[i:i+4])[0])
        return cls(value=srlg_list)
