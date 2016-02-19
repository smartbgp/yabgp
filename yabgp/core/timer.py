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

""" BGP Timer"""

# Twisted modules
from twisted.internet import reactor, error


class BGPTimer(object):
    """
    Timer class with a slightly different Timer interface than the
    Twisted DelayedCall interface
    """

    def __init__(self, call_able, name):

        self.name = name
        self.status = False
        self.delayed_call = None
        self.callable = call_able

    def cancel(self):

        """Cancels the timer if it was running, does nothing otherwise"""

        try:
            self.delayed_call.cancel()
            self.status = False
        except (AttributeError, error.AlreadyCalled, error.AlreadyCancelled):
            pass

    def reset(self, seconds_fromnow):
        """Resets an already running timer, or starts it if it wasn't running.

        :param seconds_fromnow : restart timer
        """

        try:
            self.status = True
            self.delayed_call.reset(seconds_fromnow)
        except (AttributeError, error.AlreadyCalled, error.AlreadyCancelled):
            self.delayed_call = reactor.callLater(seconds_fromnow, self.callable)

    def active(self):
        """Returns True if the timer was running, False otherwise."""

        try:
            self.status = True
            return self.delayed_call.active()
        except AttributeError:
            return False
