#!/usr/bin/python
# -*- coding: utf-8 -*-
import abc

from yabgp.common import constants as bgp_cons
from yabgp.db import constants as channel_cons
import time
from oslo_config import cfg

CONF = cfg.CONF


class BaseHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

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


class DefaultHandler(BaseHandler):
    def __init__(self):
        super(DefaultHandler, self).__init__()

    def on_update_error(self, peer, timestamp, msg):
        peer.factory.write_msg(
            timestamp=timestamp,
            msg_type=6,
            msg={'msg': msg},
            flush=True
        )

    def update_received(self, peer, timestamp, msg):
        # write message to disk
        peer.factory.write_msg(
            timestamp=timestamp,
            msg_type=bgp_cons.MSG_UPDATE,
            msg={"msg": msg}
        )
        peer.factory.flush_and_check_file_size()

    def keepalive_received(self, peer, timestamp):
        """
        keepalive message default handler
        :param peer:
        :param timestamp:
        :return:
        """

        if peer.msg_recv_stat['Keepalives'] == 1:
            # agent online
            if not CONF.standalone and peer.factory.tag in \
                    [channel_cons.TARGET_ROUTER_TAG, channel_cons.SOURCE_AND_TARGET_ROUTER_TAG]:
                send_to_channel_msg = {
                    'agent_id': '%s:%s' % (CONF.rest.bind_host, CONF.rest.bind_port),
                    'type': bgp_cons.MSG_KEEPALIVE,
                    'msg': None
                }
                peer.factory.channel.send_message(
                    exchange='', routing_key=peer.factory.peer_addr, message=send_to_channel_msg)

        if CONF.message.write_keepalive:
            # write bgp message
            peer.factory.write_msg(
                timestamp=timestamp,
                msg_type=4,
                msg={"msg": None},
                flush=True
            )

    def open_received(self, peer, timestamp, result):
        # write bgp message
        peer.factory.write_msg(
            timestamp=timestamp,
            msg_type=1,
            msg={"msg": result},
            flush=True
        )

    def route_refresh_received(self, peer, msg, msg_type):
        peer.factory.write_msg(
            timestamp=time.time(),
            msg_type=msg_type,
            msg={"msg": msg},
            flush=True
        )

    def notification_received(self, peer, msg):
        peer.factory.write_msg(
            timestamp=time.time(),
            msg_type=3,
            msg={"msg": msg},
            flush=True
        )
