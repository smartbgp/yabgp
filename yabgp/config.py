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

""" basic config """

import logging
import sys

from oslo_config import cfg

CONF = cfg.CONF


BGP_CONFIG_OPTS = [
    cfg.IntOpt('peer_start_interval',
               default=10,
               help='The interval to start each BGP peer'),
    cfg.BoolOpt('four_bytes_as',
                default=True,
                help='If support 4bytes AS'),
    cfg.BoolOpt('route_refresh',
                default=True,
                help='If support sending and receiving route refresh message'),
    cfg.BoolOpt('cisco_route_refresh',
                default=True,
                help='If support sending and receiving cisco route refresh message'),
    cfg.BoolOpt('enhanced_route_refresh',
                default=True,
                help='If support enhanced route refresh'),
    cfg.StrOpt('add_path',
               choices=['ipv4_send', 'ipv4_receive', 'ipv4_both'],
               help='BGP additional path feature and supported address family'),
    cfg.BoolOpt('graceful_restart',
                default=True,
                help='if support graceful restart'),
    cfg.BoolOpt('cisco_multi_session',
                default=True,
                help='if support cisco multi session'),
    cfg.DictOpt('running_config',
                default={},
                help='The running configuration for BGP')
]

CONF.register_opts(BGP_CONFIG_OPTS, group='bgp')

BGP_PEER_CONFIG_OPTS = [
    cfg.IntOpt('remote_as',
               help='The remote BGP peer AS number'),
    cfg.IntOpt('local_as',
               help='The Local BGP AS number'),
    cfg.IPOpt('remote_addr',
              help='The remote address of the peer'),
    cfg.IPOpt('local_addr',
              default='0.0.0.0',
              help='The local address of the BGP'),
    cfg.StrOpt('md5',
               help='The MD5 string use to auth',
               secret=True),
    cfg.ListOpt('afi_safi',
                default=['ipv4'],
                help='The Global config for address family and sub address family')
]

CONF.register_cli_opts(BGP_PEER_CONFIG_OPTS, group='bgp')

LOG = logging.getLogger(__name__)


def get_bgp_config():
    """
    Get BGP running config
    :return:
    """
    # check bgp configuration from CLI input
    LOG.info('Try to load BGP configuration from CLI input')
    if CONF.bgp.local_as and CONF.bgp.remote_as and CONF.bgp.local_addr and CONF.bgp.remote_addr:
        CONF.bgp.running_config = {
            'remote_as': CONF.bgp.remote_as,
            'remote_addr': CONF.bgp.remote_addr,
            'local_as': CONF.bgp.local_as,
            'local_addr': CONF.bgp.local_addr,
            'md5': CONF.bgp.md5,
            'afi_safi': CONF.bgp.afi_safi,
            'capability': {
                'local': {
                    'four_bytes_as': CONF.bgp.four_bytes_as,
                    'route_refresh': CONF.bgp.route_refresh,
                    'cisco_route_refresh': CONF.bgp.cisco_route_refresh,
                    'enhanced_route_refresh': CONF.bgp.enhanced_route_refresh,
                    'graceful_restart': CONF.bgp.graceful_restart,
                    'cisco_multi_session': CONF.bgp.cisco_multi_session,
                    'add_path': CONF.bgp.add_path},
                'remote': {}
            }
        }
    else:
        LOG.error('Please provide enough parameters!')
        sys.exit()
