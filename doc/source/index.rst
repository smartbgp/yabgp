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


Table of Contents
=================

.. toctree::
   :maxdepth: 2

   feature
   install
   tutorial
   msg_format
   restapi
   tools
   reference

Support
=======

There are many jobs need to do in future.
We are working hardly on that. So any of your ideas is welcome.

Please use GitHub issue system or submit pull request.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
