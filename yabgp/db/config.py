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

""" database config """

from oslo_config import cfg

CONF = cfg.CONF

database_base_options = [
    cfg.StrOpt('connection',
               default='mongodb://127.0.0.1:27017',
               help='Database connection'),
    cfg.StrOpt('dbname',
               default='yabgp',
               help='database name'),
    cfg.BoolOpt('use_replica',
                default=False,
                help='if use replica set')
]

database_replica_options = [

    cfg.StrOpt('replica_name',
               default='rs1',
               help='the replica set name'),
    cfg.IntOpt('read_preference',
               default=3,
               help='the read preference mode for this instance'),
    cfg.IntOpt('write_concern',
               default=-1,
               help='write concern'),
    cfg.IntOpt('write_concern_timeout',
               default=5000,
               help='write concern timeout')
]


def register_options():
    CONF.register_opts(database_base_options, group='database')
    if CONF.database.use_replica:
        CONF.register_opts(database_replica_options, group='database')
