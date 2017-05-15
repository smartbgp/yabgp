# 3.3.1.  Node Attribute TLVs

#    Node attribute TLVs are the TLVs that may be encoded in the BGP-LS
#    attribute with a Node NLRI.  The following Node Attribute TLVs are
#    defined:

#    +-------------+----------------------+----------+-------------------+
#    |   TLV Code  | Description          |   Length | Reference         |
#    |    Point    |                      |          | (RFC/Section)     |
#    +-------------+----------------------+----------+-------------------+
#    |     263     | Multi-Topology       | variable | Section 3.2.1.5   |
#    |             | Identifier           |          |                   |
#    |     1024    | Node Flag Bits       |        1 | Section 3.3.1.1   |
#    |     1025    | Opaque Node          | variable | Section 3.3.1.5   |
#    |             | Attribute            |          |                   |
#    |     1026    | Node Name            | variable | Section 3.3.1.3   |
#    |     1027    | IS-IS Area           | variable | Section 3.3.1.2   |
#    |             | Identifier           |          |                   |
#    |     1028    | IPv4 Router-ID of    |        4 | [RFC5305]/4.3     |
#    |             | Local Node           |          |                   |
#    |     1029    | IPv6 Router-ID of    |       16 | [RFC6119]/4.1     |
#    |             | Local Node           |          |                   |
#    +-------------+----------------------+----------+-------------------+

# +----------------+-----------------+----------+---------------+
# | TLV Code Point | Description     | Length   |       Section |
# +----------------+-----------------+----------+---------------+
# |      1034      | SR Capabilities | variable | Section 2.1.1 |
# |      1035      | SR Algorithm    | variable | Section 2.1.2 |
# |      1036      | SR Local Block  | variable | Section 2.1.3 |
# |      1037      | SRMS Preference | variable | Section 2.1.4 |
# +----------------+-----------------+----------+---------------+
