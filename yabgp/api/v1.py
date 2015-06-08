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

from flask import Blueprint
import flask

from yabgp.api import utils as api_utils

LOG = logging.getLogger(__name__)
blueprint = Blueprint('v1', __name__)


@blueprint.route('/')
def root():
    """
    v1 api root. Get the api status.

    **Example request**:

    .. sourcecode:: http

      GET /v1 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

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


@blueprint.route('/peers',  methods=['GET'])
def peers():
    """
    Get all peers realtime running information.

    **Example request**

    .. sourcecode:: http

      GET /v1/peers HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

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


@blueprint.route('/peer/<peer_ip>')
def peer(peer_ip):
    """
    Get one peer's running information.

    :param peer_ip: peer ip address

    """
    pass
