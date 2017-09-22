#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

""" Channel"""


class Channel(object):
    """channel basic class
    """
    EXCHANGE_MGMT_CONTAINER = 'mgmt_container'
    EXCHANGE_MGMT_TYPE = 'direct'

    EXCHANGE_BGP_ROUTE_POLICY = 'bgp_route_policy'
    EXCHANGE_BGP_MSG_SENDER = 'bgp-msg-sender'