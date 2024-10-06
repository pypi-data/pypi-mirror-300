import unittest
import os
from gedcom import *


class GedcomWithBomTest(unittest.TestCase):
    """Unit tests for simplepyged using GedcomWithBOM.ged."""

    def setUp(self):
        self.g = Gedcom(os.path.abspath('test/GedcomWithBOM.ged'))

    def test_parser(self):
        """Check if parser collected all records"""
        self.assertEqual(len(self.g.record_dict()), 1)

        self.assertEqual(len(self.g.individual_list()), 1)
        self.assertEqual(len(self.g.family_list()), 0)


if __name__ == '__main__':
    unittest.main()
