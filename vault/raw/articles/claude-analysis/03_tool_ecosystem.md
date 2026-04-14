# 03 · 工具生态系统（Tool Ecosystem）

> **设计哲学**：Primitives > Integrations
> 用 4 个通用基元替代 100 个脆弱的专用插件集成。
> Bash 是终极通用适配器——任何 CLI 工具都可通过它调用。

---

## 工具调用数据流

```
LLM 输出 JSON Tool Call（tool_name + tool_input）
                  │
                  ▼
        PreToolUse Hook 检查
                  │
            ┌─────┴────────┐
         拦截 (exit 2)    放行
            │              │
            ▼              ▼
       阻止执行       ToolEngine 解析 & 路由
                           │
                           ▼
                    沙箱执行环境
                    （带权限白名单检查）
                           │
                           ▼
                    结果以纯文本返回
                           │
                           ▼
                  PostToolUse Hook（质量门）
                           │
                           ▼
                    追加到消息历史
```

所有工具遵循统一接口：**JSON in → 纯文本 out**。

---

## 完整工具清单

### 一、Read & Discovery（读取与发现）

| 工具 | 功能 | 关键设计细节 |
|------|------|------------|
| `View` | 读取文件内容 | 默认 ~2000 行；分页读取，避免上下文爆炸 |
| `LS` | 目录列表 | 轻量文件系统探索 |
| `Glob` | 通配符文件搜索 | 跨大型仓库快速定位文件集合 |
| `GrepTool` | 全正则搜索（ripgrep 内核）| 精确匹配，无近似误差 |

#### 为什么用 GrepTool 而非向量检索？

```
向量检索的问题：
  · 近似匹配 → 可能错过精确目标
  · 索引漂移 → 代码变更后需重建索引
  · 运维成本 → Milvus/Pinecone 需要维护
  · 不确定性 → 相似度阈值调参困难

GrepTool 的优势：
  · 精确匹配 → 确定性结果
  · 零维护 → 无索引，直接搜索
  · Claude 能力 → 对代码语义的深度理解
                  使其能构造精确正则表达式
  · 速度 → ripgrep 基于 Rust，极快

示例：让 Claude 自己构造正则
    "找所有使用 UserService 且抛出 AuthException 的方法"
    → grep -rn "def.*UserService.*:" --include="*.py" 结合
    → grep -A 10 "AuthException" 的组合
```

---

### 二、Write & Edit（写入与编辑）

| 工具 | 功能 | 适用场景 | 呈现方式 |
|------|------|---------|---------|
| `Edit` | 精外科手术 patch | 修改特定函数/行/块 | 最小化 diff |
| `Write/Replace` | 全文覆盖写入 | 大范围重写、新内容 | 完整文件 |
| `MultiEdit` | 一次多处编辑 | 跨多位置的批量修改 | 聚合 diff |
| `Create` | 新建文件 | 初始化模块/配置 | 完整文件 |

#### Diff 工作流的工程价值

```
为什么 Diff 比全文替换更好？

可审计性：
  每次变更都有清晰的 before/after
  → 人类可以在 Claude 修改前 review

可回滚：
  所有变更被追踪
  → 出错时可精确回滚

最小化原则：
  只修改需要修改的部分
  → 减少意外的副作用

示例：
  # Edit 工具生成的 diff
  - def authenticate(self, username, password):
  -     return self.db.check(username, password)
  + def authenticate(self, username: str, password: str) -> bool:
  +     hashed = bcrypt.hash(password)
  +     return self.db.check(username, hashed)
```

---

### 三、Execute（执行）

| 工具 | 功能 | 特性 |
|------|------|------|
| `Bash` | 持久 Shell 会话 | 状态持久 · 安全过滤 · 风险分级 |

#### 持久 Shell 会话的价值

```bash
# 传统方式（每次独立进程）：
subprocess.run("cd /project && npm install")  # cd 效果消失
subprocess.run("npm test")                     # 需要重新 cd

# Claude Code Bash（持久会话）：
$ cd /project
$ npm install      # 工作目录持久保持
$ npm test         # 无需重新定位
$ git commit -m "fix auth"  # 环境变量也持久
```

#### 安全过滤层（确定性）

```python
# 注入检测 - 确定性拦截，不经过 LLM 判断
INJECTION_PATTERNS = [
    "`",           # 命令替换
    "$(",          # 命令替换
    "${",          # 变量替换攻击
    "$((",         # 算术扩展
]

def check_injection(command: str) -> bool:
    for pattern in INJECTION_PATTERNS:
        if pattern in command:
            raise SecurityError(f"检测到潜在注入模式：{pattern}")
    return True
```

#### 风险分级系统（LLM 辅助）

```
LOW  风险：git status, ls, cat file.py
     → 自动执行，无需确认

MEDIUM 风险：git commit, npm install
     → 如在白名单中自动执行，否则提示确认

HIGH 风险：rm -rf, DROP TABLE, git push --force
     → 始终要求用户明确确认

BLOCK（Hook 拦截）：rm -rf /, DROP TABLE users
     → PreToolUse Hook exit 2，直接阻止
```

#### Sandbox 沙箱模式（CI/CD 场景）

```bash
# init-firewall.sh 限制 Bash 工具的出站网络访问
# 只允许白名单域名

示例白名单（仅用于构建）：
  · api.anthropic.com    （Claude API）
  · registry.npmjs.org   （npm 包）
  · pypi.org             （Python 包）
  · github.com           （代码拉取）

效果：
  · Agent 无法意外访问生产 API
  · 防止在 CI 中泄露生产凭证
  · 隔离测试环境与外部服务
```

---

### 四、Connect（连接）—— Task 工具

| 工具 | 功能 | 深度限制 |
|------|------|---------|
| `Task` | 派生子 Agent | 最大深度 = 1（严格）|

```python
# Task 工具调用示例
{
  "tool": "Task",
  "goal": "在 src/auth/ 中找出所有 JWT 相关函数，返回函数签名列表",
  "model": "claude-haiku-4-5",   # 探索任务用便宜模型
  "context": "minimal",          # 子 Agent 获得最小上下文
  "worktree": true               # 在独立 Git Worktree 中执行
}
# 仅返回结论，不污染主上下文
```

---

## 工具选择决策树

```
需要了解代码结构？
    ├─ 找特定文件 → Glob
    ├─ 找特定内容 → GrepTool（正则）
    └─ 读文件内容 → View

需要修改代码？
    ├─ 修改现有文件的特定部分 → Edit
    ├─ 完全重写文件 → Write/Replace
    ├─ 一次改多处 → MultiEdit
    └─ 创建新文件 → Create

需要执行操作？
    ├─ 任何 CLI 工具 → Bash
    └─ 需要隔离执行 → Bash + Sandbox Mode

需要复杂子任务？
    └─ 并行探索 / 上下文隔离 → Task（子 Agent）

需要外部服务？
    └─ GitHub / DB / Slack → MCP 服务器工具
```

---

## 工具权限矩阵

| 工具 | 默认权限 | 可加白名单 | 可被 Hook 拦截 |
|------|---------|----------|--------------|
| View / LS / Glob | 自动允许 | — | 否（只读） |
| GrepTool | 自动允许 | — | 否（只读） |
| Edit / Write | 需确认 | 可白名单 | 是（PreToolUse）|
| Bash | 需确认（按风险）| 可白名单特定命令 | 是（PreToolUse）|
| Task | 需确认 | 可白名单 | 是 |
| MCP 工具 | 需确认 | `mcp__server__*` | 是 |
