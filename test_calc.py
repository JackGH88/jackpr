"""单元测试 = 主分支的"安全带"。

测试就是用来在 PR 阶段回答那个核心问题的：
"这次改动有没有把 main 上原本好好的老功能搞坏？"
"""

import unittest

from calc import add, divide


class TestAdd(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-2, 3), 1)


class TestDivide(unittest.TestCase):
    def test_divide_normal(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero_message(self):
        # 错误信息里要带上下文，线上排查才知道是谁除零
        with self.assertRaisesRegex(ValueError, "除数不能为 0"):
            divide(7, 0)

    def test_divide_by_zero_raises(self):
        # 老约定：除零必须抛 ValueError，不能返回 0 或 inf
        with self.assertRaises(ValueError):
            divide(1, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
