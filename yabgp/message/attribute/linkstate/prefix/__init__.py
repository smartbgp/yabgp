#    +---------------+----------------------+----------+-----------------+
#    |    TLV Code   | Description          |   Length | Reference       |
#    |     Point     |                      |          |                 |
#    +---------------+----------------------+----------+-----------------+
#    |      1152     | IGP Flags            |        1 | Section 3.3.3.1 |
#    |      1153     | IGP Route Tag        |      4*n | [RFC5130]       |
#    |      1154     | IGP Extended Route   |      8*n | [RFC5130]       |
#    |               | Tag                  |          |                 |
#    |      1155     | Prefix Metric        |        4 | [RFC5305]       |
#    |      1156     | OSPF Forwarding      |        4 | [RFC2328]       |
#    |               | Address              |          |                 |
#    |      1157     | Opaque Prefix        | variable | Section 3.3.3.6 |
#    |               | Attribute            |          |                 |
#    +---------------+----------------------+----------+-----------------+
