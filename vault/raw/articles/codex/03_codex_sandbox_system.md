# Codex CLI 深度解析 Vol.3：Sandbox System — 把 AI 关进 OS 的笼子

> **组件定位**：Sandbox 是 Codex CLI 的"执行边界"，用操作系统内核级机制限制 Agent 能触碰的文件系统范围和网络访问权。即使 LLM 生成了恶意命令，沙箱在内核层强制拦截。

---

## 1. 为什么需要 OS 级沙箱？

LLM 生成命令存在三类风险：

```
风险 A：意图正确，但命令错误
  LLM 想清理构建产物，写成了 rm -rf / 而不是 rm -rf dist/

风险 B：提示词注入
  仓库里某个文件包含恶意指令，LLM 被诱导执行危险操作

风险 C：范围扩散
  Agent 为完成任务"顺手"修改了 ~/.ssh/config 或 /etc/hosts
```

应用层过滤（如 ExecPolicy）是**意图层面的拦截**，但无法处理所有边缘情况。  
OS 级沙箱提供**执行层面的强制约束**，是最后一道防线。

---

## 2. 三平台沙箱实现

Codex 针对三个平台使用不同的 OS 原语：

### 2.1 macOS — Apple Sandbox (Seatbelt)

macOS 的 `sandbox-exec` 工具，基于 Scheme 描述语言的访问控制策略：

```
实现位置：codex-rs/core/src/platform/macos/
核心原语：sandbox-exec / entitlements
```

**工作原理：**
```scheme
; Codex 生成的 Seatbelt profile（简化示意）
(version 1)
(deny default)
(allow file-read*)                    ; 全盘可读
(allow file-write*                    ; 只允许写工作区
  (subpath "/Users/xm/myproject"))
(deny network-outbound)               ; 禁止网络
(allow process-exec)                  ; 允许启动子进程
```

特点：
- Apple 原生，零额外依赖
- 策略文件在运行时动态生成（根据 workspace 路径）
- `--log-denials` 调试模式可打印所有被拦截的系统调用

### 2.2 Linux — Landlock + seccomp

Linux 沙箱使用**两层独立机制**叠加：

```
实现位置：codex-rs/linux-sandbox/
构建产物：独立的 linux-sandbox 二进制
```

#### 层 1：Landlock（文件系统访问控制）

Landlock 是 Linux 5.13+ 引入的**不可绕过的文件系统沙箱**，基于 eBPF/LSM：

```rust
// 简化示意 —— Landlock 规则集
let ruleset = Ruleset::new()
    .add_rule(PathAccessFs::READ_FILE | PathAccessFs::READ_DIR, "/")  // 全盘读
    .add_rule(PathAccessFs::WRITE_FILE | ..., "/home/xm/project")     // 限写工作区
    .restrict_self();  // 对当前进程及所有子进程生效
```

**Landlock 的关键特性：**
- 进程一旦设置 Landlock 规则，**无法提权取消**（不可逆）
- 规则继承到所有子进程（`cargo build`、`npm install` 等也受限）
- 内核直接在 VFS 层拦截，无法被 `LD_PRELOAD` 或 ptrace 绕过

#### 层 2：seccomp（系统调用过滤）

在 Landlock 之上，额外用 seccomp 限制可用系统调用集：

```
允许：read, write, openat, execve, fork, ...
拒绝：socket（网络创建）, ptrace, mount, ...
```

两层叠加：
```
Agent 进程
  → 尝试 connect() 建立网络连接
  → seccomp: 系统调用 socket() 被拦截 → EPERM
  → 即使 seccomp 漏网，Landlock 在 VFS 层也会拦截文件操作
```

### 2.3 Windows — Experimental

```
当前状态：实验性支持，建议在 WSL 环境中使用 Linux 沙箱
实现机制：Job Objects + AppContainer（部分）
```

---

## 3. 沙箱模式（sandbox_mode）

Codex 提供三个预设级别：

```toml
# ~/.codex/config.toml

# 模式 1：只读（默认）
sandbox_mode = "read-only"
# 效果：全盘可读，不允许任何写操作，网络禁止

# 模式 2：工作区写（推荐日常使用）
sandbox_mode = "workspace-write"
# 效果：工作区目录可读写，其他路径只读，网络禁止

# 模式 3：危险全开（仅用于外部已隔离环境）
sandbox_mode = "danger-full-access"
# 效果：不应用任何 Codex 沙箱，假设调用方已做隔离
```

**动态路径注入：**  
`workspace-write` 模式下，Codex 在启动时将当前工作目录 + `~/.codex/memories` 注入到可写路径集合，无需手动配置。

---

## 4. 受保护路径（Protected Paths）

即使在 `workspace-write` 模式，以下路径强制只读：

```
工作区内部的受保护路径：
  .git/          → Git 元数据（防止 Agent 修改 hooks 或 commit history）
  .codex/        → Codex 自身配置（防止 Agent 修改自己的规则）
  
系统级受保护路径（任何模式下）：
  /etc/          → 系统配置
  /usr/          → 系统程序
  /bin/          → 基础命令
  ~/.ssh/        → SSH 密钥（隐式保护）
```

**工程原则：**  
> 即使信任工作区，也不信任 Git 历史的完整性。  
> Agent 不应该能修改它自己执行所依赖的规则（`.codex/`）。

---

## 5. 网络访问控制

网络控制是沙箱的重要维度：

```
默认：网络禁止
  → npm install, cargo build, curl 等均会失败
  → 防止数据外泄，防止 Agent 下载恶意代码

显式启用（工作区写模式下）：
  [sandbox_workspace_write]
  network_access = true

Codex Cloud 的两阶段模型（更精细）：
  setup 阶段：允许网络（安装依赖）
  agent 阶段：禁止网络（执行任务）
  
  → 依赖在隔离环境准备好后，agent 在离线状态运行
  → 防止 agent 在执行过程中泄露代码
```

---

## 6. 沙箱测试工具

Codex 内置沙箱调试命令，可在真实沙箱中测试任意命令：

```bash
# macOS：在 seatbelt 沙箱中测试命令行为
codex sandbox macos ls /etc
codex sandbox macos --log-denials curl https://example.com

# Linux：在 Landlock+seccomp 沙箱中测试
codex sandbox linux cat /etc/passwd
codex sandbox linux --full-auto npm install

# 评估 execpolicy 规则（不实际执行）
codex execpolicy check --rules ~/.codex/rules.toml git push --force
```

---

## 7. Sandbox ↔ ExecPolicy 协同

两层设计各自独立，但协同工作：

```
命令进来
    │
    ▼
ExecPolicy 评估
    ├── forbidden  →  直接拒绝，不进沙箱
    ├── prompt     →  暂停，等人类审批
    │                 ├── 批准  →  进沙箱执行
    │                 └── 拒绝  →  结束
    └── allow      →  直接进沙箱执行
                           │
                    OS 内核层强制约束
                    （无论 policy 说什么，
                     内核说不行就不行）
```

**关键洞察**：ExecPolicy 是**意图过滤器**，Sandbox 是**能力约束器**。  
一个好的系统，两者都需要。

---

## 8. 工程智慧总结

| 设计决策 | 背后原因 |
|---------|---------|
| 使用 Landlock 而非 chroot | Landlock 不可逆、继承到子进程、不需要 root 权限 |
| 默认禁止网络 | 失败安全原则：宁可任务失败，不可数据泄露 |
| 保护 .git 和 .codex | 防止 Agent 修改自己的执行规则（反射性攻击）|
| 全盘可读策略 | Agent 需要读取上下文才能工作，读不会直接造成损害 |
| 双层沙箱（Landlock + seccomp）| 纵深防御，单层突破不等于完全逃逸 |
| 内置沙箱测试工具 | 沙箱配置错误本身是不确定性来源，可测试消除之 |

---

*下一篇：Vol.4 — ExecPolicy：策略即代码的命令审批引擎*
