import unittest
import sys

sys.path.append('..')

from level_manager import *

class test_(unittest.TestCase):
    def test_init(self):
        level_manager = LevelManager()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
