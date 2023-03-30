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

""" Test SRv6 Endpoint Behavior TLV """

import unittest

from yabgp.message.attribute.linkstate.srv6_sid.srv6_endpoint_behavior import SRv6EndpointBehavior


class TestSRv6EndpointBehavior(unittest.TestCase):

    def test_unpack(self):
        data_bin = b'\x00\x30' \
                   b'\x00' \
                   b'\x00'

        data_dict = {
            'type': 'srv6_endpoint_behavior',
            'value': {
                'endpoint_behavior': 48,
                'flags': 0,
                'algorithm': 0
            }
        }
        self.assertEqual(data_dict, SRv6EndpointBehavior.unpack(data=data_bin).dict())
