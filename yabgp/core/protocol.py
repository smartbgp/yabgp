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

"""BGP Protocol"""

import logging
import traceback
import struct
import time

import netaddr
from oslo_config import cfg
from twisted.internet import protocol
from twisted.internet import reactor
from radix import Radix
import copy

from yabgp.common import constants as bgp_cons
from yabgp.message.open import Open
from yabgp.message.keepalive import KeepAlive
from yabgp.message.update import Update
from yabgp.message.notification import Notification
from yabgp.message.route_refresh import RouteRefresh
from yabgp.common import exception as excep

LOG = logging.getLogger(__name__)

CONF = cfg.CONF


class BGP(protocol.Protocol):
    """Protocol class for BGP 4"""

    def __init__(self):

        """Create a BGP protocol.
        """
        self.fsm = None
        self.peer_id = None

        self.disconnected = False
        self._receive_buffer = b''
        self.fourbytesas = False
        self.add_path_ipv4_receive = False
        self.add_path_ipv4_send = False
        self.adj_rib_in = {k: {} for k in CONF.bgp.afi_safi}
        self.adj_rib_out = {k: {} for k in CONF.bgp.afi_safi}
        self.adj_rib_in_ipv4_tree = Radix()
        self.afi_add_path = None

        # statistic
        self.msg_sent_stat = {
            'Opens': 0,
            'Notifications': 0,
            'Updates': 0,
            'Keepalives': 0,
            'RouteRefresh': 0
        }
        self.msg_recv_stat = {
            'Opens': 0,
            'Notifications': 0,
            'Updates': 0,
            'Keepalives': 0,
            'RouteRefresh': 0
        }
        self.send_version = {
            'ipv4': 0,
            'flowspec': 0,
            'sr_policy': 0,
            'mpls_vpn': 0
        }
        self.receive_version = {
            'ipv4': 0,
            'flowspec': 0,
            'sr_policy': 0,
            'mpls_vpn': 0
        }

        self.flowspec_send_dict = {}
        self.flowspec_receive_dict = {}
        self.sr_send_dict = {}
        self.sr_receive_dict = {}
        self.mpls_vpn_send_dict = {}
        self.mpls_vpn_receive_dict = {}

    @property
    def handler(self):
        # this is due to self.factory is assigned at runtime
        return self.factory.handler

    def init_rib(self):
        self.adj_rib_in = {k: {} for k in CONF.bgp.afi_safi}
        self.adj_rib_out = {k: {} for k in CONF.bgp.afi_safi}

    def connectionMade(self):

        """
        Starts the initial negotiation of the protocol
        """
        self.init_rib()
        # Set transport socket options
        self.transport.setTcpNoDelay(True)
        # set tcp option if you want
        #  self.transport.getHandle().setsockopt(socket.IPPROTO_TCP, TCP_MD5SIG, md5sig)

        LOG.info("[%s]TCP Connection established", self.factory.peer_addr)

        # Set the local BGP id from the local IP address if it's not set
        if self.factory.bgp_id is None:
            try:
                local_host_addr = netaddr.IPAddress(self.transport.getHost().host)
                if 'IPv6' in local_host_addr.info.__iter__():
                    self.factory.bgp_id = int(netaddr.IPAddress('127.0.0.1'))
                else:
                    self.factory.bgp_id = int(local_host_addr)
            except Exception as e:
                LOG.error(e)
                error_str = traceback.format_exc()
                LOG.debug(error_str)
                self.factory.bgp_id = int(netaddr.IPAddress('127.0.0.1'))
        try:
            self.fsm.connection_made()
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)

    def connectionLost(self, reason):
        """Called when the associated connection was lost.
        :param reason: the reason of lost connection.
        """
        LOG.debug('Called connectionLost')
        self.init_rib()
        self.handler.on_connection_lost(self)

        # Don't do anything if we closed the connection explicitly ourselves
        if self.disconnected:
            self.factory.connection_closed(self)
            LOG.info('Connection lost return and do nothing')
            return

        LOG.info("[%s]Connection lost:%s", self.factory.peer_addr, reason.getErrorMessage())

        try:
            # tell FSM that TCP connection is lost.
            self.fsm.connection_failed()
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)

    def dataReceived(self, data):
        """
        Appends newly received data to the receive buffer, and
        then attempts to parse as many BGP messages as possible.

        :param data: the data received from TCP buffer.
        """

        # Buffer possibly incomplete data first
        self._receive_buffer += data
        while self.parse_buffer():
            pass

    def parse_buffer(self):
        """
        Parse TCP buffer data.

        :return: True or False
        """
        buf = self._receive_buffer

        if len(buf) < bgp_cons.HDR_LEN:
            # Every BGP message is at least 19 octets. Maybe the rest
            # hasn't arrived yet.
            return False

        # Check whether the first 16 octets of the buffer consist of
        # the BGP marker (all bits one)
        if buf[:16] != 16 * b'\xff':
            self.fsm.header_error(bgp_cons.ERR_MSG_HDR_CONN_NOT_SYNC)
            return False
            # Parse the BGP header
        try:
            marker, length, msg_type = struct.unpack('!16sHB', buf[:bgp_cons.HDR_LEN])
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)
            self.fsm.header_error(bgp_cons.ERR_MSG_HDR_CONN_NOT_SYNC)
            return False
            # Check the length of the message, must be less than 4096, bigger than 19
        if length < bgp_cons.HDR_LEN or length > bgp_cons.MAX_LEN:
            self.fsm.header_error(bgp_cons.ERR_MSG_HDR_BAD_MSG_LEN, struct.pack('!H', length))
            # Check whether the entire message is already available
        if len(buf) < length:
            return False
        msg = buf[bgp_cons.HDR_LEN:length]
        t = time.time()  # the time when received that packet.
        try:
            if msg_type == bgp_cons.MSG_OPEN:
                try:
                    self._open_received(timestamp=t, msg=msg)
                except excep.MessageHeaderError as e:
                    LOG.error(e)
                    self.fsm.header_error(suberror=e.sub_error)
                    return False
                except excep.OpenMessageError as e:
                    LOG.error(e)
                    self.fsm.open_message_error(suberror=e.sub_error)
                    return False

            elif msg_type == bgp_cons.MSG_UPDATE:
                self._update_received(timestamp=t, msg=msg)

            elif msg_type == bgp_cons.MSG_NOTIFICATION:
                self._notification_received(Notification().parse(msg))

            elif msg_type == bgp_cons.MSG_KEEPALIVE:
                try:
                    self._keepalive_received(timestamp=t, msg=msg)
                except excep.MessageHeaderError as e:
                    LOG.error(e)
                    self.fsm.header_error(suberror=e.sub_error)
                    return False
            elif msg_type in (bgp_cons.MSG_ROUTEREFRESH, bgp_cons.MSG_CISCOROUTEREFRESH):
                route_refresh_msg = RouteRefresh().parse(msg)
                self._route_refresh_received(msg=route_refresh_msg, msg_type=msg_type)
            else:
                # unknown message type
                self.fsm.header_error(
                    bgp_cons.ERR_MSG_HDR_BAD_MSG_TYPE, struct.pack('!H', msg_type))
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)
        self._receive_buffer = self._receive_buffer[length:]
        return True

    def closeConnection(self):
        """Close the connection"""

        if self.transport.connected:
            self.transport.loseConnection()
            self.disconnected = True

    def _update_received(self, timestamp, msg):
        # if self.msg_recv_stat['Updates'] % 1000 == 0:
        #     LOG.info(self.msg_recv_stat['Updates'])
        #     LOG.info(time.time())

        """Called when a BGP Update message was received."""
        # TODO: Need to convert `self.add_path_ipv4_receive` and `self.add_path_ipv4_send` into a unified
        #  `afi_add_path` format.
        result = Update().parse(timestamp, msg, self.fourbytesas, afi_add_path=self.afi_add_path)
        if result['sub_error']:
            msg = {
                'attr': result['attr'],
                'nlri': result['nlri'],
                'withdraw': result['withdraw'],
                'hex': repr(result['hex'])
            }

            self.handler.on_update_error(self, timestamp, msg)

            LOG.error('[%s] Update message error: sub error=%s', self.factory.peer_addr, result['sub_error'])
            self.msg_recv_stat['Updates'] += 1
            self.fsm.update_received()
            return

        afi_safi = None
        # process messages
        if result['nlri'] or result['withdraw']:
            afi_safi = 'ipv4'
        elif result['attr'].get(14):
            afi_safi = bgp_cons.AFI_SAFI_DICT[result['attr'][14]['afi_safi']]
        elif result['attr'].get(15):
            afi_safi = bgp_cons.AFI_SAFI_DICT[result['attr'][15]['afi_safi']]

        msg = {
            'attr': result['attr'],
            'nlri': result['nlri'],
            'withdraw': result['withdraw'],
            'afi_safi': afi_safi
        }

        self.update_receive_verion(result['attr'], result['nlri'], result['withdraw'])

        if CONF.bgp.rib:
            # try to update bgp rib in
            if msg.get('afi_safi') == 'ipv4':
                self.update_rib_in_ipv4(msg)
                # LOG.info(msg)
        self.handler.update_received(self, timestamp, msg)

        self.msg_recv_stat['Updates'] += 1
        self.fsm.update_received()

    def send_update(self, msg):
        """
        send update message to the peer
        :param msg: message dictionary
        :return:
        """
        try:
            msg_update = Update().construct(msg, self.fourbytesas, self.add_path_ipv4_send)
            reactor.callFromThread(self.write_tcp_thread, msg_update)
            self.msg_sent_stat['Updates'] += 1

            return True
        except Exception as e:
            LOG.error(e)
            return False

    def construct_update_to_bin(self, msg):
        """
        construct update message to binary
        :param msg: message dictionary
        :return:
        """
        try:
            msg_update = Update().construct(msg, self.fourbytesas, self.add_path_ipv4_send)
            return msg_update
        except Exception as e:
            LOG.error(e)
            return "construct failed"

    def send_bin_update(self, msg):
        """
        send binary update message to the peer
        :param msg: message dictionary
        :return:
        """
        try:
            reactor.callFromThread(self.write_tcp_thread, msg)
            return True
        except Exception as e:
            LOG.error(e)
            return False

    def write_tcp_thread(self, msg):
        self.transport.write(msg)

    def send_notification(self, error, sub_error, data=b''):
        """
        send BGP notification message

        :param error:
        :param sub_error:
        :param data:
        :return:
        """
        self.msg_sent_stat['Notifications'] += 1
        LOG.info(
            "[%s]Send a BGP Notification message to the peer "
            "[Error: %s, Suberror: %s, Error data: %s ]",
            self.factory.peer_addr, error, sub_error, repr(data))
        # message statistic
        self.msg_sent_stat['Notifications'] += 1
        # construct message
        msg_notification = Notification().construct(error, sub_error, data)
        # send message
        self.transport.write(msg_notification)

    def _notification_received(self, msg):
        """
        BGP notification message received.
        """
        self.msg_recv_stat['Notifications'] += 1
        error_str = bgp_cons.NOTIFICATION_ERROR_CODES_DICT.get(msg[0])
        if error_str:
            sub_error_str = bgp_cons.NOTIFICATION_SUB_ERROR_CODES_DICT.get(msg[0]).get(msg[1])
        else:
            sub_error_str = None
        LOG.info(
            '[%s]Notification message received, error: %s, sub error: %s, data=%s',
            self.factory.peer_addr, error_str, sub_error_str, msg[2])

        nofi_msg = {'error': error_str, 'sub_error': sub_error_str, 'data': repr(msg[2])}

        self.handler.notification_received(self, nofi_msg)

        self.fsm.notification_received(msg[0], msg[1])

        LOG.debug('offline')

    def send_keepalive(self):
        """
        send BGP keepalive message.
        """
        self.msg_sent_stat['Keepalives'] += 1
        LOG.info("[%s]Send a BGP KeepAlive message to the peer.", self.factory.peer_addr)
        # message statistci
        # self.msg_sent_stat['Keepalives'] += 1
        # construct message
        msg_keepalive = KeepAlive().construct()
        # send message
        self.transport.write(msg_keepalive)

    def _keepalive_received(self, timestamp, msg):
        """
            process keepalive message

            :param timestamp:
            :param msg:
            :return:
        """

        # deal with all request in internal message queue
        # until the queue is empty
        while not self.handler.inter_mq.empty() and self.msg_recv_stat['Keepalives'] > 0:
            inter_msg = self.handler.inter_mq.get()
            LOG.debug('Get %s message %s from internal queue', inter_msg['type'], inter_msg['msg'])
            if inter_msg['type'] == 'notification':
                self.send_notification(inter_msg['msg']['error'],
                                       inter_msg['msg']['sub_error'],
                                       inter_msg['msg']['data'])
            elif inter_msg['type'] == 'update':
                self.send_update(inter_msg['msg'])

        self.msg_recv_stat['Keepalives'] += 1

        self.handler.keepalive_received(self, timestamp)

        LOG.info("[%s]A BGP KeepAlive message was received from peer.", self.factory.peer_addr)
        KeepAlive().parse(msg)

        self.fsm.keep_alive_received()

    def capability_negotiate(self):
        """
        Open message capability negotiation
        :return:
        """
        # if received open message from remote peer firstly
        # then copy peer's capability to local according to the
        # local support. best effort support.
        if cfg.CONF.bgp.running_config['capability']['remote']:
            unsupport_cap = []
            for capability in cfg.CONF.bgp.running_config['capability']['local']:
                if capability not in cfg.CONF.bgp.running_config['capability']['remote']:
                    unsupport_cap.append(capability)
            for capability in unsupport_cap:
                cfg.CONF.bgp.running_config['capability']['local'].pop(capability)

    def send_open(self):
        """
        send open message

        :return:
        """
        # construct Open message
        self.capability_negotiate()
        open_msg = Open(
            version=bgp_cons.VERSION, asn=self.factory.my_asn, hold_time=self.fsm.hold_time,
            bgp_id=self.factory.bgp_id). \
            construct(cfg.CONF.bgp.running_config['capability']['local'])
        if 'add_path' in cfg.CONF.bgp.running_config['capability']['local']:
            # check add path feature, send add path condition:
            # local support send or both
            # remote support receive or both
            self.afi_add_path = self.compare_add_path(cfg.CONF.bgp.running_config['capability']['local']['add_path'],
                                                      cfg.CONF.bgp.running_config['capability']['remote'].get('add_path'))
        # send message
        self.transport.write(open_msg)
        self.msg_sent_stat['Opens'] += 1
        LOG.info("[%s]Send a BGP Open message to the peer.", self.factory.peer_addr)
        LOG.info("[%s]Probe's Capabilities:", self.factory.peer_addr)
        for key in cfg.CONF.bgp.running_config['capability']['local']:
            LOG.info("--%s = %s", key, cfg.CONF.bgp.running_config['capability']['local'][key])
        open_msg_dict = {
            "version": bgp_cons.VERSION,
            "asn": self.factory.my_asn,
            "hold_time": self.fsm.hold_time,
            "bgp_id": str(netaddr.IPAddress(self.factory.bgp_id)),
            "capabilities": cfg.CONF.bgp.running_config['capability']['local']
        }
        timestamp = time.time()
        self.handler.send_open(self, timestamp, open_msg_dict)

    def _open_received(self, timestamp, msg):
        """
        porcess open message

        :param timestamp: timestamp that received this message
        :param msg: binary raw message data
        :return:
        """

        self.msg_recv_stat['Opens'] += 1
        open_msg = Open()
        parse_result = open_msg.parse(msg)
        if self.fsm.bgp_peering.peer_asn != open_msg.asn:
            raise excep.OpenMessageError(sub_error=bgp_cons.ERR_MSG_OPEN_BAD_PEER_AS)

        # Open message Capabilities negotiation
        cfg.CONF.bgp.running_config['capability']['remote'] = open_msg.capa_dict
        LOG.info("[%s]A BGP Open message was received", self.factory.peer_addr)
        LOG.info('--version = %s', open_msg.version)
        LOG.info('--ASN = %s', open_msg.asn)
        LOG.info('--hold time = %s', open_msg.hold_time)
        LOG.info('--id = %s', open_msg.bgp_id)
        LOG.info("[%s]Neighbor's Capabilities:", self.factory.peer_addr)
        for key in cfg.CONF.bgp.running_config['capability']['remote']:
            if key == 'four_bytes_as':
                self.fourbytesas = True
            elif key == 'add_path':
                self.afi_add_path = self.compare_add_path(
                    cfg.CONF.bgp.running_config['capability']['local']['add_path'],
                    cfg.CONF.bgp.running_config['capability']['remote'].get('add_path'))

            LOG.info("--%s = %s", key, cfg.CONF.bgp.running_config['capability']['remote'][key])

        self.peer_id = open_msg.bgp_id
        self.bgp_peering.set_peer_id(open_msg.bgp_id)

        self.negotiate_hold_time(open_msg.hold_time)
        self.fsm.open_received()

        self.handler.open_received(self, timestamp, parse_result)

    def send_route_refresh(self, afi, safi, res=0):
        """
        Send bgp route refresh message
        :param afi: address family
        :param safi: sub address family
        :param res: reserve, default is 0
        """
        # check if the peer support route refresh
        if 'cisco_route_refresh' in cfg.CONF.bgp.running_config['capability']['remote']:
            type_code = bgp_cons.MSG_CISCOROUTEREFRESH
        elif 'route_refresh' in cfg.CONF.bgp.running_config['capability']['remote']:
            type_code = bgp_cons.MSG_ROUTEREFRESH
        else:
            return False
        # check if the peer support this address family
        if (afi, safi) not in cfg.CONF.bgp.running_config['capability']['remote']['afi_safi']:
            return False
        # construct message
        msg_routerefresh = RouteRefresh(afi, safi, res).construct(type_code)
        # send message
        self.transport.write(msg_routerefresh)
        self.msg_sent_stat['RouteRefresh'] += 1
        LOG.info("[%s]Send BGP RouteRefresh message to the peer.", self.factory.peer_addr)
        return True

    def _route_refresh_received(self, msg, msg_type):
        """
        Route Refresh message received.

        :param msg: msg content
        :param msg_type: message type 5 or 128
        """
        self.msg_recv_stat['RouteRefresh'] += 1
        LOG.info(
            '[%s]Route Refresh message received, afi=%s, res=%s, safi=%s',
            self.factory.peer_addr, msg[0], msg[1], msg[2])
        nofi_msg = {'afi': msg[0], 'res': msg[1], 'safi': msg[2]}

        self.handler.route_refresh_received(self, nofi_msg, msg_type)

    def negotiate_hold_time(self, hold_time):

        """Negotiates the hold time"""

        self.fsm.hold_time = min(self.fsm.hold_time, hold_time)
        if self.fsm.hold_time != 0 and self.fsm.hold_time < 3:
            self.fsm.open_message_error(bgp_cons.ERR_MSG_OPEN_UNACCPT_HOLD_TIME)
            # Derived times
        self.fsm.keep_alive_time = self.fsm.hold_time / 3
        LOG.info(
            "[%s]Hold time:%s,Keepalive time:%s", self.factory.peer_addr,
            self.fsm.hold_time, self.fsm.keep_alive_time)

    def update_rib_out_ipv4(self, msg):
        try:
            for prefix in msg['withdraw']:
                if prefix in self.adj_rib_out['ipv4']:
                    self.send_version['ipv4'] += 1
                    self.adj_rib_out['ipv4'].pop(prefix)
            for prefix in msg['nlri']:
                if prefix not in self.adj_rib_out['ipv4'].keys():
                    self.send_version['ipv4'] += 1
                else:
                    if msg['attr'] == self.adj_rib_out['ipv4'][prefix]:
                        pass
                    else:
                        self.send_version['ipv4'] += 1
                self.adj_rib_out['ipv4'][prefix] = msg['attr']
            return True
        except Exception as e:
            LOG.error(e)
            return False

    def update_rib_in_ipv4(self, msg):
        try:
            for prefix in msg['withdraw']:
                if prefix in self.adj_rib_in['ipv4']:
                    self.receive_version['ipv4'] += 1
                    self.adj_rib_in['ipv4'].pop(prefix)
                    if self.adj_rib_in_ipv4_tree.search_exact(prefix):
                        self.adj_rib_in_ipv4_tree.delete(prefix)
            for prefix in msg['nlri']:
                if prefix not in self.adj_rib_in['ipv4'].keys():
                    self.receive_version['ipv4'] += 1
                else:
                    if msg['attr'] == self.adj_rib_in['ipv4'][prefix]:
                        pass
                    else:
                        self.receive_version['ipv4'] += 1
                self.adj_rib_in['ipv4'][prefix] = msg['attr']
                self.adj_rib_in_ipv4_tree.add(prefix)
            return True
        except Exception as e:
            LOG.error(e)
            LOG.debug(traceback.format_exc())
            return False

    def ip_longest_match(self, prefix_ip):
        results = {}
        if '/' in prefix_ip:
            if self.adj_rib_in['ipv4'].get(prefix_ip):
                return {
                    'prefix': prefix_ip,
                    'attr': self.adj_rib_in['ipv4'].get(prefix_ip)
                }
        if prefix_ip in self.adj_rib_in_ipv4_tree:
            prefix_node = self.adj_rib_in_ipv4_tree.search_best(prefix_ip)
            if prefix_node:
                if self.adj_rib_in['ipv4'].get(prefix_node.prefix):
                    return {
                        'prefix': prefix_node.prefix,
                        'attr': self.adj_rib_in['ipv4'].get(prefix_node.prefix)
                    }
        return results

    def update_send_version(self, peer_ip, attr, nlri, withdraw):
        if 14 in attr:
            if attr[14]['afi_safi'] == [1, 133]:
                LOG.info("send flowspec")
                for prefix in attr[14]['nlri']:
                    value = copy.deepcopy(attr)
                    value14 = value[14]
                    del value14['nlri']
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) not in self.flowspec_send_dict:
                        self.send_version['flowspec'] += 1
                        self.flowspec_send_dict[str(key)] = value
                    else:
                        if value == self.flowspec_send_dict[str(key)]:
                            pass
                        else:
                            self.send_version['flowspec'] += 1
                            self.flowspec_send_dict[str(key)] = value
            elif attr[14]['afi_safi'] == [1, 73]:
                LOG.info('send sr')
                key = "{"
                for k in sorted(attr[14]['nlri'].keys()):
                    key += '"' + k + '"'
                    key += ':'
                    key += '"' + str(attr[14]['nlri'][k]) + '"'
                    key += ','
                key = key[:-1]
                key += "}"
                if str(key) not in self.sr_send_dict:
                    self.send_version['sr_policy'] += 1
                    self.sr_send_dict[str(key)] = attr
                else:
                    if attr == self.sr_send_dict[str(key)]:
                        pass
                    else:
                        self.send_version['sr_policy'] += 1
                        self.sr_send_dict[str(key)] = attr
            elif attr[14]['afi_safi'] == [1, 128]:
                LOG.info("send mpls_vpn")
                for prefix in attr[14]['nlri']:
                    value = copy.deepcopy(attr)
                    value14 = value[14]
                    del value14['nlri']
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) not in self.mpls_vpn_send_dict:
                        self.send_version['mpls_vpn'] += 1
                        self.mpls_vpn_send_dict[str(key)] = value
                    else:
                        if value == self.mpls_vpn_send_dict[str(key)]:
                            pass
                        else:
                            self.send_version['mpls_vpn'] += 1
                            self.mpls_vpn_send_dict[str(key)] = value
        # flowspec sr mpls_vpn withdraw
        if 15 in attr:
            if attr[15]['afi_safi'] == [1, 133]:
                LOG.info("withdraw flowspec")
                for prefix in attr[15]['withdraw']:
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) in self.flowspec_send_dict:
                        self.send_version['flowspec'] += 1
                        del self.flowspec_send_dict[str(key)]
                    else:
                        LOG.info("Do not have %s in send flowspec dict" % key)
            elif attr[15]['afi_safi'] == [1, 73]:
                LOG.info('withdraw sr')
                key = "{"
                for k in sorted(attr[15]['withdraw'].keys()):
                    key += '"' + k + '"'
                    key += ':'
                    key += '"' + str(attr[15]['withdraw'][k]) + '"'
                    key += ','
                key = key[:-1]
                key += "}"
                if str(key) in self.sr_send_dict:
                    self.send_version['sr_policy'] += 1
                    del self.sr_send_dict[str(key)]
                else:
                    LOG.info("Do not have %s in send flowspec dict" % key)
            elif attr[15]['afi_safi'] == [1, 128]:
                LOG.info("withdraw mpls_vpn")
                for prefix in attr[15]['withdraw']:
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) in self.mpls_vpn_send_dict:
                        self.send_version['mpls_vpn'] += 1
                        del self.mpls_vpn_send_dict[str(key)]
                    else:
                        LOG.info("Do not have %s in send flowspec dict" % key)

    def update_receive_verion(self, attr, nlri, withdraw):
        if 14 in attr:
            if attr[14]['afi_safi'] == [1, 133]:
                LOG.info("recieve flowspec send")
                for prefix in attr[14]['nlri']:
                    value = copy.deepcopy(attr)
                    value14 = value[14]
                    del value14['nlri']
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) not in self.flowspec_receive_dict:
                        self.receive_version['flowspec'] += 1
                        self.flowspec_receive_dict[str(key)] = value
                    else:
                        if value == self.flowspec_receive_dict[str(key)]:
                            pass
                        else:
                            self.receive_version['flowspec'] += 1
                            self.flowspec_receive_dict[str(key)] = value
            elif attr[14]['afi_safi'] == [1, 73]:
                LOG.info('recieve sr send')
            elif attr[14]['afi_safi'] == [1, 128]:
                LOG.info("receive send mpls_vpn")
                for prefix in attr[14]['nlri']:
                    value = copy.deepcopy(attr)
                    value14 = value[14]
                    del value14['nlri']
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) not in self.mpls_vpn_receive_dict:
                        self.receive_version['mpls_vpn'] += 1
                        self.mpls_vpn_receive_dict[str(key)] = value
                    else:
                        if value == self.mpls_vpn_receive_dict[str(key)]:
                            pass
                        else:
                            self.receive_version['mpls_vpn'] += 1
                            self.mpls_vpn_receive_dict[str(key)] = value
        # receive flowspec sr mpls withdraw
        if 15 in attr:
            if attr[15]['afi_safi'] == [1, 133]:
                LOG.info("recieve flowspec withdraw")
                for prefix in attr[15]['withdraw']:
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) in self.flowspec_receive_dict:
                        self.receive_version['flowspec'] += 1
                        del self.flowspec_receive_dict[str(key)]
                    else:
                        LOG.info("Do not have %s in receive flowspec dict" % prefix)
            elif attr[15]['afi_safi'] == [1, 73]:
                LOG.info('recieve sr withdraw')
            elif attr[15]['afi_safi'] == [1, 128]:
                LOG.info("recieve withdraw mpls_vpn")
                for prefix in attr[15]['withdraw']:
                    key = "{"
                    for k in sorted(prefix.keys()):
                        key += '"' + k + '"'
                        key += ':'
                        key += '"' + str(prefix[k]) + '"'
                        key += ','
                    key = key[:-1]
                    key += "}"
                    if str(key) in self.mpls_vpn_receive_dict:
                        self.receive_version['mpls_vpn'] += 1
                        del self.mpls_vpn_receive_dict[str(key)]
                    else:
                        LOG.info("Do not have %s in receive mpls_vpn dict" % key)

    def compare_add_path(self, local_add_path, remote_add_path):
        if not local_add_path or not remote_add_path:
            return None

        afi_add_path = {}
        for local in local_add_path:
            for remote in remote_add_path:
                if local.get('afi_safi') == remote.get('afi_safi'):
                    if local.get('send/receive') in ['receive', 'both'] and remote.get('send/receive') in ['send', 'both']:
                        afi_add_path[local.get('afi_safi')] = True
                    else:
                        afi_add_path[local.get('afi_safi')] = False

        return afi_add_path
