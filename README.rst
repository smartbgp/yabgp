简体中文_

.. _简体中文: README-zh.rst

YABGP
=====

|License| |Version| |CI| |Documentation Status|


What is yabgp?
~~~~~~~~~~~~~~

YABGP is a yet another Python implementation for BGP Protocol. It can be used to establish BGP connections with all kinds
of routers (include real Cisco/HuaWei/Juniper routers and some router
simulators like GNS3) and receive/parse BGP messages for
future analysis.

Support sending BGP messages(route refresh/update) to the peer through RESTful API. YABGP can't send any BGP update messages
by itself, it's just a agent, so there can be many agents and they can be controlled by a controller.

We write it in strict accordance with the specifications of RFCs.

This software can be used on Linux/Unix, Mac OS and Windows systems. Python >= 3.13 required.
TCP MD5 authentication is only supported on Linux.

Features
~~~~~~~~

-  It can establish BGP session based on IPv4 address (TCP Layer) in
   active mode(as TCP client);

-  Support TCP MD5 authentication(IPv4 only);

-  BGP capabilities support: 4 Bytes ASN, Route Refresh(Cisco Route Refresh), Add Path send/receive;

-  Address family support:

   - IPv4/IPv6 unicast

   - IPv4/IPv6 Labeled Unicast

   - IPv4 Flowspec(limited)

   - IPv4 SR Policy(draft-previdi-idr-segment-routing-te-policy-07)

   - IPv4/IPv6 MPLSVPN

   - EVPN (partially supported)

-  Decode all BGP messages to json format and write them into files in local disk(configurable);

-  Support basic RESTFUL API for getting running information and sending BGP messages.

Quick Start
~~~~~~~~~~~

**Using uv (recommended):**

.. code:: bash

    $ git clone https://github.com/smartbgp/yabgp
    $ cd yabgp
    $ uv sync
    $ uv run yabgpd -h

**Using pip:**

.. code:: bash

    $ pip install yabgp
    $ yabgpd -h

**Using Docker:**

.. code:: bash

    $ docker run -it smartbgp/yabgp:latest --bgp-afi_safi=ipv4 --bgp-local_as=65022 --bgp-remote_addr=10.75.44.219 --bgp-remote_as=65022

**Example:**

.. code:: bash

    $ yabgpd --bgp-local_addr=1.1.1.1 --bgp-local_as=65001 --bgp-remote_addr=1.1.1.2 --bgp-remote_as=65001 --bgp-afi_safi=ipv4

Documentation
~~~~~~~~~~~~~

More information please see the documentation http://yabgp.readthedocs.org

Related Projects
~~~~~~~~~~~~~~~~

Routewatch brings automated alerting to YABGP. https://github.com/nerdalize/routewatch

A BGP update generator based on YaBGP https://github.com/trungdtbk/bgp-update-gen

Support
~~~~~~~

Send email to xiaoquwl@gmail.com, or use GitHub issue system.


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

.. |License| image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: https://github.com/smartbgp/yabgp/blob/master/LICENSE

.. |CI| image:: https://github.com/smartbgp/yabgp/actions/workflows/ci.yml/badge.svg?branch=master
   :target: https://github.com/smartbgp/yabgp/actions/workflows/ci.yml

.. |Documentation Status| image:: https://readthedocs.org/projects/yabgp/badge/?version=latest
   :target: https://readthedocs.org/projects/yabgp/?badge=latest

.. |Version| image:: https://img.shields.io/pypi/v/yabgp.svg
   :target: https://pypi.org/project/yabgp/
