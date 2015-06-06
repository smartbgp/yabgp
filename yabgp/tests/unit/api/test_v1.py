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

"""Test v1 api"""

import unittest
from yabgp.api.app import app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # prepare some peers
        self.app = app.test_client()

    def tearDown(self):
        """"""
        pass

    def test_v1_root(self):
        result = self.app.get('/v1')
        self.assertTrue(result)

    def test_v1_peers(self):
        self.assertTrue(self.app.get('/v1/peers'))

    def test_v1_peer(self):
        self.assertTrue(self.app.get('/v1/peer'))

if __name__ == '__main__':
    unittest.main()
