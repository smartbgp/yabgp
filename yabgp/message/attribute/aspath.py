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

import struct

from yabgp.common import constants as bgp_cons
from yabgp.common import exception as excep
from yabgp.message.attribute import Attribute, AttributeFlag, AttributeID


class ASPath(Attribute):
    """
        AS_PATH is a well-known mandatory attribute that is composed
    of a sequence of AS path segments. Each AS path segment is
    represented by a triple <path segment type, path segment
    length, path segment value>.
        The path segment type is a 1-octet length field with the
    following values defined:
    Value     Segment Type
        1       AS_SET: unordered set of ASes a route in the
                UPDATE message has traversed
        2       AS_SEQUENCE: ordered set of ASes a route in
                the UPDATE message has traversed
        3       AS_CONFED_SEQUENCE: ordered set of Member Autonomous
                Systems in the local confederation that the UPDATE message
                has traversed
        4       AS_CONFED_SET: unordered set of Member Autonomous Systems
                in the local confederation that the UPDATE message has
                traversed
        The path segment length is a 1-octet length field,
    containing the number of ASes (not the number of octets) in
    the path segment value field.
        The path segment value field contains one or more AS
    numbers, each encoded as a 2-octet length field.
    """
    AS_SET = 0x01
    AS_SEQUENCE = 0x02
    AS_CONFED_SEQUENCE = 0x03
    AS_CONFED_SET = 0x04

    ID = AttributeID.AS_PATH
    FLAG = AttributeFlag.TRANSITIVE
    MULTIPLE = False

    @classmethod
    def parse(cls, value, asn4=False):
        """
        Parse AS PATH attributes.
        :param asn4: 4 bytes asn or not
        :param value: raw binary value
        """
        aspath = []
        offset = 0
        total_len = len(value)

        # Determine ASN format: 4 bytes ('I') or 2 bytes ('H')
        asn_byte_len = 4 if asn4 else 2
        asn_fmt_char = 'I' if asn4 else 'H'

        valid_types = {
            cls.AS_SET,
            cls.AS_SEQUENCE,
            cls.AS_CONFED_SEQUENCE,
            cls.AS_CONFED_SET
        }

        while offset < total_len:
            if offset + 2 > total_len:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data='')

            seg_type, num_ases = struct.unpack_from('!BB', value, offset)

            if seg_type not in valid_types:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_MALFORMED_ASPATH,
                    data=repr(value[offset:]))

            offset += 2

            segment_byte_len = num_ases * asn_byte_len

            if offset + segment_byte_len > total_len:
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_ATTR_LEN,
                    data='')

            fmt = f'!{num_ases}{asn_fmt_char}'
            segment = list(struct.unpack_from(fmt, value, offset))

            aspath.append((seg_type, segment))
            offset += segment_byte_len

        return aspath

    @classmethod
    def construct(cls, value, asn4=False):
        """
        Construct AS PATH.
        :param asn4: 4byte asn
        :param value:
        """
        # value example
        # [(2, [3257, 31027, 34848, 21465])], or [(3, [64606]), (2, [64624, 65515])]

        as_path_raw = b''
        for segment in value:
            as_seg_raw = b''
            seg_type = segment[0]
            as_path_list = segment[1]
            if seg_type not in [cls.AS_SET, cls.AS_SEQUENCE, cls.AS_CONFED_SET, cls.AS_CONFED_SEQUENCE]:
                assert excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_MALFORMED_ASPATH,
                    data='')

            if asn4:
                #  4 bytes asn encode
                as_count = 0
                for asn in as_path_list:
                    as_count += 1
                    as_seg_raw += struct.pack('!I', asn)
            else:
                # 2 bytes asn encode
                as_count = 0
                for asn in as_path_list:
                    as_count += 1
                    as_seg_raw += struct.pack('!H', asn)

            as_path_raw += struct.pack('!B', seg_type) + struct.pack('!B', as_count) + as_seg_raw

        flags = cls.FLAG
        if len(as_path_raw) > 255:
            flags += AttributeFlag.EXTENDED_LENGTH
            return struct.pack('!B', flags) + struct.pack('!B', cls.ID) \
                + struct.pack('!H', len(as_path_raw)) + as_path_raw
        else:
            return struct.pack('!B', flags) + struct.pack('!B', cls.ID) \
                + struct.pack('!B', len(as_path_raw)) + as_path_raw
