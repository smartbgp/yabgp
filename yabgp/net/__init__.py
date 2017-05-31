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

import socket


class IPAddress(object):

    @staticmethod
    def unpack(data):
        return socket.inet_ntop(socket.AF_INET if len(data) == 4 else socket.AF_INET6, data)

    @staticmethod
    def pack(data):
        return socket.inet_pton(socket.AF_INET if len(data.split('.')) == 4 else socket.AF_INET6, data)


class IPNetwork(object):
    pass
