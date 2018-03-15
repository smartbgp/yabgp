# #
#    +-----------+---------------------+--------------+------------------+
#    |  TLV Code | Description         |  IS-IS TLV   | Reference        |
#    |   Point   |                     |   /Sub-TLV   | (RFC/Section)    |
#    +-----------+---------------------+--------------+------------------+
#    |    1028   | IPv4 Router-ID of   |   134/---    | [RFC5305]/4.3    |
#    |           | Local Node          |              |                  |
#    |    1029   | IPv6 Router-ID of   |   140/---    | [RFC6119]/4.1    |
#    |           | Local Node          |              |                  |
#    |    1030   | IPv4 Router-ID of   |   134/---    | [RFC5305]/4.3    |
#    |           | Remote Node         |              |                  |
#    |    1031   | IPv6 Router-ID of   |   140/---    | [RFC6119]/4.1    |
#    |           | Remote Node         |              |                  |
#    |    1088   | Administrative      |     22/3     | [RFC5305]/3.1    |
#    |           | group (color)       |              |                  |
#    |    1089   | Maximum link        |     22/9     | [RFC5305]/3.4    |
#    |           | bandwidth           |              |                  |
#    |    1090   | Max. reservable     |    22/10     | [RFC5305]/3.5    |
#    |           | link bandwidth      |              |                  |
#    |    1091   | Unreserved          |    22/11     | [RFC5305]/3.6    |
#    |           | bandwidth           |              |                  |
#    |    1092   | TE Default Metric   |    22/18     | Section 3.3.2.3  |
#    |    1093   | Link Protection     |    22/20     | [RFC5307]/1.2    |
#    |           | Type                |              |                  |
#    |    1094   | MPLS Protocol Mask  |     ---      | Section 3.3.2.2  |
#    |    1095   | IGP Metric          |     ---      | Section 3.3.2.4  |
#    |    1096   | Shared Risk Link    |     ---      | Section 3.3.2.5  |
#    |           | Group               |              |                  |
#    |    1097   | Opaque Link         |     ---      | Section 3.3.2.6  |
#    |           | Attribute           |              |                  |
#    |    1098   | Link Name           |     ---      | Section 3.3.2.7  |
#    +-----------+---------------------+--------------+------------------+

#                        Table 9: Link Attribute TLVs

#    +-----------+----------------------------+----------+---------------+
#    |  TLV Code | Description                |   Length |       Section |
#    |   Point   |                            |          |               |
#    +-----------+----------------------------+----------+---------------+
#    |    1099   | Adjacency Segment          | variable | Section 2.2.1 |
#    |           | Identifier (Adj-SID) TLV   |          |               |
#    |    1100   | LAN Adjacency Segment      | variable | Section 2.2.2 |
#    |           | Identifier (Adj-SID) TLV   |          |               |
#    +-----------+----------------------------+----------+---------------+


#    +----------+---------------------------+----------+
#    | TLV Code | Description               |   Length |
#    |  Point   |                           |          |
#    +----------+---------------------------+----------+
#    |    1101  | Peer Node Segment         | variable |
#    |          | Identifier (Peer-Node-SID)|          |
#    |    1102  | Peer Adjacency Segment    | variable |
#    |          | Identifier (Peer-Adj-SID) |          |
#    |    1103  | Peer Set Segment          | variable |
#    |          | Identifier (Peer-Set-SID) |          |
#    +----------+---------------------------+----------+
