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

""" logging handler. Reference from https://github.com/osrg/ryu/blob/master/ryu/log.py
"""

from __future__ import print_function
import inspect
import logging
import logging.config
import logging.handlers
import os
import sys
if sys.version_info[0] == 2:
    import ConfigParser
elif sys.version_info[0] == 3:
    from configparser import ConfigParser

from oslo_config import cfg


CONF = cfg.CONF

CONF.register_cli_opts([
    cfg.BoolOpt('verbose', default=False, help='show debug output'),
    cfg.BoolOpt('use-stderr', default=True, help='log to standard error'),
    cfg.StrOpt('log-dir', default=None, help='log file directory'),
    cfg.StrOpt('log-file', default=None, help='log file name'),
    cfg.StrOpt('log-file-mode', default='0644',
               help='default log file permission'),
    cfg.StrOpt('log-config-file', default=None,
               help='Path to a logging config file to use')
])

CONF.register_cli_opt(cfg.IntOpt(
    'log-backup-count',
    default=5,
    help='the number of backup log file'
))

DEBUG_LOG_FORMAT = '%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s ' \
                   '%(funcName)s %(lineno)d [-] %(message)s'
INFOR_LOG_FORMAT = '%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(message)s'
_EARLY_LOG_HANDLER = None


def early_init_log(level=None):
    global _EARLY_LOG_HANDLER
    _EARLY_LOG_HANDLER = logging.StreamHandler(sys.stderr)

    log = logging.getLogger()
    log.addHandler(_EARLY_LOG_HANDLER)
    if level is not None:
        log.setLevel(level)


def _get_log_file():
    if CONF.log_file:
        return CONF.log_file
    if CONF.log_dir:
        return os.path.join(CONF.log_dir,
                            os.path.basename(inspect.stack()[-1][1])) + '.log'
    return None


def _set_log_format(handers, _format):
    for hander in handers:
        hander.setFormatter(logging.Formatter(_format))


def init_log():
    global _EARLY_LOG_HANDLER

    log = logging.getLogger()
    if CONF.log_config_file:
        try:
            logging.config.fileConfig(CONF.log_config_file,
                                      disable_existing_loggers=False)
            if CONF.verbose:
                log.setLevel(logging.DEBUG)
                for handler in log.handlers:
                    handler.setFormatter(logging.Formatter(DEBUG_LOG_FORMAT))
        except ConfigParser.Error as e:
            print('Failed to parse %s: %s' % (CONF.log_config_file, e),
                  file=sys.stderr)
            sys.exit(2)
        return

    if CONF.use_stderr:
        log.addHandler(logging.StreamHandler(sys.stderr))
    if _EARLY_LOG_HANDLER is not None:
        log.removeHandler(_EARLY_LOG_HANDLER)
        _EARLY_LOG_HANDLER = None

    log_file = _get_log_file()
    if log_file is not None:
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        log.addHandler(logging.handlers.RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=CONF.log_backup_count))
        mode = int(CONF.log_file_mode, 8)
        os.chmod(log_file, mode)
        for handler in log.handlers:
            handler.setFormatter(logging.Formatter(INFOR_LOG_FORMAT))

    if CONF.verbose:
        log.setLevel(logging.DEBUG)
        for handler in log.handlers:
            handler.setFormatter(logging.Formatter(DEBUG_LOG_FORMAT))
    else:
        log.setLevel(logging.INFO)
        _set_log_format(log.handlers, INFOR_LOG_FORMAT)
