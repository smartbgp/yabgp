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

"""RabbitMQ Message Publisher
"""

import logging
import traceback
import json

import pika

from yabgp.channel import Channel


LOG = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False


class Publisher(Channel):
    """Publisher class
    """

    def __init__(self, url):

        self.parameters = pika.URLParameters(url)
        self._connection = None
        self._channel = None

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.

        :rtype: pika.BlockingConnection

        """
        LOG.debug('Connecting to rabbitmq server')
        try:
            # Open a connection to RabbitMQ on localhost using all default parameters
            self._connection = pika.BlockingConnection(self.parameters)

            # Open the channel
            self._channel = self._connection.channel()
            return True
        except Exception as e:
            LOG.error(e)
            LOG.debug(traceback.format_exc())
            return False

    def close(self):
        """Close connnection and channel
        """
        if self._channel:
            self._channel.close()
        if self._connection:
            self._connection.close()

    def declare_exchange(self, _exchange, _type):
        """Declare exchange
        """
        if not self.connect():
            return False
        self._channel.exchange_declare(exchange=_exchange, type=_type)
        return True

    def bind_queue(self, _exchange, _queue):
        """bind a queue to exchange
        """
        self._channel.queue_bind(exchange=_exchange, queue=_queue)

    def declare_queue(self, name):
        """Declare Queue
        """
        if not self.connect():
            return False
        self._channel.queue_declare(queue=name, durable=True)

    def publish_message(self, _exchange, _routing_key, _body):
        """
        try to publish message to exchange
        :param _exchange: exchange name
        :param _routing_key: routing key
        :param _body: message body
        :return: True or False
        """
        if not self.connect():
            return False

        try:
            # try to declare exchange
            if _exchange:
                self._channel.exchange_declare(exchange=_exchange, type='direct')
            properties = pika.BasicProperties(
                content_type='application/json',
                delivery_mode=1
            )
            # Turn on delivery confirmations
            self._channel.confirm_delivery()
            # Send a route policy
            if self._channel.basic_publish(
                    exchange=_exchange,
                    routing_key=_routing_key,
                    body=json.dumps(_body),
                    properties=properties):
                LOG.debug('Message publish was confirmed')
                return True
            else:
                LOG.error('Message publish could not be confirmed')
                return False
        except Exception as e:
            LOG.error(e)
            LOG.debug(traceback.format_exc())
            return False
