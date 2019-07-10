# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
dalian-stc-dev@cisco.com
Copyright 2019 Cisco Systems, Inc.
All rights reserved.
"""
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

""" IPv4 Unicast """

import struct
import binascii
import logging
import netaddr

from yabgp.message.attribute.nlri import NLRI
from yabgp.common import exception as excep
from yabgp.common import constants as bgp_cons


LOG = logging.getLogger()


class IPv4Unicast(NLRI):

    @staticmethod
    def parse(nlri_data, addpath=False):
        """
        Parses an RFC4271 encoded blob of BGP prefixes into a list

        :param data: hex data
        :param addpath: support addpath or not
        :return: prefix_list
        """
        prefixes = []
        postfix = nlri_data
        while len(postfix) > 0:
            # for python2 and python3
            if addpath:
                path_id = struct.unpack('!I', postfix[0:4])[0]
                postfix = postfix[4:]
            if isinstance(postfix[0], int):
                prefix_len = postfix[0]
            else:
                prefix_len = ord(postfix[0])
            if prefix_len > 32:
                LOG.warning('Prefix Length larger than 32')
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_NETWORK_FIELD,
                    data=repr(nlri_data)
                )
            octet_len, remainder = int(prefix_len / 8), prefix_len % 8
            if remainder > 0:
                # prefix length doesn't fall on octet boundary
                octet_len += 1
            tmp = postfix[1:octet_len + 1]
            # for python2 and python3
            if isinstance(postfix[0], int):
                prefix_data = [i for i in tmp]
            else:
                prefix_data = [ord(i) for i in tmp]
            # Zero the remaining bits in the last octet if it didn't fall
            # on an octet boundary
            if remainder > 0:
                prefix_data[-1] &= 255 << (8 - remainder)
            prefix_data = prefix_data + list(str(0)) * 4
            prefix = "%s.%s.%s.%s" % (tuple(prefix_data[0:4])) + '/' + str(prefix_len)
            if not addpath:
                prefixes.append(prefix)
            else:
                prefixes.append({'prefix': prefix, 'path_id': path_id})
            # Next prefix
            postfix = postfix[octet_len + 1:]

        return prefixes

    @classmethod
    def construct(cls, nlri_list):
        """
        Construct NLRI from list to hex data
        :param nlri_list:
        :return:
        """
        nlri_hex = b''
        for prefix in nlri_list:
            prefix = netaddr.IPNetwork(prefix)
            nlri_hex += struct.pack('!B', prefix.prefixlen)
            nlri_hex += binascii.unhexlify(hex(prefix.ip)[2:])
        return nlri_hex
