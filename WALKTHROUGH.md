# 实操记录：一次完整的 PR 流程

> 2026-11-17 在 https://github.com/JackGH88/jackpr 上真实跑通的完整闭环。
> 所有输出都是当时的真实终端结果。

---

## 0. 起点

```bash
$ git log --oneline --decorate
f85b063 (HEAD -> main, tag: v1.0.0) feat: 项目初始化，实现 add / divide 与单元测试
```

`main` 上有一个可用版本，4 个测试全绿，打了 `v1.0.0`。

---

## 1. 从最新的 main 切出功能分支

```bash
$ git switch main && git pull
$ git switch -c feature/subtract
$ git push -u origin feature/subtract
```

改代码 + 补测试后提交（**一条分支只做一件事**）：

```bash
$ git commit -m "feat(calc): 新增 subtract 减法函数并补测试"
$ ./run_check.sh
Ran 6 tests in 0.000s
OK
✅ 全部通过，可以提 PR 了
```

注意：**6 个测试**。老功能的 4 个还在，新功能加 2 个 —— 这就是"没搞坏老东西"的证据。

---

## 2. 开 PR

```bash
$ gh pr create --base main --head feature/subtract
https://github.com/JackGH88/jackpr/pull/2
```

CI 自动跑起来（`.github/workflows/ci.yml`，Python 3.11 + 3.12 两个版本）：

```bash
$ gh pr checks 2 --watch
test (3.11)	pass	9s
test (3.12)	pass	6s
```

---

## 3. 对照组：一个会被拦下的坏 PR

同一个仓库里还有 `feature/refactor-divide`，它"顺手简化"了 `divide`，删掉了除零校验：

```bash
$ gh pr checks 1 --watch
test (3.11)	fail	6s
test (3.12)	fail	5s
```

本地跑更直观：

```
ERROR: test_divide_by_zero_raises
  File "calc.py", line 15, in divide
    return a / b
ZeroDivisionError: division by zero
❌ 测试挂了 —— 说明这次改动碰到了老功能的行为，先修好再提 PR
```

**它没有编译错误，没有语法问题，代码甚至更短了。**
但老代码的契约变了：`divide(1, 0)` 不再抛 `ValueError`。没有那条老测试，这个 PR 会被合并，线上就会炸。

---

## 4. 开启分支保护（关键一步）

```bash
$ gh api --method PUT repos/JackGH88/jackpr/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": {"strict": true, "contexts": ["test (3.11)", "test (3.12)"]},
  "enforce_admins": true,
  "required_pull_request_reviews": {"required_approving_review_count": 0},
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
已启用分支保护
必须走 PR: True
必需检查: ['test (3.11)', 'test (3.12)']
管理员也受限: True
```

### 验证 1：直接推 main 被拒

```bash
$ git push origin main
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - 2 of 2 required status checks are expected.
! [remote rejected] main -> main (protected branch hook declined)
```

### 验证 2：坏 PR 合并不了

```bash
$ gh pr merge 1 --squash
X Pull request JackGH88/jackpr#1 is not mergeable: the base branch policy prohibits the merge.
```

```bash
$ gh pr view 1 --json mergeStateStatus
{"mergeStateStatus": "BLOCKED"}
```

`BLOCKED` —— 页面上的按钮是灰的，点不动。**这才叫制度，不然 PR 只是"建议"。**

---

## 5. 合并 + 发版

```bash
$ gh pr merge 2 --squash --delete-branch
$ git switch main && git pull
$ git log --oneline --decorate -2
e36b052 (HEAD -> main, tag: v1.1.0, origin/main) feat(calc): 新增 subtract 减法函数并补测试 (#2)
f85b063 (tag: v1.0.0) feat: 项目初始化，实现 add / divide 与单元测试

$ git tag -a v1.1.0 -m "新增 subtract 减法函数"
$ git push origin v1.1.0
$ gh release create v1.1.0 --title "v1.1.0 新增减法" --notes "..."
https://github.com/JackGH88/jackpr/releases/tag/v1.1.0
```

`squash` 把分支上的所有提交压成一个干净提交进 main，分支自动删除，历史一条直线。

---

## 6. 这次学到了什么

| 环节 | 保证的事情 |
|---|---|
| 一条分支一件事 | 出问题能整体 revert，不用挑拣提交 |
| 分支从最新 main 切出 | 少冲突，review 时看得清 |
| 新功能自带测试 | 现在能证明它工作，将来能证明它没坏 |
| CI 跑全部测试 | 老功能被改坏时，当场发现，而不是上线后发现 |
| 分支保护 | 规则强制执行，不靠自觉 |
| squash 合并 + tag | 主干历史可读，每个版本可追溯、可回滚 |

**核心一句话**：不是"PR 让代码更安全"，而是"**PR 让"代码有没有变坏"这件事变成一个必须回答、而且能被自动回答的问题**。
