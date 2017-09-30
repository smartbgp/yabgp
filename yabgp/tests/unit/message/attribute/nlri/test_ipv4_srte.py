# Copyright 2015-2017 Cisco Systems, Inc.
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

import unittest

from yabgp.message.attribute.nlri.ipv4_srte import IPv4SRTE


class TestIPv4SRTE(unittest.TestCase):

    def test_construct(self):
        nlri_bin = b'\x60\x00\x00\x00\x00\x00\x00\x00\x0a\xc0\xa8\x05\x07'
        nlri = {"distinguisher": 0, "color": 10, "endpoint": "192.168.5.7"}
        self.assertEqual(nlri_bin, IPv4SRTE.construct(nlri))

if __name__ == '__main__':
    unittest.main()
