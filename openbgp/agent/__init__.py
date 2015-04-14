# Copyright (C) 2015 Cisco Systems, Inc.
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
import logging

from openbgp import version
from openbgp.common.config import get_bgp_config
from openbgp.common import log
log.early_init_log(logging.DEBUG)

from oslo.config import cfg

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


def prepare_service(args=None):
    try:
        CONF(args=args, project='openbgp', version=version,
             default_config_files=['/etc/openbgp/openbgp.ini'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, project='openbgp', version=version)

    log.init_log()
    LOG.info('Log (Re)opened.')
    LOG.info("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.INFO)
    try:
        get_bgp_config()
    except Exception as e:
        LOG.error(e, exc_info=True)
        sys.exit()