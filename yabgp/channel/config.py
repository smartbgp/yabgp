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

""" message queue config """

from oslo_config import cfg

from yabgp.channel.filter import FILTER_TYPR_INIT_DICT

CONF = cfg.CONF

rabbit_mq = [
    cfg.StrOpt('rabbit_host',
               default='localhost',
               help='The RabbitMQ broker address where a single node is used'),
    cfg.IntOpt('rabbit_port',
               default=5672,
               help='The RabbitMQ broker port where a single node is used'),
    cfg.BoolOpt('rabbit_use_ssl',
                default=False,
                help='Connect over SSL for RabbitMQ.'),
    cfg.StrOpt('rabbit_userid',
               default='guest',
               help='The RabbitMQ userid.'),
    cfg.StrOpt('rabbit_password',
               default='guest',
               help='The RabbitMQ password.',
               secret=True),
]

channle_filter = [
    cfg.DictOpt('filter',
                default=FILTER_TYPR_INIT_DICT,
                help='the community and prefix filter dict'),
]
