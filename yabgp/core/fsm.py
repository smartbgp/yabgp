# Copyright (c) 2007 by Mark Bergsma <mark@nedworks.org>
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

"""BGP FMS Implementation"""

import time
import logging

from yabgp.core.timer import BGPTimer
from yabgp.common import constants as bgp_cons

LOG = logging.getLogger(__name__)


class FSM(object):

    """
    Implements BGP Events described in section 8.1 of RFC 4271
    Implements BGP finite state machine described in section 8.2 of RFC 4271
    """

    protocol = None
    state = bgp_cons.ST_IDLE
    large_hold_time = bgp_cons.LARGER_HOLD_TIME

    def __init__(self, bgp_peering=None, protocol=None):

        """
        please see RFC 4271 page 37 for value meanning
        """

        self.bgp_peering = bgp_peering
        self.protocol = protocol

        # Session attributes required (mandatory) for each connection:
        self.state = bgp_cons.ST_IDLE
        self.connect_retry_counter = 0
        self.connect_retry_time = bgp_cons.CONNECT_RETRY_TIME
        self.connect_retry_timer = BGPTimer(self.connect_retry_time_event)
        self.hold_time = bgp_cons.HOLD_TIME

        self.hold_timer = BGPTimer(self.hold_time_event)
        self.keep_alive_time = self.hold_time / 3
        self.keep_alive_timer = BGPTimer(self.keep_alive_time_event)

        self.allow_automatic_start = True
        self.allow_automatic_stop = False
        self.delay_open = False
        self.delay_open_time = bgp_cons.DELAY_OPEN_TIME
        self.delay_open_timer = BGPTimer(self.delay_open_time_event)
        self.idle_hold_time = bgp_cons.IDLEHOLD_TIME
        self.idle_hold_timer = BGPTimer(self.idle_hold_time_event)

        self.uptime = None

    def __setattr__(self, name, value):

        if name == 'state' and value != getattr(self, name):
            LOG.info("[%s]State is now:%s", self.bgp_peering.peer_addr, bgp_cons.stateDescr[value])
            if value == bgp_cons.ST_ESTABLISHED:
                self.uptime = time.time()
        super(FSM, self).__setattr__(name, value)

    def manual_start(self):

        """
        Event 1: ManualStart
        Definiton: Should be called when a BGP ManualStart event is requested.
                   Note that a protocol instance does not yet exist at this point,
                   so this method requires some support from BGPPeering.manual_start().
        Status: Mandatory
        """
        LOG.info('Manual start.')
        if self.state == bgp_cons.ST_IDLE:
            self.connect_retry_counter = 0
            self.connect_retry_timer.reset(self.connect_retry_time)

    def manual_stop(self):

        """
        Event 2: ManualStop
        Definition: Should be called when a BGP ManualStop event is requested.
        Status: Mandatory
        """
        LOG.info('Manual stop')
        if self.state != bgp_cons.ST_IDLE:

            self.protocol.send_notification(bgp_cons.ERR_CEASE, 0)
            # Stop all timers
            LOG.info('Stop all timers')
            for timer in (self.connect_retry_timer, self.hold_timer, self.keep_alive_timer,
                          self.delay_open_timer, self.idle_hold_timer):
                timer.cancel()
                LOG.info('-- Stop timer %s', timer)
            self._close_connection()
            self.connect_retry_counter = 0
            self.allow_automatic_start = False
            self.state = bgp_cons.ST_IDLE

    def automatic_start(self, idle_hold=False):

        """
        Event 3: AutomaticStart
        Definition: Should be called when a BGP Automatic Start event is requested.
                    Returns True or False to indicate BGPPeering whether a connection
                    attempt should be initiated.
        Status: Optional

        :param idle_hold: BGP Idle Hold or not.
        """
        LOG.info('Automatic start')
        if self.state in [bgp_cons.ST_IDLE, bgp_cons.ST_CONNECT]:
            if idle_hold:
                LOG.info('Idle Hold, please wait time=%s', self.idle_hold_time)
                self.idle_hold_timer.reset(self.idle_hold_time)
                return False
            elif self.allow_automatic_start:
                LOG.info('Do not need Idle Hold, start right now.')
                LOG.info('Connect retry counter: %s', self.connect_retry_counter)
                self.connect_retry_counter += 1
                self.connect_retry_timer.reset(self.connect_retry_time)
                LOG.info('Connect retry timer, time=%s', self.connect_retry_time)
                self.state = bgp_cons.ST_CONNECT
                return True
            else:
                return False
        else:
            return False

    def connect_retry_time_event(self):

        """
        Event 9: ConnectRetryTimer_Expires
        Definition: Called when the ConnectRetryTimer expires.
        Status: Mandatory
        """
        LOG.info('Connect retry timer expires')
        if self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            # State Connect, event 9
            self._close_connection()
            LOG.info('Reset connect retry timer, time=%s', self.connect_retry_time)
            self.connect_retry_timer.reset(self.connect_retry_time)
            self.delay_open_timer.cancel()
            LOG.info('Cancel delay open timer')
            # Initiate TCP connection
            if self.bgp_peering:
                LOG.info('Bgp peering connect retry')
                self.bgp_peering.connect_retry()
        elif self.state != bgp_cons.ST_IDLE:
            # State OpenSent, OpenConfirm, Established, event 12
            self.protocol.send_notification(bgp_cons.ERR_FSM, 0)
            self._error_close()

    def hold_time_event(self):

        """
        Event 10:   HoldTimer_Expires
        Definition: Called when the HoldTimer expires.
        Action:     NOTIFICATION message with the Hold Timer Expried Error
                    Code is sent and the BGP connection is closed
        Status:     Mandatory
        """
        LOG.info('Hold Timer expires')
        if self.state in (bgp_cons.ST_OPENSENT, bgp_cons.ST_OPENCONFIRM, bgp_cons.ST_ESTABLISHED):
            # States OpenSent, OpenConfirm, Established, event 10
            self.protocol.send_notification(bgp_cons.ERR_HOLD_TIMER_EXPIRED, 0)
            self.connect_retry_timer.cancel()
            self._error_close()
            self.state = bgp_cons.ST_IDLE
        elif self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            self._error_close()

    def keep_alive_time_event(self):

        """
        Event 11:   KeepaliveTimer_Expires
        Definition: Called when the KeepAliveTimer expires.
        Action:     Send Keepalive messsage if the state of FSM is ST_OPENCONFIRM
                    or ST_ESTABLISHED, close BGP connection if state is others
        Status: Mandatory
        """
        LOG.info('Keep alive timer expires')
        if self.state in (bgp_cons.ST_OPENCONFIRM, bgp_cons.ST_ESTABLISHED):
            # State OpenConfirm, Established, event 11
            self.protocol.send_keepalive()
            if self.hold_time > 0:
                self.keep_alive_timer.reset(self.keep_alive_time)
        elif self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            self._error_close()

    def delay_open_time_event(self):

        """
        Event 12: DelayOpenTimer_Expires
        Definition: Called when the DelayOpenTimer expires.
        Status: Optional
        """
        LOG.info('Delay open timer expires')
        # DelayOpen attribute SHOULD be set to TRUE

        if self.state == bgp_cons.ST_CONNECT:
            # State Connect, event 12
            self.protocol.send_open()
            self.hold_timer.reset(self.large_hold_time)
            self.state = bgp_cons.ST_OPENSENT
        elif self.state == bgp_cons.ST_ACTIVE:
            # State Active, event 12
            self.connect_retry_timer.cancel()
            self.delay_open_timer.cancel()
            self.protocol.send_open()
            self.hold_timer.reset(self.large_hold_time)
            self.state = bgp_cons.ST_OPENSENT
        elif self.state != bgp_cons.ST_IDLE:
            # State OpenSent, OpenConfirm, Established, event 12
            self.protocol.send_notification(bgp_cons.ERR_FSM, 0)
            self._error_close()

    def idle_hold_time_event(self):

        """
        Event 13: IdleHoldTimer_Expires
        Definition: Called when the IdleHoldTimer expires.
        Status: Optional
        """
        # DampPeerOscillations attribute SHOULD be set to TRUE
        # assert(self.dampPeerOscillations)
        LOG.info('Idle Hold Timer expires')
        if self.state == bgp_cons.ST_IDLE:
            if self.bgp_peering:
                self.bgp_peering.automatic_start(idle_hold=False)

    def connection_made(self):

        """
        Event 16: Tcp_CR_Acked
        Event 17: TcpConnectionConfirmed
        Definition: Should be called when a TCP connection has successfully been
                    established with the peer.
        Status: Mandatory
        """
        if self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            # State Connect, Event 16 or 17
            if self.delay_open:
                self.connect_retry_timer.cancel()
                LOG.info('Delay open for this peer')
                self.delay_open_timer.reset(self.delay_open_time)
            else:
                self.connect_retry_timer.cancel()
                self.protocol.send_open()
                self.hold_timer.reset(self.large_hold_time)
                self.state = bgp_cons.ST_OPENSENT

    def connection_failed(self):

        """
        Event 18: TcpConnectionFails
        Definition: Should be called when the associated TCP connection failed,
                    or was lost.
        Status: Mandatory
        """
        if self.state == bgp_cons.ST_CONNECT:
            # State Connect, event 18
            if self.delay_open_timer.active():
                self.connect_retry_timer.reset(self.connect_retry_time)
                self.delay_open_timer.cancel()
                self.state = bgp_cons.ST_ACTIVE
            else:
                self.connect_retry_timer.cancel()
                self._close_connection()
                if self.bgp_peering:
                    self.state = bgp_cons.ST_IDLE
                    self.bgp_peering.connection_closed(self.protocol)
        elif self.state == bgp_cons.ST_ACTIVE:
            # State Active, event 18
            self.connect_retry_timer.reset(self.connect_retry_time)
            self.delay_open_timer.cancel()
            if self.bgp_peering:
                # self.bgp_peering.releaseResources(self.protocol)
                pass
            # TODO: osc damping
            self.state = bgp_cons.ST_IDLE
        elif self.state == bgp_cons.ST_OPENSENT:
            # State OpenSent, event 18
            if self.bgp_peering:
                # self.bgp_peering.releaseResources(self.protocol)
                pass
            self._close_connection()
            self.connect_retry_timer.reset(self.connect_retry_time)
            self.state = bgp_cons.ST_ACTIVE
            if self.bgp_peering:
                self.bgp_peering.connection_closed(self.protocol)
        elif self.state in (bgp_cons.ST_OPENCONFIRM, bgp_cons.ST_ESTABLISHED):
            self._error_close()

    def open_received(self):

        """
        Event 19: BGPOpen
        Event 20: BGPOpen with DelayOpenTimer running
        Definition: Should be called when a BGP Open message was
                    received from the peer.
        Status: Mandatory
        """

        if self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            if self.delay_open_timer.active():
                # State Connect, event 20
                self.connect_retry_timer.cancel()
                self.delay_open_timer.cancel()
                self.connect_retry_counter = 0
                self.protocol.send_open()
                self.protocol.send_keepalive()
                if self.hold_time:
                    self.keep_alive_timer.reset(self.keep_alive_time)
                    self.hold_timer.reset(self.hold_time)
                else:    # holdTime == 0
                    self.keep_alive_timer.cancel()
                    self.hold_timer.cancel()

                self.state = bgp_cons.ST_OPENCONFIRM
            else:
                # State Connect, event 19
                self._error_close()

        elif self.state == bgp_cons.ST_OPENSENT:
            # State OpenSent, events 19, 20
            self.delay_open_timer.cancel()
            self.connect_retry_timer.cancel()
            self.protocol.send_keepalive()
            if self.hold_time > 0:
                self.keep_alive_timer.reset(self.keep_alive_time)
                self.hold_timer.reset(self.hold_time)
            self.state = bgp_cons.ST_OPENCONFIRM

        elif self.state == bgp_cons.ST_OPENCONFIRM:
            # State OpenConfirm, events 19, 20
            # TODO:Perform collision detection
            pass

        elif self.state == bgp_cons.ST_ESTABLISHED:
            # State Established, event 19 or 20
            self.protocol.send_notification(bgp_cons.ERR_FSM, 0)
            self._error_close()

    def header_error(self, suberror, data=b''):

        """
        Event 21: BGPHeaderErr
        Definition: Should be called when an invalid BGP
                    message header was received.
        Status: Mandatory

        :param suberror: bgp notification sub error code
        :param data: bgp notification error data
        """

        self.protocol.send_notification(bgp_cons.ERR_MSG_HDR, suberror, data)
        # Note: RFC4271 states that we should send ERR_FSM in the
        # Established state, which contradicts earlier statements.
        self._error_close()

    def open_message_error(self, suberror, data=b''):

        """
        Event 22: BGPOpenMsgErr
        Definition: Should be called when an invalid BGP
                    Open message was received.
        Status: Mandatory

        :param suberror: bgp notification sub error code
        :param data: bgp notification error data
        """

        self.protocol.send_notification(bgp_cons.ERR_MSG_OPEN, suberror, data)
        # Note: RFC4271 states that we should send ERR_FSM in the
        # Established state, which contradicts earlier statements.
        self._error_close()

    def notimsg_version_error(self):

        """
        Event 24: NotifMsgVerErr
        Definition: Should be called when a BGP Notification Open Version
                    Error message was received from the peer.
        Status: Mandatory
        """

        if self.state in (bgp_cons.ST_OPENSENT, bgp_cons.ST_OPENCONFIRM):
            # State OpenSent, event 24
            self.connect_retry_timer.cancel()
            self._close_connection()
            self.state = bgp_cons.ST_IDLE
        elif self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            # State Connect, event 24
            self._error_close()

    def notification_received(self, error, suberror):

        """
        Event 25: NotifMsg
        Definition: Should be called when a BGP Notification message was
                    received from the peer.
        Status: Mandatory

        :param error: bgp notification error code
        :param suberror: bgp notification sub error code
        """

        if error == bgp_cons.ERR_MSG_OPEN and suberror == 1:
            # Event 24 : version error
            self.notimsg_version_error()
        else:
            if self.state != bgp_cons.ST_IDLE:
                # State != Idle, events 24, 25
                self._error_close()

    def keep_alive_received(self):

        """
        Event 26: KeepAliveMsg
        Definition: Should be called when a BGP KeepAlive packet
                    was received from the peer.
        Status: Mandatory
        """

        if self.state == bgp_cons.ST_OPENCONFIRM:
            # State OpenSent, event 26
            self.hold_timer.reset(self.hold_time)
            self.state = bgp_cons.ST_ESTABLISHED
        elif self.state == bgp_cons.ST_ESTABLISHED:
            # State Established, event 26
            self.hold_timer.reset(self.hold_time)
        elif self.state in (bgp_cons.ST_CONNECT, bgp_cons.ST_ACTIVE):
            # States Connect, Active, event 26
            self._error_close()

    def update_received(self):

        """
        Event 27: UpdateMsg
        Definition: Called when a valid BGP Update message was received.
        Status: Mandatory
        """

        if self.state == bgp_cons.ST_ESTABLISHED:
            # State Established, event 27
            if self.hold_time != 0:
                self.hold_timer.reset(self.hold_time)

        elif self.state in (bgp_cons.ST_ACTIVE, bgp_cons.ST_CONNECT):
            # States Active, Connect, event 27
            self._error_close()
        elif self.state in (bgp_cons.ST_OPENSENT, bgp_cons.ST_OPENCONFIRM):
            # States OpenSent, OpenConfirm, event 27
            self.protocol.send_notification(bgp_cons.ERR_FSM, 0)
            self._error_close()

    def update_sent(self):

        """Called by the protocol instance when it just sent an Update message."""

        if self.hold_time > 0:
            self.keep_alive_timer.reset(self.keep_alive_time)

    def _error_close(self):

        """Internal method that closes a connection and returns the state
        to IDLE.
        """

        # Stop the timers
        for timer in (self.connect_retry_timer, self.delay_open_timer, self.hold_timer, self.keep_alive_timer):
            timer.cancel()

        self.idle_hold_timer.reset(self.idle_hold_time)

        # Release BGP resources (routes, etc)
        if self.bgp_peering:
            # self.bgp_peering.releaseResources(self.protocol)
            pass

        self._close_connection()

        self.connect_retry_counter += 1
        self.state = self.bgp_peering.fsm.state = bgp_cons.ST_IDLE

    def _close_connection(self):

        """Internal method that close the connection if a valid BGP protocol
        instance exists.
        """
        if self.protocol is not None:
            self.protocol.closeConnection()
            self.connect_retry_counter = 0
            LOG.info('Closing protocol connection.')
