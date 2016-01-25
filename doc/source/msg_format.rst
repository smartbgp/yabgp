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
---------------

BGP Update message (type = 2), the value of ``msg`` for a update message is a dict, and it
has three keys : ``attr``, ``nlri``, ``withdraw``.

=========== ========   ==============
Key         Value      Description
=========== ========   ==============
"attr"      dict       Path Attributes
"nlri"      list       Network Layer Reachability Information
"withdraw"  list       Withdrawn Routes
=========== ========   ==============

simple format:

.. code-block:: json

    {
        "msg":{
            "attr": {},
            "withdraw": [],
            "nlri": []
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
            "withdraw": []
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

ORIGIN
^^^^^^^

``ORIGIN`` value is an interger, has three kinds of value (0, 1, 2 ). it defines the
origin of the path information.  The data octet can assume the following values:

======== ===
Value    Meaning
======== ===
0        IGP
1        EGP
2        INCOMPLETE
======== ===

AS_PATH
^^^^^^^

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

NEXT_HOP
^^^^^^^^

``NEXT_HOP`` is one a string, IPv4 address format, eg: '10.0.0.1'.

MULTI_EXIT_DISC
^^^^^^^^^^^^^^^

``MULTI_EXIT_DISC`` is an interger.

LOCAL_PREF
^^^^^^^^^^

``LOCAL_PREF`` is an interger.

ATOMIC_AGGREGATE
^^^^^^^^^^^^^^^^

``ATOMIC_AGGREGATE`` is one empty string, ``""``.

AGGREGATOR
^^^^^^^^^^

``AGGREGATOR`` is a list, it has two items, [asn, aggregator], the first is AS number, the second is IP address.
eg:

.. code-block:: json

    {
        "attr": {
            "7": [100, "1.1.1.1"]
        }
    }

COMMUNITY
^^^^^^^^^

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

ORIGINATOR_ID
^^^^^^^^^^^^^^

``ORIGINATOR_ID`` is a string, format as IPv4 address, just ``NEXT_HOP`` eg: "10.0.0.1".

CLUSTER_LIST
^^^^^^^^^^^^

``CLUSTER_LIST`` is a list, each item in this List is a string, format as IPv4 address.
eg:

.. code-block:: json

    {
        "attr": {
            "10": ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        }
    }

MP_REACH_NLRI
^^^^^^^^^^^^^^

.. note::

    Only No IPv4 Unicast BGP Update messages have the attributes ``MP_REACH_NLRI`` and ``MP_UNREACH_NLRI``, because
    for IPv4 Unicast, its NLRI and WITHDRAW informations are contain in ``nlri`` and ``withdraw`` value. So for No
    IPv4 Unicast BGP messages, its ``nlri`` and ``withdraw`` are empty, and its own nlri and withdraw information
    contains in ``MP_REACH_NLRI`` and ``MP_UNREACH_NLRI``.

``MP_REACH_NLRI`` is one complex dict which has three key ``afi_safi``, ``next_hop``, ``nlri``.
and according to differences between the ``afi_safi``, the Data structure of ``next_hop`` and ``nlri`` are different.

``afi_safi`` value and meanings, reference by `Address Family Numbers <http://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml>`_ and
`Subsequent Address Family Identifiers (SAFI) Parameters <http://www.iana.org/assignments/safi-namespace/safi-namespace.xhtml>`_

In addition to IPv4 Unicast, Now we support IPv6 Unicast and IPv4 Flowspec, here are the ``afi_safi`` value example:

========= ===
Value     Meaning
========= ===
[1, 128]  IPv4 MPLSVPN
[1, 133]  IPv4 Flowspec
[2, 1]    IPv6 Unicast
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
        "attr":
            "14": {
                "afi_safi": [2, 1],
                "linklocal_nexthop": "fe80::c002:bff:fe7e:0",
                "nexthop": "2001:db8::2",
                "nlri": ["::2001:db8:2:2/64", "::2001:db8:2:1/64", "::2001:db8:2:0/64"]}
    }

The value of the Length of Next Hop Network Address field on a ``MP_REACH_NLRI`` attribute shall be set to 16,
when only a global address is present, or 32 if a link-local address is also included in the Next Hop field.

MP_UNREACH_NLRI
^^^^^^^^^^^^^^^

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
----------------------

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
----------------------------

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
-------------------------

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

