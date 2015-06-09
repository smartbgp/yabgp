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

import time

from oslo.config import cfg

from yabgp.common import constants as common_cons


def get_peer_conf_and_state(peer_ip=None):
    if peer_ip:
        pass
        return
    result = {
        'peers': []
    }
    for peer in cfg.CONF.bgp.running_config:
        peer_state = {
            'remote_as': cfg.CONF.bgp.running_config[peer]['remote_as'],
            'local_addr': cfg.CONF.bgp.running_config[peer]['local_addr'],
            'local_as': cfg.CONF.bgp.running_config[peer]['local_as'],
            'remote_addr': cfg.CONF.bgp.running_config[peer]['remote_addr']
        }
        fsm = cfg.CONF.bgp.running_config[peer]['factory'].fsm.state
        peer_state['fsm'] = common_cons.stateDescr[fsm]
        if fsm == common_cons.ST_ESTABLISHED:
            peer_state['uptime'] = time.time() - cfg.CONF.bgp.running_config[peer]['factory'].fsm.uptime
        else:
            peer_state['uptime'] = 0
        result['peers'].append(peer_state)
    return result
