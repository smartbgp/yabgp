.. yabgp documentation master file, created by
   sphinx-quickstart on Fri May 15 10:18:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

YABGP Project
=============

YABGP is a yet another Python implementation for BGP Protocol. It can be used to establish BGP connections with all kinds
of routers (include real Cisco/HuaWei/Juniper routers and some router
simulators like GNS3) and receive/parse BGP messages for
future analysis.

Support sending BGP messages(route refresh/update) to the peer through RESTful API. YABGP can't send any BGP update messages
by itself, it's just a agent, so there can be many agents and they can be controlled by a contoller.

We write it in strict accordance with the specifications of RFCs.

This software can be used on Linux/Unix, Mac OS and Windows systems.

Features
========

-  It can establish BGP session based on IPv4 address (TCP Layer) in
   active mode(as TCP client);

-  Support TCP MD5 authentication(IPv4 and does not support Windows
   now);

-  BGP capabilities support: 4 Bytes ASN, Route Refresh(Cisco Route Refresh), Add Path send/receive;

-  Address family support: IPv4 unicast, IPv6 unicast, IPv4 Flowspec(limited), IPv4 VPNv4;

-  Decode all BGP messages to human readable strings and write files to
   disk(configurable);

-  Support basic RESTFUL API for getting running information and sending BGP messages.

.. note::

  yabgp is a light weight BGP agent used for connecting network devices. It only can be
  TCP client in one BGP peering connection and can't send any update messages by itself(send through REST API).
  We recommend that each yabgp process connect only one BGP neighbor, so each process is independent with each other,
  we can start many yabgp processes within the same machine or in different machines. There can be a central controller
  which can controll all yabgp processes through REST API to send BGP update messages.

Application
===========

There are many jobs need to do in future.

We are working hardly on that. So any of your ideas is welcome.

Quickstarts
===========

.. toctree::
   :maxdepth: 2

   install
   tutorial
   msg_format
   restapi
   tools
   reference

Support
=======

Please use GitHub issue system or submit pull request.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
