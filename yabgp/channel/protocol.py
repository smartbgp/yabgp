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

""" twisted message queue protocol
reference from https://github.com/pika/pika/blob/master/examples/twisted_service.py
"""

import logging

from pika import spec
from pika.adapters import twisted_connection
from twisted.internet.defer import inlineCallbacks

PREFETCH_COUNT = 2
LOG = logging.getLogger(__name__)


class PikaProtocol(twisted_connection.TwistedProtocolConnection):
    is_connected = False
    name = 'AMQP:Protocol'
    factory = None

    @inlineCallbacks
    def connected(self, connection):

        self.channel = yield connection.channel()
        yield self.channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.is_connected = True
        for routing_key in self.factory.peer_list:
            LOG.info('routing key %s', routing_key)
            yield self.setup('', routing_key)

        # try to send all waiting messages
        LOG.info('connected, try to send all waiting message')
        self.send()

    @inlineCallbacks
    def setup(self, exchange, routing_key):
        """This function does the work to read from an exchange."""
        LOG.info("setup rabbitmq exchange or queue")
        if not exchange == '':
            yield self.channel.exchange_declare(exchange=exchange, type='topic', durable=True, auto_delete=False)
        else:
            yield self.channel.queue_declare(queue=routing_key, durable=True, auto_delete=False)

    def send(self):
        """If connected, send all waiting messages."""
        if self.is_connected:
            while len(self.factory.queued_messages) > 0:
                (exchange, r_key, message,) = self.factory.queued_messages.pop(0)
                self.send_message(exchange, r_key, message)

    @inlineCallbacks
    def send_message(self, exchange, routing_key, msg):
        """Send a single message."""
        LOG.debug('%s (%s): %s', exchange, routing_key, repr(msg))
        # yield self.channel.exchange_declare(exchange=exchange, type='topic', durable=True, auto_delete=False)
        prop = spec.BasicProperties(delivery_mode=2)
        try:
            yield self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=prop)
        except Exception as error:
            LOG.error('Error while sending message: %s', error)

    def connectionLost(self, reason):

        """Called when the associated connection was lost.

        :param reason: the reason of lost connection.
        """
        LOG.debug('Called connectionLost')
        self.is_connected = False
        LOG.info("Connection lost:%s", reason.getErrorMessage())
