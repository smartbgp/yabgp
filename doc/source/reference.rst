Reference
=========


RFCs
----

* RFC1997(BGP Communities Attribute)
* RFC2385(Protection of BGP Sessions via the TCP MD5 Signature Option)
* RFC2439(BGP Route Flap Damping)
* RFC2545(Use of BGP-4 Multiprotocol Extensions for IPv6 Inter-Domain Routing)
* RFC2858(Multiprotocol Extensions for BGP-4)
* RFC2918(Route Refresh Capability for BGP-4)
* RFC3031(Multiprotocol Label Switching Architecture)
* RFC3032(MPLS Label Stack Encoding)
* RFC3065 (Autonomous System Confederations for BGP)
* RFC3107(Carrying Label Information in BGP-4)
* RFC3392(Capabilities Advertisement with BGP-4)
* RFC4271(A Border Gateway Protocol 4)
* RFC4360(BGP Extended Communities Attribute)
* RFC4364(BGPMPLS IP Virtual Private Networks (VPNs))
* RFC4456(BGP Route Reflection An alternative to Full Mesh Internal BGP)
* RFC4724(Graceful Restart Mechanism for BGP)
* RFC4760( Multiprotocol Extensions for BGP-4)
* RFC4798(Connecting IPv6 Islands over IPv4 MPLS Using IPv6 Provider Edge Routers (6PE))
* RFC4893(BGP Support for Four-octet AS Number Space).txt
* RFC5065(Autonomous System Confederations for BGP)
* RFC5291(Outbound Route Filtering Capability for BGP-4)
* RFC5396(Textual Representation of Autonomous System (AS) Numbers).txt
* RFC5492(Capabilities Advertisement with BGP-4)
* RFC5668(4-Octet AS Specific BGP Extended Community)
* RFC5701(IPv6 Address Specific BGP Extended Community Attribute)
* RFC6368(Internal BGP as the ProviderCustomer Edge Protocol for BGPMPLS IP Virtual Private Networks (VPNs))
* RFC6472 (Recommendation for Not Using AS_SET and AS_CONFED_SET in BGP)
* RFC6513(Multicast in MPLS BGP IP VPNs)
* RFC6774(Distribution of Diverse BGP Paths)


Code
----

IOS/IOX
-------

1. BGP FlowSpec configuration

.. code-block:: bash
    :emphasize-lines: 3,5

    class-map type traffic match-all bflow
     match destination-address ipv4 2.2.2.0 255.255.255.0
     match source-address ipv4 3.3.0.0 255.255.0.0
     match protocol ipv4 gre eigrp icmp igmp ospf pim
     match source-port 80 8080 8081 8082 8083
     match ipv4 icmp-type 2 3 5 6
     match ipv4 icmp-code 2
     match tcp-flag 40
     match packet length 254 254-300
     match dscp cs5 cs6
     match fragment-type  dont-fragment
     match destination-port 8080-8090
     end-class-map

     policy-map type pbr bflow
     class type traffic bflow
      set dscp ef

     router bgp 100
     bgp router-id 1.1.1.1
     address-family ipv4 unicast
      network 1.1.1.1/32
     !
     address-family vpnv4 unicast
     !
     address-family ipv6 unicast
     !
     address-family ipv4 flowspec
     !
     neighbor 10.75.44.121
      remote-as 100
      password encrypted 121A0C041104
      update-source MgmtEth0/0/CPU0/0
      address-family ipv4 flowspec
       route-policy XR in
       route-policy XR out
      !
     !


     flowspec
     address-family ipv4
      service-policy type pbr bflow
      service-policy type pbr match_dest_110.1.1.x_drop
      service-policy type pbr match_src_10.1.1.10_police
      service-policy type pbr match_proto_gre_redir_nh_ipv4
     !