# Copyright 2015 Cisco Systems, Inc.
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

""" Test Notification message"""

import unittest


from yabgp.message.notification import Notification


class TestNotification(unittest.TestCase):

    def test_parse(self):
        msg_hex = b'\x03\x05\x00\x00'
        noti_msg = Notification().parse(msg_hex)
        self.assertEqual((3, 5, b'\x00\x00'), noti_msg)

    def test_construct(self):

        msg_hex = Notification().construct(error=3, suberror=5, data=b'\x00\x00')
        hope_msg = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\x00\x17\x03\x03\x05\x00\x00'
        self.assertEqual(hope_msg, msg_hex)

if __name__ == '__main__':
    unittest.main()
