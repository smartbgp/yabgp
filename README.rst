YABGP
=====

|Join Chat| |License| |Build Status| |Code Climate| |Code Health| |Documentation Status| |Test Coverage|

What is yabgp?
~~~~~~~~~~~~~~

YABGP is a yet another Python implementation for BGP Protocol. It was born in
Cisco around 2011, we use it to establish BGP connections with all kinds
of routers (include real Cisco/HuaWei/Juniper routers and some router
simulators in Cisco like IOL/IOU) and receive/parse BGP messages for
future analysis. Now we open sourced it.

We write it in strict accordance with the specifications of RFCs.

This software can be used on Linux/Unix, Mac OS and Windows systems.

Features
~~~~~~~~

-  It can establish BGP session based on IPv4 address (TCP Layer) in
   active mode(as TCP client);

-  Support TCP MD5 authentication(IPv4 and does not support Windows
   now);

-  BGP capabilities support: 4 Bytes ASN, IPv4 address family, Route
   Refresh(Cisco Route Refresh);

-  Decode all BGP messages to human readable strings and write files to
   disk(configurable);

Quick Start
~~~~~~~~~~~

We recommend run ``yabgp`` through python virtual-env from source
code or pip install

Use yabgp from source code:

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ git clone https://github.com/smartbgp/yabgp
    $ cd yabgp
    $ pip install -r requirements.txt
    $ cd bin
    $ python yabgpd -h

Use pip install

.. code:: bash

    $ virtualenv yabgp-virl
    $ source yabgp-virl/bin/activate
    $ pip install yabgp
    $ which yabgpd
    /home/bgpmon/yabgp-virl/bin/yabgpd
    $ yabgpd -h

For example:

.. code:: bash

    $ yabgpd --bgp-local_addr=1.1.1.1 --bgp-local_as=65001 --bgp-remote_addr=1.1.1.2 --bgp-remote_as=65001 --bgp-md5=test --config-file=../etc/yabgp/yabgp.ini

BGP message example:

in ``yabgp.ini``, you can point out if you want to store the parsing
BGP message to local disk and where you want to put them in.

::

    [message]
    # how to process parsed BGP message?

    # Whether the BGP message is written to disk
    # write_disk = True

    # the BGP messages storage path
    # write_dir = /home/bgpmon/data/bgp/
    write_dir = ./
    # The Max size of one BGP message file, the unit is MB
    # write_msg_max_size = 500

::

    $ more 1429257741.41.msg 
    [1429258235.343657, 1, 1, {'bgpID': '192.168.45.1', 'Version': 4, 'holdTime': 180, 'ASN': 23650, 'Capabilities': {'GracefulRestart': False, 'ciscoMultiSession': False, 'ciscoRouteRefresh': True, '4byteAS': True, 'AFI_SAFI': [(1, 1)],
 '7
    0': '', 'routeRefresh': True}}, (0, 0)]
    [1429258235.346803, 2, 4, None, (0, 0)]
    [1429258235.349598, 3, 4, None, (0, 0)]
    [1429258235.349837, 4, 2, {'ATTR': {1: 0, 2: [(2, [64639, 64660])], 3: '192.168.24.1', 4: 0, 5: 100}, 'WITHDRAW': [], 'NLRI': ['192.168.1.0/24']}, (1, 1)]

The structure of each line is:

::

    [timestamp, sequence number, message type, message content, address family]

For message type:

::

    MSG_OPEN = 1
    MSG_UPDATE = 2
    MSG_NOTIFICATION = 3
    MSG_KEEPALIVE = 4
    MSG_ROUTEREFRESH = 5
    MSG_CISCOROUTEREFRESH = 128

Support
~~~~~~~

Send email to penxiao@cisco.com, or use GitHub issue system.

TODO
~~~~

-  support more address family (IPv6, VPNv4, VPNv6, etc.)
-  support RESTful API, send message/control peer state, etc.
-  unittest
-  others

Contribute
~~~~~~~~~~

Please create Github Pull Request https://github.com/smartbgp/yabgp/pulls

More details please read HACKING.rst.

Thanks
~~~~~~

For core files like fsm, protocol, we copy some of the code from
https://github.com/wikimedia/PyBal/blob/master/pybal/bgp.py,

and message parsing, we reference from
https://github.com/Exa-Networks/exabgp

.. |License| image:: https://img.shields.io/hexpm/l/plug.svg
   :target: https://github.com/smartbgp/yabgp/blob/master/LICENSE
.. |Build Status| image:: https://travis-ci.org/smartbgp/yabgp.svg?branch=master
   :target: https://travis-ci.org/smartbgp/yabgp
.. |Code Climate| image:: https://codeclimate.com/github/smartbgp/yabgp/badges/gpa.svg
   :target: https://codeclimate.com/github/smartbgp/yabgp

.. |Join Chat| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/smartbgp/yabgp?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |Code Health| image:: https://landscape.io/github/smartbgp/yabgp/master/landscape.svg?style=flat
   :target: https://landscape.io/github/smartbgp/yabgp/master

.. |Documentation Status| image:: https://readthedocs.org/projects/yabgp/badge/?version=latest
   :target: https://readthedocs.org/projects/yabgp/?badge=latest

.. |Test Coverage| image:: https://coveralls.io/repos/smartbgp/yabgp/badge.svg?branch=master 
   :target: https://coveralls.io/r/smartbgp/yabgp
