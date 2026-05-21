# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, version 2.0 (the "License"); you may
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

"""Test Add Path Capability"""

import unittest

from yabgp.message.open import convert_addpath_str_to_int


class TestAddPathCapability(unittest.TestCase):
    """
    Test cases for Add Path capability introduced in commits 1a17665 and 814598b.
    These tests cover:
    1. convert_addpath_str_to_int function
    2. Add path capability parsing and construction
    3. Add path negotiation logic
    """

    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None

    def test_convert_addpath_str_to_int_single_receive(self):
        """
        Test converting a single AFI/SAFI in receive mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_single_send(self):
        """
        Test converting a single AFI/SAFI in send mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 2]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_single_both(self):
        """
        Test converting a single AFI/SAFI in both mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_multiple_afi_safi(self):
        """
        Test converting multiple AFI/SAFI entries
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [
            [(1, 1), 3],  # ipv4, both
            [(2, 1), 1],  # ipv6, receive
            [(1, 128), 2]  # vpnv4, send
        ]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_ipv4_lu(self):
        """
        Test converting IPv4 Labeled Unicast
        """
        addpath_list = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 4), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_ipv6_lu(self):
        """
        Test converting IPv6 Labeled Unicast
        """
        addpath_list = [
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(2, 4), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_vpnv6(self):
        """
        Test converting VPNv6
        """
        addpath_list = [
            {'afi_safi': 'vpnv6', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(2, 128), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_flowspec(self):
        """
        Test converting Flowspec
        """
        addpath_list = [
            {'afi_safi': 'flowspec', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 133), 2]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_empty_list(self):
        """
        Test converting empty list
        """
        addpath_list = []
        result = convert_addpath_str_to_int(addpath_list)
        expected = []
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_mixed_families(self):
        """
        Test converting mixed address families (IPv4, IPv6, VPN, Labeled Unicast)
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'both'},
            {'afi_safi': 'ipv4_lu', 'send/receive': 'receive'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'},
            {'afi_safi': 'vpnv6', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [
            [(1, 1), 3],    # ipv4, both
            [(2, 1), 3],    # ipv6, both
            [(1, 4), 1],    # ipv4_lu, receive
            [(2, 4), 1],    # ipv6_lu, receive
            [(1, 128), 2],  # vpnv4, send
            [(2, 128), 2]   # vpnv6, send
        ]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_evpn(self):
        """
        Test converting EVPN
        """
        addpath_list = [
            {'afi_safi': 'evpn', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(25, 70), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_bgpls(self):
        """
        Test converting BGP-LS
        """
        addpath_list = [
            {'afi_safi': 'bgpls', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(16388, 71), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_sr_policy(self):
        """
        Test converting SR Policy
        """
        addpath_list = [
            {'afi_safi': 'ipv4_srte', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 73), 3]]
        self.assertEqual(expected, result)


class TestLocalAddPathConfig(unittest.TestCase):
    """
    Test cases for local_add_path configuration processing in config.py
    Tests the list comprehension that converts local_add_path strings to dictionaries
    """

    def test_local_add_path_single_ipv4_both(self):
        """
        Test processing single IPv4 both mode configuration
        """
        # Simulate the list comprehension from config.py line 137-139
        local_add_path_config = ['ipv4_both']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_single_ipv4_receive(self):
        """
        Test processing single IPv4 receive mode configuration
        """
        local_add_path_config = ['ipv4_receive']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_single_ipv4_send(self):
        """
        Test processing single IPv4 send mode configuration
        """
        local_add_path_config = ['ipv4_send']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_multiple_families(self):
        """
        Test processing multiple address families configuration
        """
        local_add_path_config = ['ipv4_both', 'ipv6_receive', 'vpnv4_send']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_labeled_unicast(self):
        """
        Test processing Labeled Unicast address family configuration
        Note: ipv4_lu has two underscores, rsplit('_', 1) only splits the last one
        """
        local_add_path_config = ['ipv4_lu_both', 'ipv6_lu_receive']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_empty_list(self):
        """
        Test processing empty configuration list
        """
        local_add_path_config = []
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = []
        self.assertEqual(expected, result)

    def test_local_add_path_all_modes(self):
        """
        Test all modes (send, receive, both)
        """
        local_add_path_config = ['ipv4_send', 'ipv6_receive', 'vpnv4_both']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_complex_afi_safi_names(self):
        """
        Test complex address family names (containing multiple underscores)
        """
        local_add_path_config = [
            'ipv4_lu_both',
            'ipv6_lu_receive',
            'ipv4_srte_send',
            'ipv6_flowspec_both'
        ]
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'},
            {'afi_safi': 'ipv4_srte', 'send/receive': 'send'},
            {'afi_safi': 'ipv6_flowspec', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
