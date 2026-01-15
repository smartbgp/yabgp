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

""" Test Application-Specific Link Attributes TLV """

import unittest

from yabgp.message.attribute.linkstate.link.app_spec_link_attr import AppSpecLinkAttr


class TestAppSpecLinkAttr(unittest.TestCase):
    """Test AppSpecLinkAttr TLV (Type 1122)"""

    def test_unpack_with_te_metric(self):
        """Test unpack ASLA TLV with TE Metric sub-TLV

        Data: 04 04 00 00 10 00 00 00 00 00 00 00 04 44 00 04 ff ff ff ff
            Header (4 bytes):
                - SABM Length: 0x04 = 4
                - UDABM Length: 0x04 = 4
                - Reserved: 0x0000
            SABM (4 bytes): 0x10000000
            UDABM (4 bytes): 0x00000000
            Sub-TLV (8 bytes):
                - Type: 0x0444 = 1092 (TE Default Metric)
                - Length: 0x0004 = 4
                - Value: 0xffffffff = 4294967295
        """
        data_bin = bytes.fromhex('04040000100000000000000004440004ffffffff')

        expected = {
            'type': 'ASLA',
            'value': {
                'sabm': {'len': 4, 'value': '0x10000000'},
                'udabm': {'len': 4, 'value': '0x00000000'},
                'sub_tlvs': [
                    {
                        'type': 'te_metric',
                        'value': 4294967295
                    }
                ]
            }
        }

        self.assertEqual(expected, AppSpecLinkAttr.unpack(data_bin).dict())


if __name__ == "__main__":
    unittest.main()
