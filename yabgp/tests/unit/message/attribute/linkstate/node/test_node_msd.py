import unittest
from yabgp.message.attribute.linkstate.node.node_msd import NodeMSD_266


class TestNodeMSD(unittest.TestCase):

    def test_unpack_for_type266(self):
        data_bin = b'\x29\x03\x2a\x03\x2b\x03\x2c\x03\x2d\x04'
        expected_results = {"type": "node_msd",
                            "value": [{'MSD_Type': 41, 'MSD_Value': 3},
                                      {'MSD_Type': 42, 'MSD_Value': 3},
                                      {'MSD_Type': 43, 'MSD_Value': 3},
                                      {'MSD_Type': 44, 'MSD_Value': 3},
                                      {'MSD_Type': 45, 'MSD_Value': 4}]}

        actual_results = NodeMSD_266.unpack(data=data_bin).dict()

        self.assertEqual(expected_results, actual_results)


if __name__ == "__main__":
    unittest.main()
