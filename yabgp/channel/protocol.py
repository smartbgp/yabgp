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
    connected = False
    name = 'AMQP:Protocol'

    @inlineCallbacks
    def connected(self, connection):
        self.channel = yield connection.channel()
        yield self.channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.connected = True
        for (exchange, routing_key, callback,) in self.factory.read_list:
            yield self.setup_read(exchange, routing_key, callback)

        self.send()

    @inlineCallbacks
    def read(self, exchange, routing_key, callback):
        """Add an exchange to the list of exchanges to read from."""
        if self.connected:
            yield self.setup_read(exchange, routing_key, callback)

    @inlineCallbacks
    def setup_read(self, exchange, routing_key, callback):
        """This function does the work to read from an exchange."""
        if not exchange == '':
            yield self.channel.exchange_declare(exchange=exchange, type='topic', durable=True, auto_delete=False)
        if not exchange == '':
            queue = yield self.channel.queue_declare(durable=False, exclusive=True, auto_delete=True)
            queue_name = queue.method.queue
            yield self.channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)
        else:
            queue = yield self.channel.queue_declare(queue=routing_key, durable=False, exclusive=True, auto_delete=True)
            queue_name = queue.fields[0]
        (queue, consumer_tag,) = yield self.channel.basic_consume(queue=queue_name, no_ack=True)
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)

    def _read_item(self, item, queue, callback):
        """Callback function which is called when an item is read."""
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)
        (channel, deliver, props, msg,) = item
        LOG.debug('%s (%s): %s', deliver.exchange, deliver.routing_key, repr(msg))
        callback(item)

    def _read_item_err(self, error):
        LOG.error(error)

    def send(self):
        """If connected, send all waiting messages."""
        if self.connected:
            while len(self.factory.queued_messages) > 0:
                (exchange, r_key, message,) = self.factory.queued_messages.pop(0)
                self.send_message(exchange, r_key, message)

    @inlineCallbacks
    def send_message(self, exchange, routing_key, msg):
        """Send a single message."""
        LOG.debug('%s (%s): %s', exchange, routing_key, repr(msg))
        yield self.channel.exchange_declare(exchange=exchange, type='topic', durable=True, auto_delete=False)
        prop = spec.BasicProperties(delivery_mode=2)
        try:
            yield self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=prop)
        except Exception as error:
            LOG.error('Error while sending message: %s', error)
