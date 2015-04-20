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

from oslo.config import cfg

CONF = cfg.CONF

msg_process_opts = [
    cfg.BoolOpt('write_disk',
                default=True,
                help='Whether the BGP message is written to disk'),
    cfg.StrOpt('write_dir',
               default='/home/bgpmon/data/bgp/',
               help='The BGP messages storage path'),
    cfg.IntOpt('write_msg_max_size',
               default=500,
               help='The Max size of one BGP message file, the unit is MB'),
]

CONF.register_opts(msg_process_opts, group='message')

bgp_config_opts = [
    cfg.IntOpt('peer_start_interval',
               default=10,
               help='The interval to start each BGP peer'),
    cfg.ListOpt('afi_safi',
                default=['ipv4'],
                help='The Global config for address family and sub address family'),
    cfg.DictOpt('running_config',
                default={},
                help='The running configuration for BGP'),
    cfg.StrOpt('config_file',
               help='BGP peers configuration file')

]
CONF.register_opts(bgp_config_opts, group='bgp')

bgp_peer_conf_cli_opts = [
    cfg.IntOpt('remote_as',
               help='The remote BGP peer AS number'),
    cfg.IntOpt('local_as',
               help='The Local BGP AS number'),
    cfg.StrOpt('remote_addr',
               help='The remote address of the peer'),
    cfg.StrOpt('local_addr',
               help='The local address of the BGP'),
    cfg.StrOpt('md5',
               help='The MD5 string use to auth')
]

CONF.register_cli_opts(bgp_peer_conf_cli_opts, group='bgp')

LOG = logging.getLogger(__name__)


def get_bgp_config():
    """
    Get BGP running config
    :return:
    """
    # check bgp_conf_file
    if CONF.bgp.config_file:
        LOG.info('Try to load BGP configuration from %s' % CONF.bgp.config_file)
        LOG.error('Failed to load BGP configuration')
        # TODO parse xml config file to get multi bgp config
        # will be supported in future
        sys.exit()
    else:
        # check bgp configuration from CLI input
        LOG.info('Try to load BGP configuration from CLI input')
        if CONF.bgp.local_as and CONF.bgp.remote_as and CONF.bgp.local_addr and CONF.bgp.remote_addr:
            CONF.bgp.running_config[CONF.bgp.remote_addr] = {
                'remote_as': CONF.bgp.remote_as,
                'remote_addr': CONF.bgp.remote_addr,
                'local_as': CONF.bgp.local_as,
                'local_addr': CONF.bgp.local_addr,
                'rib': CONF.bgp.rib,
                'md5': CONF.bgp.md5,
                'afi_safi': CONF.bgp.afi_safi
            }
            LOG.info('Get BGP running configuration for peer %s' % CONF.bgp.remote_addr)
            for item in CONF.bgp.running_config[CONF.bgp.remote_addr]:
                LOG.info("%s = %s" % (item, CONF.bgp.running_config[CONF.bgp.remote_addr][item]))
            return
        else:
            LOG.error('Please provide enough parameters!')
            sys.exit()