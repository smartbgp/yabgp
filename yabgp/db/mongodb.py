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

""" mongodb """

import logging

import pymongo

LOG = logging.getLogger(__name__)


class MongoApi(object):
    """Class handling MongoDB specific functionality.

    This class uses PyMongo APIs internally to create database connection,
    also serves as handle to collection for get/set operations, etc.

    """
    # class level attributes for re-use of db client connection and collection
    _DB = {}  # dict of db_name: db connection reference
    _MONGO_COLLS = {}  # dict of cache_collection : db collection reference

    def __init__(self, connection_url, db_name, use_replica=False, replica_name='rs1',
                 read_preference=3, write_concern=-1, w_timeout=5000):
        """for parameters details, please see
        http://api.mongodb.org/python/current/api/pymongo/mongo_client.html

        :param connection_url: string like mongodb://localhost:27017
        :param db_name: database name, string
        :param use_replica: if use replica, true of false
        :param replica_name: if use replica, then the replica set name
        :param read_preference: read preference, interger
        :param write_concern: write concern, interger
        :param w_timeout: write concern timeout, interger
        """
        LOG.debug('Creating MongoDB API class')
        self.conection_url = connection_url
        self.db_name = db_name
        self.collection_name = None

        # config about replica set
        self.use_replica = use_replica
        self.replica_name = replica_name
        self.read_preference = read_preference

        # Write Concern options:
        self.w = write_concern
        self.w_timeout = w_timeout

    def _get_db(self):
        """
        get database
        :return: database
        """
        try:
            if self.use_replica:  # if use replica set configuration
                connection = pymongo.MongoClient(
                    self.conection_url, replicaSet=self.replica_name)
            else:  # use for standalone node or mongos in sharded setup
                connection = pymongo.MongoClient(self.conection_url)

        except pymongo.errors.ConnectionFailure as e:
            LOG.warn('Unable to connect to the database server, %s', e)
            raise

        database = getattr(connection, self.db_name)
        return database

    def _close_db(self):
        if self.db_name in self._DB:
            self._DB[self.db_name].client.close()
            self._DB.pop(self.db_name)

    def get_collection(self):
        """
        get collection
        :return: database collection
        """
        if self.collection_name not in self._MONGO_COLLS:

            if self.db_name not in self._DB:
                self._DB[self.db_name] = self._get_db()
            coll = getattr(self._DB[self.db_name], self.collection_name)

            if self.use_replica:
                # for read preference
                # TODO(xiaoquwl) fix this as more elegant way in future
                if self.read_preference is not None:
                    if self.read_preference == 0:
                        coll.with_options(read_preference=pymongo.ReadPreference.PRIMARY)
                    elif self.read_preference == 1:
                        coll.with_options(read_preference=pymongo.ReadPreference.PRIMARY_PREFERRED)
                    elif self.read_preference == 2:
                        coll.with_options(read_preference=pymongo.ReadPreference.SECONDARY)
                    elif self.read_preference == 3:
                        coll.with_options(read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)
                    elif self.read_preference == 4:
                        coll.with_options(read_preference=pymongo.ReadPreference.NEAREST)
                    else:
                        LOG.error('unknow read preference setting')
                        pass

                # for write concern
                if self.w > -1:
                    coll.write_concern['w'] = self.w
                    coll.write_concern['wtimeout'] = 5000

            self._MONGO_COLLS[self.collection_name] = coll

        return self._MONGO_COLLS[self.collection_name]

    def remove_collection(self):
        self._DB[self.db_name].drop_collection(self.collection_name)
