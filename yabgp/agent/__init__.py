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
from twisted.web.server import Site

from yabgp import version, log
from yabgp.core.factory import BGPPeering
from yabgp.config import get_bgp_config
from yabgp.common import constants as bgp_cons
from yabgp.api.app import app
from yabgp.channel.config import rabbit_mq
from yabgp.channel.factory import PikaFactory
from yabgp.db.config import database_options
from yabgp.db.mongodb import MongoApi


log.early_init_log(logging.DEBUG)

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


def check_running_mode():

    if not CONF.standalone:
        # not standalone?
        CONF.register_opts(rabbit_mq, group='rabbit_mq')
        CONF.register_opts(database_options, group='database')


def check_msg_config():

    LOG.info('Check configurations about message process')
    if CONF.message.write_disk:
        if not os.path.exists(CONF.message.write_dir):
            os.makedirs(CONF.message.write_dir)
            LOG.info('Create dir %s', CONF.message.write_dir)
        CONF.message.write_msg_max_size = CONF.message.write_msg_max_size * 1024 * 1024


def prepare_twisted_service():
    LOG.info('Prepare twisted services')
    # check all peers
    all_peers = {}

    # check running mode
    if not CONF.standalone:
        # rabbitmq factory
        rabbit_mq_factory = PikaFactory(
            host=CONF.rabbit_mq.rabbit_host,
            port=CONF.rabbit_mq.rabbit_port,
            userid=CONF.rabbit_mq.rabbit_userid,
            password=CONF.rabbit_mq.rabbit_password
        )
        rabbit_mq_factory.connect()
        # mongodb connection
        mongo_connection = MongoApi(
            connection_url=CONF.database.connection,
            db_name=CONF.database.dbname,
            use_replica=CONF.database.use_replica,
            replica_name=CONF.database.replica_name,
            read_preference=CONF.database.read_preference,
            write_concern=CONF.database.write_concern,
            w_timeout=CONF.database.write_concern_timeout
        )
    else:
        rabbit_mq_factory = None
        mongo_connection = None
    for peer in CONF.bgp.running_config:
        LOG.info('Get peer %s configuration', peer)
        if CONF.message.write_disk:
            msg_file_path_for_peer = os.path.join(
                CONF.message.write_dir,
                peer.lower()
            )
            if not os.path.exists(msg_file_path_for_peer):
                os.makedirs(msg_file_path_for_peer)
                LOG.info('Create dir %s for peer %s', msg_file_path_for_peer, peer)
            LOG.info('BGP message file path is %s', msg_file_path_for_peer)
        else:
            msg_file_path_for_peer = None
        LOG.info('Create BGPPeering instance')
        afi_safi_list = [bgp_cons.AFI_SAFI_STR_DICT[afi_safi]
                         for afi_safi in CONF.bgp.running_config[peer]['afi_safi']]
        CONF.bgp.running_config[peer]['afi_safi'] = afi_safi_list
        CONF.bgp.running_config[peer]['capability']['local']['afi_safi'] = afi_safi_list
        bgp_peering = BGPPeering(
            myasn=CONF.bgp.running_config[peer]['local_as'],
            myaddr=CONF.bgp.running_config[peer]['local_addr'],
            peerasn=CONF.bgp.running_config[peer]['remote_as'],
            peeraddr=CONF.bgp.running_config[peer]['remote_addr'],
            afisafi=CONF.bgp.running_config[peer]['afi_safi'],
            msgpath=msg_file_path_for_peer,
            md5=CONF.bgp.running_config[peer]['md5'],
            channel=rabbit_mq_factory,
            mongo_conn=mongo_connection
        )
        all_peers[peer] = bgp_peering
        CONF.bgp.running_config[peer]['factory'] = bgp_peering

    # Starting api server
    if sys.version_info[0] == 2:
        from twisted.web.wsgi import WSGIResource
        LOG.info("Prepare RESTAPI service")
        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = Site(resource)
        try:
            reactor.listenTCP(CONF.rest.bind_port, site, interface=CONF.rest.bind_host)
            LOG.info("serving RESTAPI on http://%s:%s", CONF.rest.bind_host, CONF.rest.bind_port)
        except Exception as e:
            LOG.error(e, exc_info=True)
            sys.exit()

    for peer in all_peers:
        LOG.info('start peer, peer address=%s', peer)
        all_peers[peer].automatic_start()
    reactor.run()


def prepare_service(args=None):
    try:
        CONF(args=args, project='yabgp', version=version,
             default_config_files=['/etc/yabgp/yabgp.ini'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, project='yabgp', version=version)

    check_running_mode()
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
