.. yabgp documentation master file, created by
   sphinx-quickstart on Fri May 15 10:18:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

YABGP Project
=============

YABGP is a yet another Python implementation for BGP Protocol. It can be used to establish BGP connections with all kinds
of routers (include real Cisco/HuaWei/Juniper routers and some router
simulators like Cisco's IOL/IOU, Junipers' JUOS, and GNS3) and receive/parse BGP messages for
future analysis. Now we open sourced it.

We write it accordance with the specifications of RFCs.

This software can be used on Linux/Unix, Mac OS and Windows systems.

Features
========

-  It can establish BGP session based on IPv4 address (TCP Layer) in
   active mode(as TCP client);

-  Support TCP MD5 authentication(IPv4 and does not support Windows
   now);

-  BGP capabilities support: 4 Bytes ASN, IPv4 address family, Route
   Refresh(Cisco Route Refresh);

-  Decode all BGP messages to human readable strings and write files to
   disk(configurable);

-  Support basic RESTFUL API.

.. note::

  yabgp is a light weight BGP agent used for connecting network devices. It only can be
  TCP client in one BGP peering connection, and we recommend that each yabgp process connect
  only one BGP neighbor, so each process is independent with each other, we can start many yabgp
  processes within the same machine or in different machines.

Application
===========

There are many jobs need to do in future.

We are working hardly on that. So any of your ideas is welcome.

Quickstarts
===========

.. toctree::
   :maxdepth: 1

   install
   tutorial
   msg_format
   restapi
   reference

Support
=======

Please use GitHub issue system or submit pull request.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
