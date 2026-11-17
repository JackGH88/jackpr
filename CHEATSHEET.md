# Git / GitHub 分支与 PR 速查表

练习仓库位置：`/Users/jack/WorkBuddy/学习PR/git-lab`

---

## 一、日常循环（每天都是这套）

```bash
# 0) 切回主干、拉最新（分支要从最新的 main 长出来）
git switch main
git pull

# 1) 开新分支，一条分支只干一件事
git switch -c feature/subtract     # 新功能
# git switch -c fix/divide-zero    # 修 bug
# git switch -c docs/readme        # 纯文档

# 2) 写代码 + 写测试，然后分小步提交
git add -A
git commit -m "feat(calc): 新增 subtract 减法函数并补测试"

# 3) 推送分支到远端（第一次要 -u 建立跟踪）
git push -u origin feature/subtract

# 4) 开 PR（推荐用 gh，一行搞定）
gh pr create --base main --fill    # 或者去网页点 "Compare & pull request"

# 5) 等 CI 绿 + 至少一个人 review 通过 → 合并
gh pr merge --squash --delete-branch

# 6) 回本地收拾干净
git switch main && git pull && git branch -d feature/subtract
```

---

## 二、commit 信息规范（Conventional Commits）

| 前缀                           | 用途           | 例子                 |
| ---------------------------- | ------------ | ------------------ |
| `feat:`                      | 新功能          | `feat: 支持导出 CSV`   |
| `fix:`                       | 修 bug        | `fix: 修复除零崩溃`      |
| `refactor:`                  | 重构（不改行为）     | `refactor: 抽出公共方法` |
| `docs:` / `test:` / `chore:` | 文档 / 测试 / 杂活 | `docs: 补部署说明`      |
| `!` 或 `BREAKING CHANGE`      | 破坏性改动        | `feat!: 移除 v1 接口`  |

好处：`git log` 一眼看懂；自动生成发版说明；出问题时能快速定位是哪个改动引入的。

---

## 三、PR 的三道关卡（保证 main 不出事）

1. **自动化门禁**：CI 跑全部测试（老测试 + 新测试）。红灯 = 不许合。
2. **人工 review**：别人看你的 diff，问"为什么要改这里""老代码依赖这个行为吗"。
3. **分支保护规则**（GitHub 仓库 Settings → Branches）：
   - Require a pull request before merging ✅
   - Require status checks to pass ✅（选 CI）
   - Require approvals: 1 ✅
   - Do not allow bypassing（管理员也一样）✅
   - Require linear history / squash merge（可选，历史更干净）

**没开分支保护，PR 就只是"建议"；开了才是"制度"。**

---

## 四、冲突处理（main 也前进过导致的）

```bash
git switch feature/subtract
git fetch origin
git rebase origin/main        # 把自己的提交挪到最新 main 之后（推荐）
# 冲突了就编辑文件，删掉 <<<<<<< ======= >>>>>>> 标记
git add <冲突文件>
git rebase --continue         # 想放弃：git rebase --abort
git push --force-with-lease   # rebase 改写了历史，必须强推（用 --force-with-lease 不要 --force）
```

不想 rebase 就用合并：`git merge origin/main` 然后正常 push。

**原则：先自己解决冲突，别把冲突甩给 main。**

---

## 五、版本管理（Tag / SemVer）

```bash
git tag -a v1.1.0 -m "新增 subtract"
git push origin v1.1.0            # tag 要单独推
git tag -l 'v1.*'                 # 看有哪些版本
git show v1.1.0                   # 看某版本包含什么
```

语义化版本 `主版本.次版本.修订号`：

- **1**.0.0 → 不兼容的大改（老用户代码会坏）
- 1.**1**.0 → 加功能，向后兼容
- 1.1.**1** → 只修 bug

GitHub 上对应<u> </u>**Releases** 页，把 tag 变成可下载的发行版 + 更新说明。

---

## 六、出事怎么办（回滚）

```bash
# 还没合进 main：直接扔掉分支
git branch -D feature/xxx

# 已合并，要撤销那个提交（安全，生成一个新提交抵消它）
git revert <commit-id> && git push

# 本地没提交的乱改：全部丢弃
git restore .

# 只是切到某个旧版本看看（不要在上面提交）
git switch --detach v1.0.0
```

⚠️ 不要在共享分支上用 `git reset --hard` + 强推，会把别人的提交一起干掉。

---

## 七、几个救命命令

```bash
git status                 # 我现在在哪、改了啥（最高频）
git log --graph --oneline --all --decorate   # 分支结构全景图
git diff main              # 我这条分支相对 main 改了什么
git log --oneline main..HEAD                 # 我比 main 多了哪些提交
git branch -vv             # 每个分支跟踪哪个远端、领先/落后多少
git stash / git stash pop  # 临时收起来 / 取回来
git blame <file>           # 这行是谁、哪次提交改的
```
