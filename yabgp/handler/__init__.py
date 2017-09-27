#!/usr/bin/python
# -*- coding: utf-8 -*-
import abc
import logging
from queue import Queue


LOG = logging.getLogger(__name__)


class BaseHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        internal message queue:
        push message in custom handler
        pop message when keep alive received
        """
        self.inter_mq = Queue()
        pass

    @abc.abstractmethod
    def init(self):
        raise NotImplemented

    @abc.abstractmethod
    def on_update_error(self, peer, timestamp, msg):
        raise NotImplemented

    @abc.abstractmethod
    def update_received(self, peer, timestamp, msg):
        raise NotImplemented

    @abc.abstractmethod
    def keepalive_received(self, peer, timestamp):
        raise NotImplemented

    @abc.abstractmethod
    def open_received(self, peer, timestamp, result):
        raise NotImplemented

    @abc.abstractmethod
    def route_refresh_received(self, peer, msg, msg_type):
        raise NotImplemented

    @abc.abstractmethod
    def notification_received(self, peer, msg):
        raise NotImplemented

    @abc.abstractmethod
    def on_connection_lost(self, peer):
        raise NotImplemented

    @abc.abstractmethod
    def on_connection_failed(self, peer, msg):
        raise NotImplemented
