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
import traceback

from oslo_config import cfg
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from yabgp import version, log
from yabgp.core.factory import BGPPeering
from yabgp.config import get_bgp_config
from yabgp.common import constants as bgp_cons
from yabgp.api.app import app
from yabgp.handler.default_handler import DefaultHandler


log.early_init_log(logging.DEBUG)

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


def check_msg_config():
    """check message configuration
    """
    LOG.info('Check configurations about message process')
    if CONF.message.write_disk:
        if not os.path.exists(CONF.message.write_dir):
            try:
                os.makedirs(CONF.message.write_dir)
                LOG.info('Create dir %s', CONF.message.write_dir)
            except OSError:
                # sencond try
                if not os.path.exists(CONF.message.write_dir):
                    LOG.error(traceback.format_exc())
                    sys.exit()
        CONF.message.write_msg_max_size = CONF.message.write_msg_max_size * 1024 * 1024


def prepare_twisted_service(handler, reactor_thread_size=100):
    """prepare twsited service
    """
    LOG.info('Prepare twisted services')

    LOG.info('Get peer configuration')
    for conf_key in CONF.bgp.running_config:
        LOG.info('---%s = %s', conf_key, CONF.bgp.running_config[conf_key])

    # init handler
    handler.init()

    LOG.info('Create BGPPeering twsited instance')
    afi_safi_list = [bgp_cons.AFI_SAFI_STR_DICT[afi_safi] for afi_safi in CONF.bgp.running_config['afi_safi']]
    CONF.bgp.running_config['afi_safi'] = afi_safi_list
    CONF.bgp.running_config['capability']['local']['afi_safi'] = afi_safi_list
    bgp_peering = BGPPeering(
        myasn=CONF.bgp.running_config['local_as'],
        myaddr=CONF.bgp.running_config['local_addr'],
        peerasn=CONF.bgp.running_config['remote_as'],
        peeraddr=CONF.bgp.running_config['remote_addr'],
        afisafi=CONF.bgp.running_config['afi_safi'],
        md5=CONF.bgp.running_config['md5'],
        handler=handler
    )
    CONF.bgp.running_config['factory'] = bgp_peering

    # Starting api server
    LOG.info("Prepare RESTAPI service")
    LOG.info("reactor_thread_size = %s", reactor_thread_size)
    reactor.suggestThreadPoolSize(reactor_thread_size)
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)
    try:
        reactor.listenTCP(CONF.rest.bind_port, site, interface=CONF.rest.bind_host)
        LOG.info("serving RESTAPI on http://%s:%s", CONF.rest.bind_host, CONF.rest.bind_port)
    except Exception as e:
        LOG.error(e, exc_info=True)
        sys.exit()

    LOG.info('Starting BGPPeering twsited instance')
    bgp_peering.automatic_start()

    reactor.run()


def register_api_handler(api_handler):
    """register flask blueprint
    """
    app.register_blueprint(api_handler.blueprint, url_prefix=api_handler.url_prefix)


def prepare_service(args=None, handler=None, api_hander=None, reactor_thread_size=100):
    """prepare all services
    """
    try:
        CONF(args=args, project='yabgp', version=version,
             default_config_files=['/etc/yabgp/yabgp.ini'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, project='yabgp', version=version)

    log.init_log()
    LOG.info('Log (Re)opened.')
    LOG.info("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.INFO)
    try:
        if not handler:
            LOG.info('No handler provided, init default handler')
            handler = DefaultHandler()
        get_bgp_config()
        check_msg_config()
    except Exception as e:
        LOG.error(e)
        LOG.debug(traceback.format_exc())
        sys.exit()
    # prepare api handler
    if api_hander:
        register_api_handler(api_hander)
    LOG.info('Starting server in PID %s', os.getpid())
    prepare_twisted_service(handler, reactor_thread_size)
