"""练习用极简模块：一个"已有功能"的库。

主分支（main）上的代码永远是"能上线的版本"。
任何新功能都从 main 拉分支去做，做完走 PR 回到 main。
"""


def add(a, b):
    """加法。v1.0.0 就有的老功能。"""
    return a + b


def subtract(a, b):
    """减法。v1.1.0 新增的功能（在 feature/subtract 分支上做的）。"""
    return a - b


def divide(a, b):
    """除法。顺手"优化"掉了除零校验 —— 这就是一次典型的老功能回归。"""
    return a / b
