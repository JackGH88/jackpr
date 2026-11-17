#!/usr/bin/env bash
# 本地质量门禁：push / 开 PR 之前自己先跑一遍。
# 只有全绿，才值得让 main 接受你的代码。
set -u

echo "▶ 1/2 跑单元测试"
if ! python3 -m unittest discover -s . -p "test_*.py" -v; then
  echo "❌ 测试挂了 —— 说明这次改动碰到了老功能的行为，先修好再提 PR"
  exit 1
fi

echo "▶ 2/2 检查是否留下未完成标记"
if grep -rn "TODO_\|FIXME_" --include="*.py" . ; then
  echo "❌ 代码里还有未完成标记，别把半成品合进 main"
  exit 1
fi

echo "✅ 全部通过，可以提 PR 了"
