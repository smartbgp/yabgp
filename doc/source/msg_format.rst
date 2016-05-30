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
[2, 1]    IPv6 Unicast
[2, 128]  IPv6 MPLSVPN
[25, 70]  EVPN
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
                "nlri": [{"1": "192.88.2.3/24", "2": "192.89.1.3/24"}]
            }
        }
    }

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
            "16": [[2, "100:12"]]
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
                "withdraw": [{"1": "192.88.2.3/24", "2": "192.89.1.3/24"}]
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
    BGP_EXT_COM_RT_0 = 0x0002  # Route Target,Format AS(2bytes):AN(4bytes)
    BGP_EXT_COM_RT_1 = 0x0102  # Route Target,Format IPv4 address(4bytes):AN(2bytes)
    BGP_EXT_COM_RT_2 = 0x0202  # Route Target,Format AS(4bytes):AN(2bytes)

    # Route Origin (SOO site of Origin)
    BGP_EXT_COM_RO_0 = 0x0003  # Route Origin,Format AS(2bytes):AN(4bytes)
    BGP_EXT_COM_RO_1 = 0x0103  # Route Origin,Format IP address:AN(2bytes)
    BGP_EXT_COM_RO_2 = 0x0203  # Route Origin,Format AS(2bytes):AN(4bytes)

    # BGP Flow Spec
    BGP_EXT_REDIRECT_NH = 0x0800  # redirect to ipv4/v6 nexthop
    BGP_EXT_TRA_RATE = 0x8006  # traffic-rate 2-byte as#, 4-byte float
    BGP_EXT_TRA_ACTION = 0x8007  # traffic-action bitmask
    BGP_EXT_REDIRECT_VRF = 0x8008  # redirect 6-byte Route Target
    BGP_EXT_TRA_MARK = 0x8009  # traffic-marking DSCP value

    # Transitive Opaque
    BGP_EXT_COM_OSPF_ROUTE_TYPE = 0x0306  # OSPF Route Type
    BGP_EXT_COM_COLOR = 0x030b  # Color
    BGP_EXT_COM_ENCAP = 0x030c  # BGP_EXT_COM_ENCAP = 0x030c
    BGP_EXT_COM_DEFAULT_GATEWAY = 0x030d  # Default Gateway

    # BGP EVPN
    BGP_EXT_COM_EVPN_MAC_MOBIL = 0x0600  # Mac Mobility
    BGP_EXT_COM_EVPN_ESI_MPLS_LABEL = 0x0601  # ESI MPLS Label
    BGP_EXT_COM_EVPN_ES_IMPORT = 0x0602  # ES Import
    BGP_EXT_COM_EVPN_ROUTE_MAC = 0x0603  # EVPN Router MAC Extended Community

    # BGP cost cummunity
    BGP_EXT_COM_COST = 0x4301

    # BGP link bandwith
    BGP_EXT_COM_LINK_BW = 0x4004



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

