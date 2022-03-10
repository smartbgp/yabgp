import unittest
from yabgp.message.attribute.linkstate.node.node_msd import NodeMSD_266


class TestNodeMSD(unittest.TestCase):

    def test_unpack_for_type266(self):
        '''
        Node MSD TLV: https://datatracker.ietf.org/doc/html/rfc8814#section-3
        IGP MSD-Types: https://www.iana.org/assignments/igp-parameters/igp-parameters.xhtml
        '''
        data_bin = b'\x29\x03\x2a\x03\x2b\x03\x2c\x03\x2d\x04'
        expected_results = {"type": "node_msd",
                            "value": [{'type': 41, 'value': 3},
                                      {'type': 42, 'value': 3},
                                      {'type': 43, 'value': 3},
                                      {'type': 44, 'value': 3},
                                      {'type': 45, 'value': 4}]}

        actual_results = NodeMSD_266.unpack(data=data_bin).dict()

        self.assertEqual(expected_results, actual_results)


if __name__ == "__main__":
    unittest.main()
