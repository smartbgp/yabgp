#!/usr/bin/env bash

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

echo "Please makesure you have installed docker and can run as no-root user"
echo "if yes, please press Enter..."
read

# for rabbitmq
echo "Starting rabbitmq..."
docker pull tutum/rabbitmq
docker run -d -p 5672:5672 -p 15672:15672 tutum/rabbitmq

# for mongodb
echo "starting mongodb replica set"
docker pull tattsun/mongodb-replset

cd ~
for ((i=1; i<4; i++)); do
    if ! [ -d data/mongo/node$i ]; then
        mkdir -p data/mongo/node$i
    fi
done

SCRIPTPATH=`pwd -P`

docker run -p 27017:27017 -p 27018:27018 -p 27019:27019 -d \
    -v /host/primary:$SCRIPTPATH/data/mongo/node1 -v /host/secondary:$SCRIPTPATH/data/mongo/node2 \
    tattsun/mongodb-replset
