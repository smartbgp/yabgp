#!/bin/bash

set -e

yabgpd --bgp-local_as=$LOCAL_AS --bgp-remote_addr=$REMOTE_IP --bgp-remote_as=$REMOTE_AS \
 --bgp-afi_safi=$AFI_SAFI --log-file=/root/data/bgp/$REMOTE_IP/log/yabgp.log --nouse-stderr