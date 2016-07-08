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
import logging
from functools import wraps

from oslo_config import cfg
from flask import request
import flask

from yabgp.common import constants as common_cons

LOG = logging.getLogger(__name__)


def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        LOG.info('API request url %s', request.url)
        if request.query_string:
            LOG.info('API query string %s', request.query_string)
        LOG.info('API request method %s', request.method)
        if request.method == 'POST':
            LOG.info('API POST data %s', request.json)
        LOG.debug('API request environ %s', request.environ)
        return f(*args, **kwargs)
    return decorated_function


def makesure_peer_establish(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        value = kwargs['peer_ip']
        if _ready_to_send_msg(peer_ip=value):
            return f(*args, **kwargs)
        else:
            return flask.jsonify({
                'status': False,
                'code': "Please check the peer's state"
            })
    return decorator


def get_peer_conf_and_state(peer_ip=None):
    """
    get peer configuration and state
    :param peer_ip: peer ip address
    :return:
    """

    def get_peer_state(peer):
        one_peer_state = {key: cfg.CONF.bgp.running_config[peer][key] for key in [
            'remote_as', 'remote_addr', 'local_as', 'local_addr', 'capability']}
        fsm = cfg.CONF.bgp.running_config[peer]['factory'].fsm.state
        one_peer_state['fsm'] = common_cons.stateDescr[fsm]
        if fsm == common_cons.ST_ESTABLISHED:
            one_peer_state['uptime'] = time.time() - cfg.CONF.bgp.running_config[peer]['factory'].fsm.uptime
        else:
            one_peer_state['uptime'] = 0
        return one_peer_state

    if peer_ip:
        peer_state = {}
        if peer_ip in cfg.CONF.bgp.running_config:
            peer_state = get_peer_state(peer_ip)
        return {'peer': peer_state}
    # for multi peers
    result = {'peers': []}
    for peer_ip in cfg.CONF.bgp.running_config:
        result['peers'].append(get_peer_state(peer_ip))
    return result


def get_peer_msg_statistic(peer_ip=None):
    """
    get peer send and receive message statistic
    :param peer_ip: peer ip address
    :return:
    """

    if peer_ip and peer_ip in cfg.CONF.bgp.running_config:
        return {
            'send': cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.msg_sent_stat,
            'receive': cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.msg_recv_stat,
        }
    else:
        return {}


def _ready_to_send_msg(peer_ip):
    """
    check if the peer is ready to send message
    :param peer_ip:  peer ip address
    :return: if is ready, return is True, or False
    """
    if peer_ip and peer_ip in cfg.CONF.bgp.running_config:
        # check if the peer is established
        peer_state = get_peer_conf_and_state(peer_ip)
        if peer_state.get('peer').get('fsm') == common_cons.stateDescr[common_cons.ST_ESTABLISHED]:
            return True
    return False


def send_route_refresh(peer_ip, afi, safi, res):
    """
    send route refresh messages
    :param peer_ip: peer ip address
    :return: the sending results
    """
    try:
        if cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.send_route_refresh(
                afi=afi, safi=safi, res=res):
            return {
                'status': True
            }
    except Exception as e:
        LOG.error(e)
        return {
            'status': False,
            'code': 'failed when send this message out'
        }


def send_update(peer_ip, attr, nlri, withdraw):
    """
    send update message
    :param peer_ip: peer ip address
    :return:
    """
    # TODO check RIB out policy
    # TODO update RIB out table
    if cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.send_update({
            'attr': attr, 'nlri': nlri, 'withdraw': withdraw}):
        # TODO update ad rib out table
        # if nlri or withdraw:
        #     for prefix in nlri:
        #         if isinstance(prefix, basestring):
        #             cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.get_rib_out()['ipv4'][prefix] = attr

        return {
            'status': True
        }
    else:
        return {
            'status': False,
            'code': 'failed when send this message out'
        }


def get_adj_rib_in(peer_ip, afi_safi, prefix=None):
    rib_table = cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.get_rib_in().get(afi_safi) or {}
    if prefix:
        attr = rib_table.get(prefix)
        if not attr:
            flask.abort(404)
        else:
            return attr
    return rib_table.keys()


def get_adj_rib_out(peer_ip, afi_safi, prefix=None):
    rib_table = cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.get_rib_out().get(afi_safi) or {}
    if prefix:
        attr = rib_table.get(prefix)
        if not attr:
            flask.abort(404)
        else:
            return attr
    return rib_table.keys()


def close_bgp_connection(peer_ip):
    cfg.CONF.bgp.running_config[peer_ip]['factory'].manual_stop()


def start_bgp_connection(peer_ip, idle_hold=False):
    cfg.CONF.bgp.running_config[peer_ip]['factory'].manual_start(idle_hold=idle_hold)


def restart_bgp_connection(peer_ip):
    close_bgp_connection(peer_ip)
    start_bgp_connection(peer_ip)


def get_adj_rib_all(peer_ip, afi_safi):
    rib_table = cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.get_rib_in().get(afi_safi) or {}

    return rib_table
