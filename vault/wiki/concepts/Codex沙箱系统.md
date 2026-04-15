---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [Codex Sandbox, Codex Sandbox System]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[ExecPolicy]]"
    type: extends
    confidence: 0.9
  - target: "[[Landlock]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Codex沙箱系统

[[Codex CLI]] 的执行边界层，用**操作系统内核级机制**限制 Agent 能触碰的文件系统范围和网络权限。即使 LLM 生成了恶意命令，沙箱在内核层强制拦截——是 [[Codex CLI]] 三道防线中的最后一道。

## 为什么需要 OS 级沙箱

应用层过滤（如 [[ExecPolicy]]）是**意图层面的拦截**，无法处理所有边缘情况：

| 风险类型 | 示例 |
|---------|------|
| 意图正确，命令错误 | LLM 想清理 dist/，写成了 `rm -rf /` |
| 提示词注入 | 仓库文件包含恶意指令，诱导 LLM 执行危险操作 |
| 范围扩散 | Agent "顺手"修改 `~/.ssh/config` 或 `/etc/hosts` |

OS 级沙箱提供**执行层面的强制约束**。

## 三平台实现

### macOS — Apple Sandbox (Seatbelt)

基于 Scheme 描述语言的访问控制策略（`sandbox-exec`），动态生成：全盘可读、只写工作区、禁止网络出站。支持 `--log-denials` 调试模式。

### Linux — Landlock + seccomp（双层）

**层 1：Landlock**（Linux 5.13+ 引入）

基于 eBPF/LSM 的不可绕过文件系统沙箱：
- 进程设置后**无法提权取消**（不可逆）
- 规则自动继承到所有子进程（`cargo build`、`npm install` 等也受限）
- 在 VFS 层拦截，无法被 `LD_PRELOAD` 或 ptrace 绕过

**层 2：seccomp**（系统调用过滤）

在 Landlock 之上额外限制可用系统调用集：允许 `read/write/openat/execve`，拒绝 `socket/ptrace/mount` 等。两层叠加形成纵深防御，单层突破不等于完全逃逸。

### Windows

实验性支持（Job Objects + AppContainer），建议在 WSL 中使用 Linux 沙箱。

## 沙箱模式（sandbox_mode）

| 模式 | 文件系统 | 网络 | 适用场景 |
|------|---------|------|---------|
| `read-only`（默认） | 全盘可读，不可写 | 禁止 | 审阅/规划阶段 |
| `workspace-write` | 工作区读写，其他只读 | 默认禁止 | 日常开发 |
| `danger-full-access` | 无限制 | 无限制 | 外部已隔离环境 |

`workspace-write` 模式启动时自动将当前工作目录 + `~/.codex/memories` 注入可写路径，无需手动配置。

## 受保护路径

即使在 `workspace-write` 模式，以下路径强制只读：
- `.git/` — 防止 Agent 修改 hooks 或 commit history
- `.codex/` — 防止 Agent 修改自己的执行规则（反射性攻击防护）
- `/etc/`、`/usr/`、`/bin/`、`~/.ssh/` 等系统路径

## 网络访问控制

默认禁止网络（失败安全原则：宁可任务失败，不可数据外泄）。[[Codex CLI|Codex]] Cloud 的两阶段模型：setup 阶段允许网络（安装依赖），agent 阶段禁止网络（执行任务）——依赖就绪后 agent 在离线状态运行。

## 与 ExecPolicy 的协同

```
命令 → ExecPolicy（意图过滤）
         ├── forbidden → 直接拒绝
         ├── prompt → 等人类审批
         └── allow → 进入 OS 沙箱（能力约束）
                       ↓
                  内核层强制执行（无法绕过）
```

**ExecPolicy 是意图过滤器，Sandbox 是能力约束器**。两者各自独立，协同工作。

## 调试工具

```bash
codex sandbox macos --log-denials curl https://example.com
codex sandbox linux cat /etc/passwd
codex execpolicy check --rules ~/.codex/rules.toml git push --force
```

## 来源

- [[raw/articles/ai-tools/codex/03_codex_sandbox_system.md]]
