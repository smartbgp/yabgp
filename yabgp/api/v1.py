#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

"""Blueprint for version 1 of API
"""
import binascii
import logging
import time
import re

from flask_httpauth import HTTPBasicAuth
from flask import Blueprint, request
import flask
from oslo_config import cfg

from yabgp.api import utils as api_utils
from yabgp.common import constants as bgp_cons

LOG = logging.getLogger(__name__)
blueprint = Blueprint('v1', __name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == cfg.CONF.rest.username:
        return cfg.CONF.rest.password
    return None


@blueprint.route('/')
@api_utils.log_request
def root():
    """
    v1 api root. Get the api status.
    """
    intro = {
        "status": "stable",
        "updated": "2015-01-22T00:00:00Z",
        "version": "v1"}
    cfg.CONF.keep_alive.last_time = time.time()
    return flask.jsonify(intro)


@blueprint.route('/peer/<peer_ip>/state')
@auth.login_required
@api_utils.log_request
def peer(peer_ip):
    """
    Get one peer's running information, include basic configurations and fsm state.
    """
    return flask.jsonify(api_utils.get_peer_conf_and_state(peer_ip))


@blueprint.route('/peer/<peer_ip>/version/<action>')
@auth.login_required
@api_utils.log_request
def get_peer_version(peer_ip, action):
    """
    Get one peer's message statistic, include sending and receiving.
    """
    return flask.jsonify(api_utils.get_peer_version(action, peer_ip))


@blueprint.route('/peer/<peer_ip>/statistic')
@auth.login_required
@api_utils.log_request
def get_peer_statistic(peer_ip):
    """
    Get one peer's message statistic, include sending and receiving.
    """
    return flask.jsonify(api_utils.get_peer_msg_statistic(peer_ip))


@blueprint.route('/peer/<peer_ip>/send/route-refresh', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def send_route_refresh(peer_ip):
    """
    Try to send BGP Route Refresh message to a peer
    """
    LOG.debug('Try to send route refresh to peer %s', peer_ip)
    json_request = flask.request.get_json()
    if 'afi' in json_request and 'safi' in json_request:
        if 'res' not in json_request:
            res = 0
        else:
            res = json_request['res']
        result = api_utils.send_route_refresh(
            peer_ip=peer_ip, afi=json_request['afi'], safi=json_request['safi'], res=res)
        return flask.jsonify(result)
    return flask.jsonify({
        'status': False,
        'code': 'please check your post data'
    })


@blueprint.route('/peer/<peer_ip>/send/update', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def send_update_message(peer_ip):
    """
    Try to send BGP update message to the peer.
    Both update nlri and withdraw nlri treated as Update.
    """
    LOG.debug('Try to send update message to peer %s', peer_ip)
    json_request = flask.request.get_json()
    attr = json_request.get('attr') or {}
    nlri = json_request.get('nlri') or []
    withdraw = json_request.get('withdraw') or []
    if attr:
        attr = {int(k): v for k, v in attr.items()}
        res = api_utils.get_peer_conf_and_state(peer_ip)
        if 5 not in attr and res['peer']['remote_as'] == res['peer']['local_as']:
            # default local preference
            attr[5] = 100
        if 16 in attr:
            # extended community recombine
            ext_community = []
            for ext_com in attr[16]:
                key, value = ext_com.split(':', 1)
                if key.strip().lower() == 'route-target':
                    values = value.strip().split(',')
                    for vau in values:
                        if '.' in vau.strip().split(':')[0]:
                            ext_community.append([258, vau.strip()])
                        else:
                            nums = vau.strip().split(':', 1)
                            if int(nums[0].strip()) <= 65535:
                                ext_community.append([2, vau.strip()])
                            else:
                                if res['peer']['capability']['remote']:
                                    four_bytes_as = res['peer']['capability']['remote']['four_bytes_as']
                                else:
                                    return flask.jsonify({
                                        'status': False,
                                        'code': 'please check peer state'
                                    })
                                if int(nums[0].strip()) > 65535 and four_bytes_as:
                                    ext_community.append([514, vau.strip()])
                                elif not four_bytes_as and int(nums[0].strip()) > 65535:
                                    return flask.jsonify({
                                        'status': False,
                                        'code': 'peer not support as num of greater than 65535'
                                    })
                elif key.strip().lower() == 'dmzlink-bw':
                    values = value.strip().split(',')
                    for vau in values:
                        ext_community.append([16388, vau.strip()])
                elif key.strip().lower() == 'route-origin':
                    values = value.strip().split(',')
                    for vau in values:
                        if '.' in vau.strip().split(':')[0]:
                            ext_community.append([259, vau.strip()])
                        else:
                            if res['peer']['capability']['remote']:
                                four_bytes_as = res['peer']['capability']['remote']['four_bytes_as']
                            else:
                                return flask.jsonify({
                                    'status': False,
                                    'code': 'please check peer state'
                                })
                            nums = vau.strip().split(':', 1)
                            if int(nums[0].strip()) > 65535 and four_bytes_as:
                                ext_community.append([515, vau.strip()])
                            elif not four_bytes_as and int(nums[0].strip()) > 65535:
                                return flask.jsonify({
                                    'status': False,
                                    'code': 'peer not support as num of greater than 65535'
                                })
                            else:
                                ext_community.append([3, vau.strip()])
                elif key.strip().lower() == 'redirect-nexthop':
                    values = value.strip().split(':', 1)
                    ext_community.append([2048, values[0], int(values[1])])
                elif key.strip().lower() == 'redirect-vrf':
                    ext_community.append([32776, value.strip()])
                elif key.strip().lower() == 'traffic-action':
                    values = value.strip().lower().split(',')
                    vau_dict = {}
                    for vau in values:
                        flg, v = vau.strip().split(':', 1)
                        if flg == 's':
                            vau_dict.update({'s': int(v)})
                        elif flg == 't':
                            vau_dict.update({'t': int(v)})
                    ext_community.append([32775, vau_dict])
                elif bgp_cons.BGP_EXT_COM_DICT_1.get(key.strip().lower()):
                    key_num = bgp_cons.BGP_EXT_COM_DICT_1.get(key.strip().lower())
                    values = value.strip().split(':', 1)
                    ext_community.append([key_num, int(values[0]), int(values[1])])
                else:
                    key_num = bgp_cons.BGP_EXT_COM_DICT.get(key.strip().lower())
                    if key_num:
                        values = value.strip().split(',')
                        for vau in values:
                            if key_num == 32777:
                                ext_community.append([key_num, int(vau.strip())])
                            else:
                                ext_community.append([key_num, vau.strip()])
                    else:
                        return flask.jsonify({
                            'status': False,
                            'code': 'unexpected extended community "%s", please check your post data' % key
                        })
            attr[16] = ext_community
    if cfg.CONF.bgp.rib:
        result = api_utils.save_send_ipv4_policies(
            msg={
                'attr': attr,
                'nlri': nlri,
                'withdraw': withdraw
            }
        )
        if not result.get('status'):
            return flask.jsonify(result)
    if (attr and nlri) or withdraw:
        api_utils.update_send_version(peer_ip, attr, nlri, withdraw)
        return flask.jsonify(api_utils.send_update(peer_ip, attr, nlri, withdraw))
    elif 14 in attr or 15 in attr:
        api_utils.update_send_version(peer_ip, attr, nlri, withdraw)
        return flask.jsonify(api_utils.send_update(peer_ip, attr, nlri, withdraw))

    else:
        return flask.jsonify({
            'status': False,
            'code': 'please check your post data'
        })


@blueprint.route('/peer/<peer_ip>/manual-start')
@auth.login_required
@api_utils.log_request
def manual_start(peer_ip):
    """
    Try to manual start BGP session
    """
    LOG.debug('Try to manual start BGP session %s', peer_ip)
    return flask.jsonify(api_utils.manual_start(peer_ip))


@blueprint.route('/peer/<peer_ip>/manual-stop')
@auth.login_required
@api_utils.log_request
def manual_stop(peer_ip):
    """
    Try to manual stop BGP session
    """
    LOG.debug('Try to manual stop BGP session %s', peer_ip)
    return flask.jsonify(api_utils.manual_stop(peer_ip))


@blueprint.route('/peer/<peer_ip>/adj-rib-in', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def search_adj_rib_in(peer_ip):
    json_request = flask.request.get_json()
    prefix_list = json_request.get('data')
    afi_safi = dict(request.args.items()).get('afi_safi') or 'ipv4'
    return flask.jsonify(api_utils.get_adj_rib_in(prefix_list, afi_safi))


@blueprint.route('/peer/<peer_ip>/adj-rib-out', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def search_adj_rib_out(peer_ip):
    json_request = flask.request.get_json()
    prefix_list = json_request.get('data')
    afi_safi = dict(request.args.items()).get('afi_safi') or 'ipv4'
    return flask.jsonify(api_utils.get_adj_rib_out(prefix_list, afi_safi))


@blueprint.route('/peer/<peer_ip>/json_to_bin', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def json_to_bin(peer_ip):
    json_request = flask.request.get_json()
    attr = json_request.get('attr') or {}
    nlri = json_request.get('nlri') or []
    withdraw = json_request.get('withdraw') or []
    format = flask.request.args.get('format') or None
    if attr:
        attr = {int(k): v for k, v in attr.items()}
        res = api_utils.get_peer_conf_and_state(peer_ip)
        if 5 not in attr and res['peer']['remote_as'] == res['peer']['local_as']:
            # default local preference
            attr[5] = 100
        if 16 in attr:
            # extended community recombine
            ext_community = []
            for ext_com in attr[16]:
                key, value = ext_com.split(':', 1)
                if key.strip().lower() == 'route-target':
                    values = value.strip().split(',')
                    for vau in values:
                        if '.' in vau.strip().split(':')[0]:
                            ext_community.append([258, vau.strip()])
                        else:
                            nums = vau.strip().split(':', 1)
                            # check(2:2)whether the last 2(AN) < 65535
                            if int(nums[0].strip()) <= 65535:
                                ext_community.append([2, vau.strip()])
                            else:
                                # 4 byte, need to check whether four_bytes_as is true in capability
                                if res['peer']['capability']['remote']:
                                    four_bytes_as = res['peer']['capability']['remote']['four_bytes_as']
                                else:
                                    return flask.jsonify({
                                        'status': False,
                                        'code': 'please check peer state'
                                    })
                                if int(nums[0].strip()) > 65535 and four_bytes_as:
                                    ext_community.append([514, vau.strip()])
                                elif not four_bytes_as and int(nums[0].strip()) > 65535:
                                    return flask.jsonify({
                                        'status': False,
                                        'code': 'peer not support as num of greater than 65535'
                                    })
                elif key.strip().lower() == 'dmzlink-bw':
                    values = value.strip().split(',')
                    for vau in values:
                        ext_community.append([16388, vau.strip()])
                elif key.strip().lower() == 'route-origin':
                    values = value.strip().split(',')
                    for vau in values:
                        if '.' in vau.strip().split(':')[0]:
                            ext_community.append([259, vau.strip()])
                        else:
                            if res['peer']['capability']['remote']:
                                four_bytes_as = res['peer']['capability']['remote']['four_bytes_as']
                            else:
                                return flask.jsonify({
                                    'status': False,
                                    'code': 'please check peer state'
                                })
                            nums = vau.strip().split(':', 1)
                            if int(nums[0].strip()) > 65535 and four_bytes_as:
                                ext_community.append([515, vau.strip()])
                            elif not four_bytes_as and int(nums[0].strip()) > 65535:
                                return flask.jsonify({
                                    'status': False,
                                    'code': 'peer not support as num of greater than 65535'
                                })
                            else:
                                ext_community.append([3, vau.strip()])
                elif key.strip().lower() == 'redirect-vrf':
                    ext_community.append([32776, value.strip()])
                elif key.strip().lower() == 'redirect-nexthop':
                    values = value.strip().split(':', 1)
                    ext_community.append([2048, values[0], int(values[1])])
                elif key.strip().lower() == 'traffic-action':
                    values = value.strip().lower().split(',')
                    vau_dict = {}
                    for vau in values:
                        flg, v = vau.strip().split(':', 1)
                        if flg == 's':
                            vau_dict.update({'s': int(v)})
                        elif flg == 't':
                            vau_dict.update({'t': int(v)})
                    ext_community.append([32775, vau_dict])
                elif bgp_cons.BGP_EXT_COM_DICT_1.get(key.strip().lower()):
                    key_num = bgp_cons.BGP_EXT_COM_DICT_1.get(key.strip().lower())
                    values = value.strip().split(':', 1)
                    ext_community.append([key_num, int(values[0]), int(values[1])])
                else:
                    key_num = bgp_cons.BGP_EXT_COM_DICT.get(key.strip().lower())
                    if key_num:
                        values = value.strip().split(',')
                        for vau in values:
                            if key_num == 32777:
                                ext_community.append([key_num, int(vau.strip())])
                            else:
                                ext_community.append([key_num, vau.strip()])
                    else:
                        return flask.jsonify({
                            'status': False,
                            'code': 'unexpected extended community "%s", please check your post data' % key
                        })
            attr[16] = ext_community
    if (attr and nlri) or withdraw:
        massage_bin = api_utils.construct_update_to_bin(peer_ip, attr, nlri, withdraw)
        massage = binascii.b2a_hex(massage_bin).decode('utf-8')
        if format == 'human':
            massage_tmp = ' '.join(re.findall('.{2}', massage))
            massage = re.findall('.{24}', massage_tmp)
            massage.append(massage_tmp[(len(massage) * 24):])
        return flask.jsonify({'bin': massage})
    elif 14 in attr or 15 in attr:
        massage_bin = api_utils.construct_update_to_bin(peer_ip, attr, nlri, withdraw)
        LOG.info('massage_bin:' + binascii.b2a_hex(massage_bin).decode('utf-8'))
        massage = binascii.b2a_hex(massage_bin).decode('utf-8')
        LOG.info('massage:' + massage)
        if format == 'human':
            massage_tmp = ' '.join(re.findall('.{2}', massage))
            massage = re.findall('.{24}', massage_tmp)
            massage.append(massage_tmp[(len(massage) * 24):])
        return flask.jsonify({'bin': massage})
    else:
        return flask.jsonify({
            'status': False,
            'code': 'please check your post data'
        })


@blueprint.route('/peer/<peer_ip>/send/bin_update', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def send_bin_update(peer_ip):
    format = flask.request.args.get('format') or None
    json_request = flask.request.get_json()
    bin = json_request.get('binary_data') or None
    try:
        if bin:
            if format == 'human':
                bin = ''.join(bin).replace(' ', '')
            elif not isinstance(bin, str):
                raise TypeError('arg type should be string')
            massage = binascii.a2b_hex(bin)
            return flask.jsonify(api_utils.send_bin_update(peer_ip, massage))
        else:
            return flask.jsonify({
                'status': False,
                'code': 'please input some string'
            })
    except binascii.Error as e:
        LOG.error(e)
        return flask.jsonify({
            'status': False,
            'code': 'please input even length string'
        })
    except Exception as e:
        LOG.error(e)
        return flask.jsonify({
            'status': False,
            'code': 'please check your post data'
        })
