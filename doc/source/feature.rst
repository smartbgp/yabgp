Features
========

-  It can establish BGP session based on IPv4 address (TCP Layer) in
   active mode(as TCP client);

-  Support TCP MD5 authentication(IPv4 and does not support Windows
   now);

-  BGP capabilities support: 4 Bytes ASN, Route Refresh(Cisco Route Refresh), Add Path send/receive;

-  Address family support:

   - IPv4/IPv6 unicast

   - IPv4 Flowspec(limited)

   - IPv4/IPv6 MPLSVPN

   - EVPN (partially supported)

-  Decode all BGP messages to json format and write them into files in local disk(configurable);

-  Support basic RESTFUL API for getting running information and sending BGP messages.

-  Platform support:  Linux/Unix(recommended), Mac OS and Windows.

.. note::

  yabgp is a light weight BGP agent used for connecting network devices. It only can be
  TCP client in one BGP peering connection and can't send any update messages by itself(send through REST API).
  We recommend that each yabgp process connect only one BGP neighbor, so each process is independent with each other,
  we can start many yabgp processes within the same machine or in different machines. There can be a central controller
  which can controll all yabgp processes through REST API to send BGP update messages.