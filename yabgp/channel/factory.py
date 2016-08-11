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

"""Twisted message queue factory
reference from https://github.com/pika/pika/blob/master/examples/twisted_service.py
"""

import logging

import pika
from twisted.internet import protocol
from twisted.internet import reactor

from yabgp.channel.protocol import PikaProtocol

LOG = logging.getLogger(__name__)


class PikaFactory(protocol.ReconnectingClientFactory):

    def __init__(self, url):
        self.parameters = pika.URLParameters(url)
        self.client = None
        self.queued_messages = []
        self.peer_list = []

    def startedConnecting(self, connector):
        LOG.info('Started to connect to AMQP')

    def buildProtocol(self, addr):
        self.resetDelay()
        LOG.info('Connected AMQP')
        self.client = PikaProtocol(self.parameters)
        self.client.factory = self
        self.client.ready.addCallback(self.client.connected)
        return self.client

    def clientConnectionLost(self, connector, reason):
        LOG.info('Lost connection.  Reason: %s', reason.getErrorMessage())
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason.getErrorMessage())

    def clientConnectionFailed(self, connector, reason):
        LOG.info('Connection failed. Reason: %s', reason.getErrorMessage())
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason.getErrorMessage())

    def send_message(self, exchange=None, routing_key=None, message=None):
        self.queued_messages.append((exchange, routing_key, message))
        if self.client is not None:
            self.client.send()

    def connect(self):

        try:
            reactor.connectTCP(
                host=self.parameters.host,
                port=self.parameters.port,
                factory=self)
        except Exception as e:
            LOG.error(e)
