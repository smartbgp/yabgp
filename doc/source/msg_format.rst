BGP Message Format
==================

Basic
-----

BGP message is **json** format, and it has four keys: ``t``, ``seq``, ``type`` and ``msg``.

``t`` is timestamp,  it is a standard unix time stamp, the number of seconds since 00:00:00 UTC on January 1, 1970.

Example:

.. code-block:: python

    timestamp = 1372051151.2572551 # that is Mon Jun 24 13:19:11 2013.

``seq`` is sequence number  It is a interger and represents the message number.

``type`` It is a interger that represents the message type.

there are eight types of message now.

============  =============================
Type          Description
============  =============================
0             Session information Message
1             BGP Open Message
2             BGP Update Message
3             BGP Notification Message
4             BGP Keepalive Message
5             BGP Route Refresh Message
128           BGP Cisco Route Refresh Message
6             Malformed Update Message
============  =============================

``msg`` is the message contents, and its format is different according to different message types.

Session Info Message
--------------------

Session information message (type = 0) always represents the TCP connection is closed by some reason, for example, the connection
is refused or the connection is reset by the other site.

.. code-block:: json

    {
        "t": 1372065358.666234,
        "seq": 12,
        "type": 0,
        "msg": "Connection lost:Connection to the other side was lost in a non-clean fashion."
    }
    {
        "t": 1451360038.041204,
        "seq": 1,
        "type": 0,
        "msg": "Client connection failed: Couldn't bind: 49: Can't assign requested address."
    }

Open Message
------------

BGP Open message (type = 1). for the meaning of the keys, please check RFC 4271 section 4.2.

.. code-block:: json

    {
        "t": 1452008814.016207,
        "seq": 1,
        "type": 1,
        "msg":{
            "hold_time": 180,
            "capabilities": {
                "cisco_route_refresh": true,
                "route_refresh": true,
                "graceful_restart": true,
                "add_path": "ipv4_both",
                "four_bytes_as": true,
                "afi_safi": [[1, 1], [1, 133]]
            },
            "bgp_id": "9.9.9.9",
            "version": 4,
            "asn": 9308
        }
    }

Update Message
--------------

BGP Update message (type = 2), the value of ``msg`` for a update message is a dict, and it
has four keys : ``attr``, ``nlri``, ``withdraw`` and ``afi_safi``.

=========== ========   ==============
Key         Value      Description
=========== ========   ==============
"attr"      dict       Path Attributes
"nlri"      list       Network Layer Reachability Information
"withdraw"  list       Withdrawn Routes
"afi_safi"  string     address family
=========== ========   ==============

simple format:

.. code-block:: json

    {
        "msg":{
            "attr": {},
            "withdraw": [],
            "nlri": [],
            "afi_safi": "ipv4"
        }
    }

and here is a full BGP update message example:

.. code-block:: json

    {
        "t": 1450668281.624188,
        "seq": 17,
        "type": 2,
        "msg": {
            "attr": {
                "1": 0,
                "2": [[2, [209, 2768, 2768, 2768, 2768]]],
                "3": "1.1.1.2",
                "5": 500,
                "8": ["1234:5678", "2345:6789"],
                "9": "1.1.1.2",
                "10": ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
            },
            "nlri": ["65.122.75.0/24", "65.122.74.0/24"],
            "withdraw": [],
            "afi_safi": "ipv4"
        }
    }

and here is a withdraw message:

.. code-block:: json

    {
        "t": 1450163221.123568,
        "seq": 17,
        "type": 2,
        "msg": {
            "attr": {},
            "nlri": [],
            "withdraw": ["65.122.75.0/24", "65.122.74.0/24"]
            "afi_safi": "ipv4"
        }
    }

The ``withdraw`` and ``nlri`` are all List, they contain the particular prefix string.
Here is one real BGP decoded message example

Example for a ``nlri`` or ``withdraw`` value:

.. code-block:: json

    ["1.1.1.1/32", "2.2.2.2/32"]

The value of key ``attr`` is a dictionary. it contains the BGP prefix's attribute, the dict's key represent
what of kind of attribute, and the value is this attribute's value.

The attribute we supported now is: (reference by `IANA <http://www.iana.org/assignments/bgp-parameters/bgp-parameters.xml>`_)

.. code-block:: json
    :emphasize-lines: 3,5

    {
        "1": "ORIGIN",
        "2": "AS_PATH",
        "3": "NEXT_HOP",
        "4": "MULTI_EXIT_DISC",
        "5": "LOCAL_PREF",
        "6": "ATOMIC_AGGREGATE",
        "7": "AGGREGATOR",
        "8": "COMMUNITY",
        "9": "ORIGINATOR_ID",
        "10": "CLUSTER_LIST",
        "14": "MP_REACH_NLRI",
        "15": "MP_UNREACH_NLRI",
        "16": "EXTENDED_COMMUNITY",
        "17": "AS4_PATH",
        "18": "AS4_AGGREGATOR",
        "22": "PMSI_TUNNEL",
        "23": "TUNNEL_ENCAPSULATIONS",
        "128": "ATTR_SET"
    }

Example for ``attr`` value:

.. code-block:: json

    {
        "1": 0,
        "2": [[2, [209, 2768, 2768, 2768, 2768]]],
        "3": "1.1.1.2",
        "5": 500,
        "8": ["1234:5678", "5678:1234"],
        "9": "1.1.1.2",
        "10": ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
    }

Next, we will explain the detail structure of each attribute.

1. ORIGIN
^^^^^^^^^

``ORIGIN`` value is an interger, has three kinds of value (0, 1, 2 ). it defines the
origin of the path information.  The data octet can assume the following values:

======== ===
Value    Meaning
======== ===
0        IGP
1        EGP
2        INCOMPLETE
======== ===

2. AS_PATH
^^^^^^^^^^

``AS_PATH`` value is a list, it has one item at least, each item also is a list and it reprensents
one ``AS PATH`` segment,like [[sgement_1], [segment_2], ......], and each AS path segment is represented
by [path segment type,  path segment value]. For path sgement value, its a list of interger.

each segment's first item is segment type, it has four kinds of vlaue.

====== ===
Value  Meaning
====== ===
1      AS_SET: unordered set of ASes a route in the UPDATE message has traversed
2      AS_SEQUENCE: ordered set of ASes a route in the UPDATE message has traversed
====== ===

For example:

.. code-block:: json

    {
        "attr": {
            "2": [[2, [209, 2768, 2768, 2768, 2768]]]
        }
    }

For this example, it only has one AS path segment: ``[2, [209, 2768, 2768, 2768, 2768]]``,
this segment's type is ``AS_SEQUENCE``, and its value is ``[209, 2768, 2768, 2768, 2768]``.

3. NEXT_HOP
^^^^^^^^^^^

``NEXT_HOP`` is one a string, IPv4 address format, eg: '10.0.0.1'.

4. MULTI_EXIT_DISC
^^^^^^^^^^^^^^^^^^

``MULTI_EXIT_DISC`` is an interger.

5. LOCAL_PREF
^^^^^^^^^^^^^

``LOCAL_PREF`` is an interger.

6. ATOMIC_AGGREGATE
^^^^^^^^^^^^^^^^^^^

``ATOMIC_AGGREGATE`` is one empty string, ``""``.

7. AGGREGATOR
^^^^^^^^^^^^^

``AGGREGATOR`` is a list, it has two items, [asn, aggregator], the first is AS number, the second is IP address.
eg:

.. code-block:: json

    {
        "attr": {
            "7": [100, "1.1.1.1"]
        }
    }

8. COMMUNITY
^^^^^^^^^^^^

``COMMUNITY`` is a list, each item of this List is a string.

eg:

.. code-block:: json

    {
        "attr": {
            "8": ["NO_EXPORT", "1234:5678"]
        }
    }

There are two kinds of ``COMMUNITY``, first is "Well-Konwn", second is "The Others".

"Well-known" COMMUNITY

.. code-block:: python
    :emphasize-lines: 3,5

    planned_shut               = 0xFFFF0000
    accept_own                 = 0xFFFF0001
    ROUTE_FILTER_TRANSLATED_v4 = 0xFFFF0002
    ROUTE_FILTER_v4            = 0xFFFF0003
    ROUTE_FILTER_TRANSLATED_v6 = 0xFFFF0004
    ROUTE_FILTER_v6            = 0xFFFF0005
    NO_EXPORT                  = 0xFFFFFF01
    NO_ADVERTISE               = 0xFFFFFF02
    NO_EXPORT_SUBCONFED        = 0xFFFFFF03
    NOPEER                     = 0xFFFFFF04

9. ORIGINATOR_ID
^^^^^^^^^^^^^^^^

``ORIGINATOR_ID`` is a string, format as IPv4 address, just ``NEXT_HOP`` eg: "10.0.0.1".

10. CLUSTER_LIST
^^^^^^^^^^^^^^^^

``CLUSTER_LIST`` is a list, each item in this List is a string, format as IPv4 address.
eg:

.. code-block:: json

    {
        "attr": {
            "10": ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        }
    }

11. MP_REACH_NLRI
^^^^^^^^^^^^^^^^^

.. note::

    Only No IPv4 Unicast BGP Update messages have the attributes ``MP_REACH_NLRI`` and ``MP_UNREACH_NLRI``, because
    for IPv4 Unicast, its NLRI and WITHDRAW informations are contain in ``nlri`` and ``withdraw`` value. So for No
    IPv4 Unicast BGP messages, its ``nlri`` and ``withdraw`` are empty, and its own nlri and withdraw information
    contains in ``MP_REACH_NLRI`` and ``MP_UNREACH_NLRI``.

``MP_REACH_NLRI`` is one complex dict which has three key ``afi_safi``, ``next_hop``, ``nlri``.
and according to differences between the ``afi_safi``, the Data structure of ``next_hop`` and ``nlri`` are different.

``afi_safi`` value and meanings, reference by `Address Family Numbers <http://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml>`_ and
`Subsequent Address Family Identifiers (SAFI) Parameters <http://www.iana.org/assignments/safi-namespace/safi-namespace.xhtml>`_

In addition to IPv4 Unicast, here are the ``afi_safi`` we support:

========= ===
Value     Meaning
========= ===
[1, 128]  IPv4 MPLSVPN
[1, 133]  IPv4 Flowspec
[1, 73]   IPv4 Sr-policy
[2, 1]    IPv6 Unicast
[2, 128]  IPv6 MPLSVPN
[25, 70]  L2VPN EVPN
...       ...
========= ===

IPv4 MPLSVPN
""""""""""""

.. code-block:: json

    {
        "attr":{
            "14": {
                "afi_safi": [1, 128],
                "nexthop": {"rd": "0:0", "str": "2.2.2.2"},
                "nlri": [
                    {
                        "label": [25],
                        "rd": "100:100",
                        "prefix": "11.11.11.11/32"}]}
            }
    }

IPv4 FlowSpec
"""""""""""""

.. code-block:: json

    {
        "attr":{
            "14": {
                "afi_safi": [1, 133],
                "nexthop": "",
                "nlri": [
                    {"1": "192.88.2.3/24", "2": "192.89.1.3/24", "5": "=80|=8080"},
                    {"1": "192.88.5.3/24", "2": "192.89.2.3/24", "5": "=80|=8080"}
                ]
            }
        }
    }

The nlri contains filters and values, and the supported filters are:

.. code-block:: python

    BGPNLRI_FSPEC_DST_PFIX = 1  # RFC 5575
    BGPNLRI_FSPEC_SRC_PFIX = 2  # RFC 5575
    BGPNLRI_FSPEC_IP_PROTO = 3  # RFC 5575
    BGPNLRI_FSPEC_PORT = 4  # RFC 5575
    BGPNLRI_FSPEC_DST_PORT = 5  # RFC 5575
    BGPNLRI_FSPEC_SRC_PORT = 6  # RFC 5575
    BGPNLRI_FSPEC_ICMP_TP = 7  # RFC 5575
    BGPNLRI_FSPEC_ICMP_CD = 8  # RFC 5575
    BGPNLRI_FSPEC_TCP_FLAGS = 9  # RFC 5575
    BGPNLRI_FSPEC_PCK_LEN = 10  # RFC 5575
    BGPNLRI_FSPEC_DSCP = 11  # RFC 5575
    BGPNLRI_FSPEC_FRAGMENT = 12  # RFC 5575

The value format of each filter are: `BGPNLRI_FSPEC_DST_PFIX` and `BGPNLRI_FSPEC_SRC_PFIX` are prefixes format,
others are integers, but in string format like:

`=80` means equal to `80`

`=80|=8080` means equal to 80 or 8080.

`>=80|<40` means geater than 80 or equal to 80 or less than 40

IPv4 Sr-policy
""""""""""""""

.. code-block:: json

    {
        "attr": {
            "8": ["NO_ADVERTISE"],
            "14": {
                "afi_safi": [1, 73],
                "nexthop": "192.168.5.5",
                "nlri": {
                    "distinguisher": 0,
                    "color": 10,
                    "endpoint": "192.168.76.1"
                }
            },
            "16": ["route-target:10.75.195.199:00"],
            "23": {
                "0": "new",
                "12": 100,
                "13": 25102,
                "128": [
                    {
                        "9": 10,
                        "1": [
                            {
                                "1": {
                                    "label": 2000,
                                    "TC": 0,
                                    "S": 0,
                                    "TTL": 255
                                }
                            },
                            {
                                "3": {
                                    "node": "10.1.1.1",
                                    "SID": {
                                        "label": 3000,
                                        "TC": 0,
                                        "S": 0,
                                        "TTL": 255
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }

attribute explaination(only for this format):
::

    "8": Optionally assign
    "14": Multiprotocol Reacable Attribute
    "16": Route Target Extended Community
    "23": Tunnel Encapsulation Attribute
        "0": if the ios version lower than 6.4.1.14(Cisco facility), the value should be 'old', and in the meantime,
             the key of Preference should be '6', key of Binding SID should be '7', else it should be 'new' and key
             of Preference and Binding SID should be '12' and '13'
        "6"/"12": Preference
        "7"/"13": Binding SID
        "128": Multiple segement lists
            "9": Weighted
            "1": Segement list
                "1": Segement type 1
                    "label": Value of MPLS Label
                    "TC": Assign optionally, default value is 0
                    "S": Assign optionally, default value is 0
                    "TTL": Assign optionally, default value is 255
                "3": Segement type 3
                    "node": An Ipv4 Address
                    "SID": Assign Optionally, inner structure similar to Segement type 1

IPv6 Unicast
""""""""""""

For IPv6 Unicast, it has three or four keys:

.. code-block:: json

    {
        "attr":{
            "14": {
                "afi_safi": [2, 1],
                "linklocal_nexthop": "fe80::c002:bff:fe7e:0",
                "nexthop": "2001:db8::2",
                "nlri": ["::2001:db8:2:2/64", "::2001:db8:2:1/64", "::2001:db8:2:0/64"]}
        }
    }

The value of the Length of Next Hop Network Address field on a ``MP_REACH_NLRI`` attribute shall be set to 16,
when only a global address is present, or 32 if a link-local address is also included in the Next Hop field.

IPv6 MPLSVPN
""""""""""""

.. code-block:: json

    {
        "attr":{
            "14": {
                "afi_safi": [2, 128],
                "nexthop": {"rd": "100:12", "str": "::ffff:172.16.4.12"},
                "nlri": [
                    {
                        "label": [54],
                        "rd": "100:12",
                        "prefix": "2010:0:12:4::/64"},
                    {
                        "label": [55],
                        "rd": "100:12",
                        "prefix": "2010:1:12::/64"
                    }
                ]
            },
            "16": ["route-target:100:12"]
            }
    }

EVPN
""""

.. code-block:: json

    {
        "attr": {
            "1": 0,
            "2": [],
            "5": 100,
            "14": {
                "afi_safi": [25, 70],
                "nexthop": "10.75.44.254",
                "nlri": [
                    {
                        "type": 2,
                        "value": {
                            "eth_tag_id": 108,
                            "ip": "11.11.11.1",
                            "label": [0],
                            "rd": "172.17.0.3:2",
                            "mac": "00-11-22-33-44-55",
                            "esi": 0}}]
            }
        }
    }


12. MP_UNREACH_NLRI
^^^^^^^^^^^^^^^^^^^

The difference between ``MP_REACH_NLRI`` and ``MP_UNREACH_NLRI`` is that ``MP_UNREACH_NLRI`` only has two keys,
``afi_safi`` and ``withdraw``, and there structure is the same.

IPv4 MPLSVPN
""""""""""""

.. code-block:: json

    {
        "attr":{
            "15": {
                "afi_safi": [1, 128],
                "withdraw": [
                    {
                        "rd": "100:100",
                        "prefix": "11.11.11.11/32"}]}
            }
    }

IPv4 FlowSpec
"""""""""""""

.. code-block:: json

    {
        "attr":{
            "15": {
                "afi_safi": [1, 133],
                "withdraw": [
                    {"1": "192.88.2.3/24", "2": "192.89.1.3/24", "5": "=80|=8080"},
                    {"1": "192.16.0.0/8", "6": "=8080"}
                ]
            }
        }
    }

IPv4 Sr-policy
""""""""""""""

.. code-block:: json

    {
        "attr":{
            "15": {
                "afi_safi": [1, 73],
                "withdraw": {
                    "distinguisher": 0,
                    "color": 10,
                    "endpoint": "192.168.76.1"
                }
            }
        }
    }

IPv6 Unicast
""""""""""""

.. code-block:: json

    {
        "attr":
            "15": {
                "afi_safi": [2, 1],
                "withdraw": ["::2001:db8:2:2/64", "::2001:db8:2:1/64", "::2001:db8:2:0/64"]}
    }

IPv6 MPLSVPN
""""""""""""

.. code-block:: json

    {
        "attr":{
            "15": {
                "afi_safi": [2, 128],
                "withdraw": [
                    {
                        "label": [54],
                        "rd": "100:12",
                        "prefix": "2010:0:12:4::/64"},
                    {
                        "label": [55],
                        "rd": "100:12",
                        "prefix": "2010:1:12::/64"
                    }
                ]}
    }}

EVPN
""""

.. code-block:: json

    {
        "attr": {
            "15": {
                "afi_safi": [25, 70],
                "withdraw": [
                    {
                        "type": 2,
                        "value": {
                            "eth_tag_id": 108,
                            "ip": "11.11.11.1",
                            "label": [0],
                            "rd": "172.17.0.3:2",
                            "mac": "00-11-22-33-44-55",
                            "esi": 0}}]
            }
        }
    }

13. EXTENDED_COMMUNITY
^^^^^^^^^^^^^^^^^^^^^^

Extended community we supported:

.. code-block:: Python

    #  VPN Route Target  #
    route-target  # Route Target

    # Route Origin (SOO site of Origin)
    route-origin  # Route Origin

    # BGP Flow Spec
    redirect-nexthop  # redirect to ipv4/v6 nexthop
    traffic-rate  # traffic-rate
    redirect-vrf  # redirect Route Target
    traffic-marking-dscp  # traffic-marking DSCP value

    # Transitive Opaque
    color # Color, treated like color-00, leftmost 2 bits of reserved field = 00, CO bits = 00
    # Color, leftmost 2 bits of reserved field = 00, CO bits = 00
    # srpolicy -> IGP
    color-00
    # Color, leftmost 2 bits of reserved field = 01, CO bits = 01
    # srpolicy -> same afi null endpoint -> any null endpoint -> IGP
    color-01
    # Color, leftmost 2 bits of reserved field = 10, CO bits = 10
    # srpolicy -> same afi null endpoint -> any null endpoint -> same afi endpoint -> any endpoint -> IGP
    color-10
    # Color, leftmost 2 bits of reserved field = 11, CO bits = 11
    # treated like color-00
    color-11
    encapsulation  # encapsulation

    # BGP EVPN
    mac-mobility  # Mac Mobility
    esi-label  # ESI MPLS Label
    es-import  # ES Import
    router-mac  # EVPN Router MAC


14. AS4_PATH
^^^^^^^^^^^^

4 bytes AS PATH same as ``AS_PATH``.

15. AS4_AGGREGATOR
^^^^^^^^^^^^^^^^^^

4 bytes AS same as ``AGGREGATOR``.

16. PMSI_TUNNEL
^^^^^^^^^^^^^^^

"P-Multicast Service Interface Tunnel (PMSI Tunnel) attribute".  This is an optional transitive BGP attribute.  The format of this attribute is defined as follows:

.. code-block:: json

    {
        "mpsl_label": 625,
        "tunnel_id": "4.4.4.4",
        "tunnel_type": 6,
        "leaf_info_required": 0
    }

Notification Message
--------------------

BGP notification message is type 3.

.. code-block:: json

    {
        "t": 1452236692.201259,
        "seq": 28,
        "type": 3,
        "msg": {
            "data": "'\\x03\\xe8'",
            "sub_error": "Bad Peer AS",
            "error": "OPEN Message Error"
        }
    }

Keepalive Message
-----------------

BGP Keepalive message type is 4.
Example:

.. code-block:: json

    {
        "t": 1372065358.666234,
        "seq": 11,
        "type": 4,
        "msg": null
    }

Route Refresh Message
---------------------

Route refresh message content is (AFI, SAFI).

.. code-block:: json

    {
        "t": 1452237198.880322,
        "seq": 10,
        "type": 5,
        "msg": {
            "res": 0,
            "afi": 1,
            "safi": 1
        }
    }


Cisco Route Refresh Message
---------------------------

.. code-block:: json

    {
        "t": 1452237198.880322,
        "seq": 10,
        "type": 128,
        "msg": {
            "res": 0,
            "afi": 1,
            "safi": 1
        }
    }


Malformed Update Message
------------------------

If the BGP update message's encoding is wrong and some part of it can't be decoded,
then it will write this message as malformed update message, for example:

.. code-block:: json

    {
        "t": 1452237406.457384,
        "seq": 21,
        "type": 6,
        "msg":{
            "attr": null,
            "nlri": ["200.0.0.0/24", "201.0.0.0/24"],
            "withdraw": [],
            "hex": "hex": "'\\x00\\x00\\x00*@\\x01\\x01\\x00@\\x02\\x0e\\x02\\x03\\x00\\"
        }
    }

