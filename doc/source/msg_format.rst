Message Format
==============

BGP messsage structure
----------------------

BGP message is a **Python List**, and it contains more than three parts.

[ **timestamp**, **sequence number**, **type**, **other information** (at least one )]

**timestamp** It is a standard unix time stamp, the number of seconds since 00:00:00 UTC on January 1, 1970.

Example:

.. code-block:: python
    :emphasize-lines: 3,5

    timestamp = 1372051151.2572551 # that is Mon Jun 24 13:19:11 2013.

**sequence number**  It is a interger and represents the message number.

**type** It is a interger and represents the message type.

there are eight types of message now.

Type = 0  ( session information, TCP Connection information)

Type = 1  ( open message )

Type = 2  ( update message )

Type = 3  ( notification message )

Type = 4  (keepalive message)

Type = 5  ( route refresh message)

Type = 128 ( cisco route refresh message)

Type = 6  (Malformed update message )

- **1. type = 0**

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 0, session information]
    # Example
    [1372065358.666234, 141353378, 0, 'Connection lost:Connection to the other side was lost in a non-clean fashion: Connection lost.']

- **2. type = 1**

.. code-block:: python
    :emphasize-lines: 3,5

    [ timestamp, sequence number, type, decoded_message]
    # message example
    [1371604039.783044,
     1,
     1,
     {'ASN': 100,
      'Capabilities': {'4byteAS': True,
                       'AFI_SAFI': [(1, 1)],
                       'GracefulRestart': False,
                       'ciscoMultiSession': False,
                       'ciscoRouteRefresh': True,
                       'routeRefresh': True},
      'Version': 4,
      'bgpID': '1.1.1.1',
      'holdTime': 180}]

- **3. type = 2**

.. code-block:: python
    :emphasize-lines: 3,5

    [ timestamp, sequence number, type, decoded_message]

Decoded message is a Python dictionary

.. code-block:: python
    :emphasize-lines: 3,5

    {
        'attr': {},
        'withdraw': [],
        'nlri': []
    }

The decoded message dictionary has three keys, **attr**, **withdraw**, **nlri**.

The value of key **attr** is a Python dictionary. it contains the BGP prefix's attribute, the dict's key represent
what of kind of attribute, and the value is this attribute's value.

The attribute we supported now is: (reference by `IANA <http://www.iana.org/assignments/bgp-parameters/bgp-parameters.xml>`_)

.. code-block:: python
    :emphasize-lines: 3,5

    {
        1: 'ORIGIN',
        2: 'AS_PATH',
        3: 'NEXT_HOP',
        4: 'MULTI_EXIT_DISC',
        5: 'LOCAL_PREF',
        6: 'ATOMIC_AGGREGATE',
        7: 'AGGREGATOR',
        8: 'COMMUNITY',
        9: 'ORIGINATOR_ID',
        10: 'CLUSTER_LIST',
        14: 'MP_REACH_NLRI',
        15: 'MP_UNREACH_NLRI',
        16: 'EXTENDED_COMMUNITY',
        17: 'AS4_PATH',
        18: 'AS4_AGGREGATOR',
        128: 'ATTR_SET'
    }

The **withdraw** and **nlri** are all Python List, they contain the particular prefix. Here is one real BGP decoded message example

.. code-block:: python
    :emphasize-lines: 3,5

    # this is decoded update message
    {'attr': {1: 0,
              2: [(2, [3356, 20485, 12772])],
              3: '219.158.1.203',
              4: 45400,
              8: ['4837:2110', '4837:3356'],
              9: '219.158.1.203',
              10: ['219.158.1.209', '0.0.0.30'],
              '5': 110},
     'nlri': ['46.52.204.0/24',
              '46.52.204.0/23',
              '94.28.54.0/24',
              '79.122.216.0/22',
              '46.52.146.0/23'],
     'withdraw': []}

     # this is decoded withdraw message
     {'attr': {},
      'nlri': [],
      'withdraw': ['46.52.204.0/24',
                  '46.52.204.0/23',
                  '94.28.54.0/24',
                  '79.122.216.0/22',
                  '46.52.146.0/23']}

Next, we will explain the detail structure of each attribute.

.. [1] ORIGIN (key = 1)

**Origin** value is one Python interger, has three kinds of value (0, 1, 2 )

.. code-block:: python
    :emphasize-lines: 3,5

    {
        0: 'IGP',
        1: 'EGP',
        2: 'INCOMPLETE'
    }

.. [2] AS_PATH (key = 2)

**AS_PATH** value is one Python List, it has one item at least, each item is a Python Tuple and it reprensents one **AS PATH** segment.

[(sgement_1), (segment_2), ......] eg. [(2, [3356, 20485, 12772]), (3, [65501,65502])]

each segment's first item is segment type, it has four kinds of vlaue.

.. code-block:: python
    :emphasize-lines: 3,5

    {
        1: 'AS_SET',
        2: 'AS_SEQUENCE',
        3: 'AS_CONFED_SEQUENCE',
        4: 'AS_CONFED_SET'
    }

.. [3] NEXT_HOP (key = 3)

**NEXT_HOP** is one Python string, IPv4 address format, eg: '10.0.0.1'.

.. [4] MULTI_EXIT_DISC (key = 4)

**MULTI_EXIT_DISC** is one Python interger.

.. [5] LOCAL_PREF (key = 5)

**LOCAL_PREF** is one Python interger.

.. [6] ATOMIC_AGGREGATE (key = 6)

**ATOMIC_AGGREGATE** is one empty Python string, "".

.. [7] AGGREGATOR (key = 7)

**AGGREGATOR** is one Python tuple, it has two items, (asn, aggregator), the first the AS number, the second is IP address. eg: (1239, 10.1.1.2).

.. [8] COMMUNITY (key = 8)

**COMMUNITY** is one Python List, each item of this List is Python String.

eg: ['NO_EXPORT', '4837:9929']

There are two kinds of **COMMUNITY**, first is "Well-Konwn", second is "The Others".

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

.. [9] ORIGINATOR_ID (key = 9)

**ORIGINATOR_ID** is one Python string, format as IPv4 address, eg: "0.0.0.1", "10.0.0.1".

.. [10] CLUSTER_LIST (key = 10)

**CLUSTER_LIST** is one Python List, each item in this List is one Python string, format as IPv4
address. eg: ['0.0.0.1', '0.0.0.2', '10.0.0.1'].

.. [14] MP_REACH_NLRI (key = 14)

**MP_REACH_NLRI** is one complex Python dict which has three key **afi_safi**, **next_hop**, **nlri**.
and according to difference between the **afi_safi**, the Data structure of **next_hop** and **nlri** are different.

Here are the details.

**a.** afi_safi=(1, 4)

**b.** afi_safi=(1, 128)

**c.** afi_safi=(2, 1)

**d.** afi_safi=(2, 4)

**e.** afi_safi=(2, 128)

**f.** afi_safi=(1, 133)


.. [15] MP_UNREACH_NLRI (key=15)

The difference between **MP_REACH_NLRI** and **MP_UNREACH_NLRI** is that **MP_UNREACH_NLRI** only has two keys,
**afi_safi** and **withdraw**.

Here are some examples:

**a.** afi_safi=(1, 4)

**b.** afi_safi=(1, 128)

**c.** afi_safi=(2, 1)

**d.** afi_safi=(2, 4)

**e.** afi_safi=(2, 128)

**f.** afi_safi=(1, 133)


Here are some real BGP Update message examples:

.. code-block:: python
    :emphasize-lines: 3,5

    [1372646400.563245, 2, 2, {'attr': {1: 0, 2: [(2, [2914, 45896, 56149])], 3: '10.75.44.224', 4: 37, 5: 500, 9: '219.158.1.153', 10: ['72.163.226.222', '219.158.1.209', '0.0.0.40']}, 'withdraw': [], 'nlri': ['103.3.252.0/22']}, (1, 1)]
    [1372646400.563346, 3, 2, {'attr': {1: 2, 2: [(2, [4766, 9531])], 3: '10.75.44.224', 5: 500, 9: '219.158.1.151', 10: ['72.163.226.222', '219.158.1.209', '0.0.0.30']}, 'withdraw': [], 'nlri': ['210.218.1.0/24', '210.218.2.0/24', '210.218.6.0/24']}, (1, 1)]
    [1372646400.563359, 4, 2, {'attr': {1: 0, 2: [(2, [3356, 20485, 49055])], 3: '10.75.44.224', 4: 45400, 5: 110, 9: '219.158.1.203', 10: ['72.163.226.222', '219.158.1.209', '0.0.0.30']},'withdraw': [], 'nlri': ['31.128.32.0/20', '95.215.208.0/22']}, (1, 1)]
    [1372646400.56337, 5, 2, {'attr': {1: 0, 2: [(2, [3257, 43833])], 3: '10.75.44.224', 4: 0, 5: 500, 9: '219.158.30.2', 10: ['72.163.226.222', '219.158.1.209', '0.0.0.30']}, 'withdraw':[], 'NLRI': ['89.29.203.0/24']}, (1, 1)]
    [1372646400.563379, 6, 2, {'attr': {1: 0, 2: [(2, [3257, 22773, 22073])], 3: '10.75.44.224', 4: 500, 5: 500, 9: '219.158.1.240', 10: ['72.163.226.222', '219.158.1.209', '0.0.0.30']}, 'withdraw': [], 'nlri': ['208.48.8.0/24']}, (1, 1)]

- **3. type = 3**

type = 3 is BGP notification message.

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 3, BGP notification message]
    # Example
    [1372065358.666234, 141353378, 3, {'Error': 'ERR_MSG_OPEN', 'Suberror': 'ERR_MSG_OPEN_BAD_PEER_AS', 'Error data':'\x01\xa2\x23\x03'}]

- **4. type = 4**

type = 4 is BGP keepalive message.

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 4, BGP keepalive message]
    # Example
    [1372065358.666234, 141353378, 4, None]

- **5. type = 5**

type = 5 is BGP route refresh message.

route refresh message content is (AFI, SAFI).

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 5, BGP route refresh message]
    # Example
    [1372065358.666234, 141353378, 5, (1, 2)]


- **6. type = 6**

type = 6 is Malformed update message.

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 6, BGP raw hex message, afi_safi]
    # Example
    [1372065358.666234, 141353378, 6, '\x0a\x03\xdf\x03\x04\x02\x23\x45\x5d', (1, 1)]

- **7. type = 128**

cisco route refresh message. just like type = 5

.. code-block:: python
    :emphasize-lines: 3,5

    [timestamp, sequence number, type = 128, Cisco route refresh message]
    # Example
    [1372065358.666234, 141353378, 128, (1, 2)]
