# Copyright 2023 Cisco Systems, Inc.
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

""" Test SRv6 Locator TLV """

import unittest

from yabgp.message.attribute.linkstate.prefix.srv6_locator import SRv6Locator


class TestSRv6Locator(unittest.TestCase):

    def test_unpack(self):
        data_bin = b'\x00' \
                   b'\x00' \
                   b'\x00\x04' \
                   b'\x00\x00\x00\x00'

        data_dict = {
            'type': 'srv6_locator',
            'value': {
                'flags': {
                    'D-flag': 0
                },
                'algorithm': 0,
                'metric': 0,
                'sub_tlvs': []
            }
        }
        self.assertEqual(data_dict, SRv6Locator.unpack(data=data_bin, bgpls_pro_id=1).dict())
