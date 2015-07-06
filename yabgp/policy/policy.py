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

"""BGP RIB in and out policy
"""


class Rules(dict):
    """Route Policy Rules"""

    def __init__(self, rules=None, default_rule=None):
        """Initialize the Route Policy Rules"""

        super(Rules, self).__init__(rules or {})
        self.default_rule = default_rule

    @classmethod
    def from_dict(cls, rules_dict, default_rule=None):
        pass

    @classmethod
    def from_database(cls):
        pass
