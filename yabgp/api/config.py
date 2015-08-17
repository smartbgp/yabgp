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

from oslo_config import cfg


CONF = cfg.CONF

rest_server_ops = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='Address to bind the API server to'),
    cfg.IntOpt('bind_port',
               default=8801,
               help='Port the bind the API server to'),
    cfg.StrOpt('username',
               default='admin',
               help='Username for api server'),
    cfg.StrOpt('password',
               default='admin',
               help='Password for api server',
               secret=True)
]
