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
import logging

from flask.ext.httpauth import HTTPBasicAuth
from flask import Blueprint
import flask
from oslo_config import cfg

from yabgp.api import utils as api_utils

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
    return flask.jsonify(intro)


@blueprint.route('/peer/<peer_ip>/state')
@auth.login_required
@api_utils.log_request
def peer(peer_ip):
    """
    Get one peer's running information, include basic configurations and fsm state.
    """
    return flask.jsonify(api_utils.get_peer_conf_and_state(peer_ip))


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
    attr = json_request.get('attr')
    nlri = json_request.get('nlri')
    withdraw = json_request.get('withdraw')
    if attr:
        attr = {int(k): v for k, v in attr.items()}
        if 5 not in attr:
            # default local preference
            attr[5] = 100
    if (attr and nlri) or withdraw:
        return flask.jsonify(api_utils.send_update(peer_ip, attr, nlri, withdraw))
    elif 14 in attr or 15 in attr:
        return flask.jsonify(api_utils.send_update(peer_ip, attr, nlri, withdraw))

    else:
        return flask.jsonify({
            'status': False,
            'code': 'please check your post data'
        })
