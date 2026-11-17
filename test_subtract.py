"""新功能自带测试 —— 这是 PR 能过的前提。"""

import unittest

from calc import subtract


class TestSubtract(unittest.TestCase):
    def test_subtract_positive(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_subtract_to_negative(self):
        self.assertEqual(subtract(3, 5), -2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
