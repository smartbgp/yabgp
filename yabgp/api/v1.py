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
from yabgp.channel import filter as channel_filter

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

    **Example request**:

    .. sourcecode:: http

      GET /v1 HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "status": "stable",
        "updated": "2015-01-22T00:00:00Z",
        "version": "v1"
      }

    :status 200: the api can work.
    """
    intro = {
        "status": "stable",
        "updated": "2015-01-22T00:00:00Z",
        "version": "v1"}
    return flask.jsonify(intro)


@blueprint.route('/peers', methods=['GET'])
@auth.login_required
@api_utils.log_request
def peers():
    """
    Get all peers realtime running information, include basic configurations and fsm state.

    **Example request**

    .. sourcecode:: http

      GET /v1/peers HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json

      {
          "peers": [
              {
                  "fsm": "ESTABLISHED",
                  "local_addr": "100.100.0.1",
                  "local_as": 65022,
                  "remote_addr": "100.100.9.1",
                  "remote_as": 65022,
                  "uptime": 106810.47324299812
              },
              {
                  "fsm": "ESTABLISHED",
                  "local_addr": "100.100.0.1",
                  "local_as": 65022,
                  "remote_addr": "100.100.9.1",
                  "remote_as": 65022,
                  "uptime": 106810.47324299812
              }
          ]
      }

    :status 200: the api can work.
    """
    return flask.jsonify(api_utils.get_peer_conf_and_state())


@blueprint.route('/peer/<peer_ip>/state')
@auth.login_required
@api_utils.log_request
def peer(peer_ip):
    """
    Get one peer's running information, include basic configurations and fsm state.

    **Example request**

    .. sourcecode:: http

      GET /v1/peer/10.124.1.245/state HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "peer": {
            "fsm": "ESTABLISHED",
            "local_addr": "10.75.44.11",
            "local_as": 23650,
            "remote_addr": "10.124.1.245",
            "remote_as": 23650,
            "uptime": 7.913731813430786
            }
        }

    :param peer_ip: peer ip address
    :status 200: the api can work.

    """
    return flask.jsonify(api_utils.get_peer_conf_and_state(peer_ip))


@blueprint.route('/peer/<peer_ip>/statistic')
@auth.login_required
@api_utils.log_request
def get_peer_statistic(peer_ip):
    """
    Get one peer's message statistic, include sending and receiving.

    **Example request**

    .. sourcecode:: http

      GET /v1/peer/10.124.1.245/statistic HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
          "receive": {
              "Keepalives": 3,
              "Notifications": 0,
              "Opens": 1,
              "Route Refresh": 0,
              "Updates": 5
          },
          "send": {
              "Keepalives": 3,
              "Notifications": 0,
              "Opens": 1,
              "Route Refresh": 0,
              "Updates": 0
          }
      }

    :param peer_ip: peer ip address
    :status 200: the api can work.

    """
    return flask.jsonify(api_utils.get_peer_msg_statistic(peer_ip))


@blueprint.route('/peer/<peer_ip>/send/route-refresh', methods=['POST'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def send_route_refresh(peer_ip):
    """
    Try to send BGP Route Refresh message to a peer

    **Example request**

    .. sourcecode:: http

      POST /v1/peer/10.124.1.245/send/route-refresh HTTP/1.1
      Host: example.com
      Accept: application/json
      POST Data:
      {
        "afi": 1,
        "safi": 1,
        "res": 0
      }
      `res` is optional, the default value is 0.

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "status": True
      }

    Success f the status is `True` in the reponse, otherwise, the status is `False`. If the status is
    Flase, there will be a code tell you why. like:

    .. sourcecode:: http

        {
            "status": False,
            "code": "please check your post data"
        }

    :param peer_ip: peer ip address
    :status 200: the api can work.
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
    Try to send BGP update message to the peer. Both update nlri and withdraw nlri treated as Update.

    **Example request**

    .. sourcecode:: http

      POST /v1/peer/10.124.1.245/send/update HTTP/1.1
      Host: example.com
      Accept: application/json

    Post data example for IPv4 update and withdraw

    .. sourcecode:: http

        # update
        {
            "attr":{
                "1": 0,
                "2": [],
                "3": "192.0.2.1",
                "5": 100,
                "8": ["NO_EXPORT"]
        },
            "nlri": ["172.20.1.0/24", "172.20.2.0/24"]
        }
        # withdraw
        {
            "withdraw": ["172.20.1.0/24", "172.20.2.0/24"]
        }


    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "status": True
      }

    Success f the status is `True` in the reponse, otherwise, the status is `False`. If the status is
    Flase, there will be a code tell you why. like:

    .. sourcecode:: http

        {
            "status": False,
            "code": "please check your post data"
        }

    :param peer_ip: peer ip address
    :status 200: the api can work.

    """
    LOG.debug('Try to send update message to peer %s', peer_ip)
    json_request = flask.request.get_json()
    attr = json_request.get('attr')
    nlri = json_request.get('nlri')
    withdraw = json_request.get('withdraw')
    if attr:
        attr = {int(k): v for k, v in attr.items()}
    if (attr and nlri) or withdraw:
        return flask.jsonify(api_utils.send_update(peer_ip, attr, nlri, withdraw))
    else:
        return flask.jsonify({
            'status': False,
            'code': 'please check your post data'
        })


@blueprint.route('/channel/filter', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
@api_utils.log_request
def manage_channel_filter():
    """
    manage channel filter which is used in channel for sending bgp update messages

    **Example request**

    .. sourcecode:: http

      POST /v1/channel/filter HTTP/1.1
      Host: example.com
      Accept: application/json

    post data example

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
          "filter": [
            {
                'type': 'prefix',
                'value': '1.1.1.1/32'
            },
            {
                'type': 'as_path',
                'value': 4837
            },
            {
                'type': 'community',
                'value': '4837:1239'
            }
          ]
      }

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "status": True
      }

    Success f the status is `True` in the reponse, otherwise, the status is `False`. If the status is
    Flase, there will be a code tell you why. like:

    :status 200: the api can work.

    """
    if cfg.CONF.standalone:
        return flask.jsonify({
            'status': False,
            'code': 'The standalone mode does not support channel filter function'
        })
    if flask.request.method in ['POST', 'DELETE']:
        filter_dict = flask.request.get_json()
        if flask.request.method == 'POST':
            for item in filter_dict['filter']:
                cfg.CONF.rabbit_mq.filter[item['type']][item['value']] = None
        elif flask.request.method == 'DELETE':
            for item in filter_dict['filter']:
                if item['value'] in cfg.CONF.rabbit_mq.filter[item['type']]:
                    cfg.CONF.rabbit_mq.filter[item['type']].pop(item['value'])
        return flask.jsonify({
            'status': True,
            'code': None
        })
    elif flask.request.method == 'GET':
        filter_list = []
        for filter_type in channel_filter.FILTER_TYPE_LIST:
            for item in cfg.CONF.rabbit_mq.filter[filter_type].keys():
                filter_list.append({
                    'type': filter_type,
                    'value': item
                })
        return flask.jsonify({
            'filter': filter_list
        })


@blueprint.route('/adj-rib-in/<afi_safi>/<peer_ip>', methods=['GET'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def get_adj_rib_in(afi_safi, peer_ip):
    """
    Try to get BGP adj rib in

    **Example request**

    .. sourcecode:: http

      GET /v1/adj-rib-in/ipv4/10.75.44.242  HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "prefixes": [
          "1.1.1.1/32",
          "2.2.2.2/32",
          "3.3.3.3/32"
        ]
      }

    **Example request**

    .. sourcecode:: http

      GET /v1/adj-rib-in/ipv4/10.75.44.242?prefix=1.1.1.1/32  HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
          "attr": {
            "1": 0,
            "2": [],
            "3": "10.124.1.221",
            "4": 0,
            "5": 100
          }
      }

    :param afi_safi: address and sub address family, now only suport ipv4
    :param peer_ip: peer ip address
    :status 200: the api can work, otherwise the peer is not established maybe.
    """
    prefix = flask.request.args.get('prefix')
    community = flask.request.args.get('community')
    if prefix or community:
        if prefix:
            return flask.jsonify({
                'attr': api_utils.get_adj_rib_in(peer_ip, afi_safi, prefix)
            })
    else:
        return flask.jsonify({
            'prefixes': api_utils.get_adj_rib_in(peer_ip, afi_safi)}
        )


@blueprint.route('/adj-rib-out/<afi_safi>/<peer_ip>', methods=['GET'])
@auth.login_required
@api_utils.log_request
@api_utils.makesure_peer_establish
def get_adj_rib_out(afi_safi, peer_ip):
    """
    Try to get BGP adj rib out

    **Example request**

    .. sourcecode:: http

      GET /v1/adj-rib-out/ipv4/10.75.44.242  HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "prefixes": [
          "4.4.4.4/32",
          "5.5.5.5/32",
          "6.6.6.6/32"
        ]
      }

    **Example request**

    .. sourcecode:: http

      GET /v1/adj-rib-out/ipv4/10.75.44.242?prefix=4.4.4.4/32  HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
          "attr": {
            "1": 0,
            "2": [],
            "3": "10.75.44.225",
            "5": 100,
            "8": [
              "NO_EXPORT"
            ]
          }
      }

    :param afi_safi: address and sub address family, now only suport ipv4
    :param peer_ip: peer ip address
    :status 200: the api can work, otherwise the peer is not established maybe.
    """
    prefix = flask.request.args.get('prefix')
    community = flask.request.args.get('community')
    if prefix or community:
        if prefix:
            return flask.jsonify({
                'attr': api_utils.get_adj_rib_out(peer_ip, afi_safi, prefix)
            })
    return flask.jsonify({
        'prefixes': api_utils.get_adj_rib_out(peer_ip, afi_safi)}
    )
