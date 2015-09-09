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

FILTER_TYPE_PREFIX = 'prefix'
FILTER_TYPE_COMMUNITY = 'community'
FILTER_TYPE_AS_PATH = 'as_path'

FILTER_TYPE_LIST = [FILTER_TYPE_PREFIX, FILTER_TYPE_COMMUNITY, FILTER_TYPE_AS_PATH]

FILTER_TYPR_INIT_DICT = dict([(k, {}) for k in FILTER_TYPE_LIST])
