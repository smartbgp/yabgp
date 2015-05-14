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

import sys
import os
import logging

from oslo.config import cfg
from twisted.internet import reactor

from softbgp import version
from softbgp.core.factory import BGPPeering
from softbgp.common.config import get_bgp_config
from softbgp.common import constants as bgp_cons
from softbgp.common import log
log.early_init_log(logging.DEBUG)

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


def check_msg_config():

    LOG.info('Check configurations about message process')
    if CONF.message.write_disk:
        if not os.path.exists(CONF.message.write_dir):
            os.makedirs(CONF.message.write_dir)
            LOG.info('Create dir %s' % CONF.message.write_dir)
        CONF.message.write_msg_max_size = CONF.message.write_msg_max_size * 1024 * 1024


def prepare_twisted_service():
    LOG.info('Prepare twisted services')
    # check all peers
    all_peers = {}
    for peer in CONF.bgp.running_config:
        LOG.info('Get peer %s configuration' % peer)
        if CONF.message.write_disk:
            msg_file_path_for_peer = os.path.join(
                CONF.message.write_dir,
                peer.lower()
            )
            if not os.path.exists(msg_file_path_for_peer):
                os.makedirs(msg_file_path_for_peer)
                LOG.info('Create dir %s for peer %s' % (msg_file_path_for_peer, peer))
            LOG.info('BGP message file path is %s' % msg_file_path_for_peer)
        else:
            msg_file_path_for_peer = None
        LOG.info('Create BGPPeering instance')
        afi_safi_list = [bgp_cons.AFI_SAFI_STR_DICT[afi_safi]
                         for afi_safi in CONF.bgp.running_config[peer]['afi_safi']]
        CONF.bgp.running_config[peer]['afi_safi'] = afi_safi_list
        bgp_peering = BGPPeering(
            myasn=CONF.bgp.running_config[peer]['local_as'],
            myaddr=CONF.bgp.running_config[peer]['local_addr'],
            peerasn=CONF.bgp.running_config[peer]['remote_as'],
            peeraddr=CONF.bgp.running_config[peer]['remote_addr'],
            afisafi=CONF.bgp.running_config[peer]['afi_safi'],
            msgpath=msg_file_path_for_peer,
            md5=CONF.bgp.running_config[peer]['md5']
        )
        all_peers[peer] = bgp_peering

    for peer in all_peers:
        LOG.info('start peer, peer address=%s' % peer)
        all_peers[peer].automatic_start()
    reactor.run()


def prepare_service(args=None):
    try:
        CONF(args=args, project='softbgp', version=version,
             default_config_files=['/etc/softbgp/softbgp.ini'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, project='softbgp', version=version)

    log.init_log()
    LOG.info('Log (Re)opened.')
    LOG.info("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.INFO)
    try:
        get_bgp_config()
        check_msg_config()
    except Exception as e:
        LOG.error(e, exc_info=True)
        sys.exit()
    prepare_twisted_service()
