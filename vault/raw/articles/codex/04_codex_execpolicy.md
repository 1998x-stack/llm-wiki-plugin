# Codex CLI 深度解析 Vol.4：ExecPolicy — 策略即代码的命令审批引擎

> **组件定位**：ExecPolicy 是一个独立的规则引擎，位于 Sandbox 之前。它把"哪些命令允许、哪些需要审批、哪些禁止"这个判断从硬编码逻辑中解放出来，变成可版本化、可测试、可共享的**策略声明文件**。

---

## 1. 核心思想：Policy as Code

传统 Agent 安全做法：把危险命令硬编码在黑名单里。

```python
# 传统做法（硬编码，脆弱）
BLACKLIST = ["rm -rf", "shutdown", "dd if="]
if any(cmd.startswith(b) for b in BLACKLIST):
    deny()
```

Codex 的做法：把规则写成**结构化规则文件**，支持版本控制、单元测试、团队共享：

```toml
# ~/.codex/rules/safe.rules（ExecPolicy 规则文件）
[[rule]]
name = "allow-git-read"
prefix = ["git", ["log", "status", "diff", "show"]]
decision = "allow"
justification = "只读 git 操作，安全"

[[rule]]
name = "prompt-git-push"
prefix = ["git", "push"]
decision = "prompt"
justification = "推送到远程，需要人工确认"

[[rule]]
name = "forbid-git-force-push"
prefix = ["git", "push", "--force"]
decision = "forbidden"
justification = "强制推送可能覆盖他人工作，禁止。请使用 git push --force-with-lease"
```

---

## 2. 规则语法详解

### 2.1 基本结构

```toml
[[rule]]
name = "规则名称"            # 人类可读标识
prefix = [...]              # 命令前缀匹配模式
decision = "allow"          # allow | prompt | forbidden
justification = "原因说明"   # 在 approval UI 或错误信息中展示

# 内置单元测试（load time 验证）
match = [
  ["git", "status"],        # 应匹配此规则
  "git log --oneline"       # 字符串会用 shlex 分词
]
not_match = [
  ["git", "push"],          # 不应匹配此规则
]
```

### 2.2 前缀匹配语法

```toml
# 精确前缀：命令必须以此开头
prefix = ["npm", "install"]
# 匹配：npm install express
# 不匹配：npm run build

# 列表表示"或"：数组内任意一个均匹配
prefix = ["git", ["log", "status", "diff"]]
# 匹配：git log, git status, git diff
# 不匹配：git push, git commit

# 嵌套或：
prefix = [["npm", "yarn"], "install"]
# 匹配：npm install, yarn install
```

### 2.3 三态决策

```
allow    → 直接放行，不触发 Approval Gate
prompt   → 暂停，在 TUI 显示审批弹窗，等待人类决策
forbidden → 直接拒绝，命令不执行，向 Agent 返回错误 + justification
```

**forbidden 的工程价值：**  
当命令被 forbidden 时，Codex 会把 `justification` 中的建议方案返回给 LLM。  
LLM 可以根据建议重新规划（如用 `--force-with-lease` 替代 `--force`），实现**自动纠错循环**。

---

## 3. 规则评估机制

### 3.1 前缀树匹配

规则在 load 时构建成**前缀树（Trie）**，O(k) 时间匹配（k = 命令 token 数）：

```
规则树（示意）：
  git
  ├── log      → allow
  ├── status   → allow
  ├── push
  │   ├── --force  → forbidden
  │   └── *        → prompt
  └── commit   → prompt
  npm
  ├── install  → allow
  └── run      → allow
  rm
  └── -rf      → forbidden
```

### 3.2 规则优先级

```
1. 更具体的规则优先（更长的前缀匹配）
2. 多个规则文件合并时，按 --rules 参数顺序评估
3. 先匹配先生效（first-match）
4. 无匹配规则时，fallback 到 approval_policy 全局设置
```

### 3.3 Host Executable 解析

当启用 `--resolve-host-executables` 时：

```
命令：/usr/bin/git status
               ↓
系统解析：/usr/bin/git 的 basename = git
               ↓
规则匹配：查找 prefix = ["git", ...] 的规则
               ↓
如果有 host_executable(name="git") 声明：
  仅允许 /usr/bin/git 路径，不允许其他 git
```

这防止了 **PATH 欺骗攻击**：Agent 无法通过将恶意程序命名为 `git` 并放入 PATH 来绕过规则。

---

## 4. 规则文件的存储层次

ExecPolicy 规则文件遵循 Config 系统的层次结构：

```
优先级（高 → 低）：

~/.codex/rules/         # 用户级：个人安全偏好
  └── safe.rules

{project}/.codex/rules/ # 项目级：团队共享规则（提交到 Git）
  └── project.rules

/etc/codex/rules/       # 系统级：企业策略（IT 管理员设置）
  └── enterprise.rules
```

**团队共享的工程价值：**  
把项目级规则提交到仓库，团队所有成员使用相同的 ExecPolicy。  
新成员 clone 仓库后，自动获得与团队一致的安全策略。

---

## 5. 与 approval_policy 的关系

```
approval_policy（全局）：
  控制"当没有规则匹配时"的默认行为

ExecPolicy rules（具体）：
  覆盖特定命令的默认行为

优先级：具体规则 > 全局 policy

示例：
  approval_policy = "never"     # 全局全自动
  + rule: git push → prompt     # 但 git push 必须手动确认

  approval_policy = "on-request" # 全局遇到不确定就问
  + rule: npm install → allow    # 但 npm install 直接放行（已知安全）
```

---

## 6. 实战：调试 ExecPolicy

```bash
# 检查命令会触发哪个规则（不实际执行）
codex execpolicy check \
  --rules ~/.codex/rules/safe.rules \
  git push --force

# 输出示例：
{
  "decision": "forbidden",
  "matched_rule": "forbid-git-force-push",
  "justification": "强制推送可能覆盖他人工作，禁止。请使用 git push --force-with-lease"
}

# 合并多个规则文件检查
codex execpolicy check \
  --rules ~/.codex/rules/safe.rules \
  --rules .codex/rules/project.rules \
  --pretty \
  rm -rf dist/
```

**Load-time 单元测试：**  
规则文件加载时，`match` / `not_match` 中的示例会自动运行验证。  
规则错误在启动时就会被发现，而不是在执行时。

---

## 7. ExecPolicy 降低不确定性的机制

| 不确定性场景 | ExecPolicy 的应对 |
|------------|-----------------|
| LLM 生成不安全命令 | `forbidden` 规则直接拒绝 + 返回替代建议 |
| 不知道某命令是否安全 | `prompt` 规则让人类在执行前决策 |
| 团队成员安全策略不一致 | 项目级规则文件提交 Git，统一策略 |
| 新加的规则引入了 bug | `match/not_match` 单元测试在 load time 捕获 |
| 规则被 PATH 欺骗绕过 | host_executable 解析绑定绝对路径 |
| Agent 绕过策略重复尝试 | forbidden + justification 引导 LLM 走正确路径 |

---

## 8. 工程哲学摘要

> **ExecPolicy 把安全策略从"运行时判断"变成了"编译时声明"。**
>
> 规则在加载时就被验证，在执行时被机械地应用。
> 没有临时判断，没有模糊地带，没有"这次特殊情况"。
>
> 这是把不确定性（"AI 会不会乱来？"）转化为确定性（"这条规则说不行就不行"）的关键机制。

---

*下一篇：Vol.5 — Session Manager：Agent 记忆与上下文的持久化*
