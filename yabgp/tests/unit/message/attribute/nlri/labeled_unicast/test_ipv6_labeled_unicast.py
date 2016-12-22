# Copyright 2015-2016 Cisco Systems, Inc.
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

from yabgp.message.attribute.nlri.labeled_unicast.ipv6 import IPv6LabeledUnicast


class TestIPv6LabeledUnicast(unittest.TestCase):

    def test_construct(self):
        nlri_list = [
            {'label': [91], 'prefix': '2001:2121::1/128'},
            {'label': [92], 'prefix': '::2001:2121:1:0/64'},
            {'label': [93], 'prefix': '2001:4837:1821::2/127'}]
        nlri_hex = b'\x98\x00\x05\xb1\x20\x01\x21\x21\x00\x00\x00\x00\x00\x00\x00' \
            '\x00\x00\x00\x00\x01\x58\x00\x05\xc1\x20\x01\x21\x21\x00\x01' \
            '\x00\x00\x97\x00\x05\xd1\x20\x01\x48\x37\x18\x21\x00\x00\x00' \
            '\x00\x00\x00\x00\x00\x00\x02'

        self.assertEqual(nlri_hex, IPv6LabeledUnicast.construct(nlri_list))

    def test_parse(self):
        nlri_list = [
            {'label': [91], 'prefix': '2001:2121::1/128'},
            {'label': [92], 'prefix': '::2001:2121:1:0/64'},
            {'label': [93], 'prefix': '2001:4837:1821::2/127'}]
        nlri_hex = b'\x98\x00\x05\xb1\x20\x01\x21\x21\x00\x00\x00\x00\x00\x00\x00' \
            '\x00\x00\x00\x00\x01\x58\x00\x05\xc1\x20\x01\x21\x21\x00\x01' \
            '\x00\x00\x97\x00\x05\xd1\x20\x01\x48\x37\x18\x21\x00\x00\x00' \
            '\x00\x00\x00\x00\x00\x00\x02'

        self.assertEqual(nlri_list, IPv6LabeledUnicast.parse(nlri_hex))


if __name__ == '__main__':
    unittest.main()
