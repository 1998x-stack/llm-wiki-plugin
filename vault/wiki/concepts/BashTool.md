---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI工具, 代码助手, 智能体系统, 安全机制, AI工程]
aliases: ["BashTool", "Bash Security"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Tool System]]"
    type: part_of
  - target: "[[bashSecurity.ts]]"
    type: implements
supersedes: null
---

# BashTool

## 概述
[[Claude Code]]中最重要也最危险的工具，允许AI Agent执行任意Shell命令，具有严密的安全机制以保障系统安全。

## 关键内容
1. **安全检查机制**：包含23项按序执行的安全检查，构成完整的命令行安全专用威胁模型。

2. **威胁模型分类**：
   - 命令黑名单：拦截rm -rf /、dd if=/dev/zero of=/dev/sda、mkfs.*、fdisk /dev/等危险命令
   - Zsh特有威胁：专门针对Zsh的威胁模型，拦截18个Zsh特有内建命令，包括Zsh等号展开攻击（=curl在Zsh中等价于$(which curl)）和IFS空字节注入
   - Unicode安全：防范零宽字符注入（Unicode零宽空格U+200B）和双向控制字符（RTL override）等欺骗手段
   - 管道与重定向分析：对复合命令递归分析每个管道段和重定向目标，确保所有子命令都通过安全检查

3. **[[Permissions|权限]]三级体系**：
   - Level 3：自动执行只[[Read|读操作]]、低风险命令（ls, cat, git status等）
   - Level 2：单次确认[[Write|写操作]]、网络请求、文件删除等，每次执行前询问用户
   - Level 1：永久拒绝或需要特殊授权系统级操作、危险命令（rm -rf, dd, 格式化磁盘等）

4. **执行环境**：每个Bash命令都在独立的子进程中执行，配备执行超时（防止无限挂起）、输出大小限制（防止输出溢出）和进程组管理（确保子进程被正确清理）。

## 来源
- [[Claude Code 源码泄露深度解析（二）：核心 Agent 引擎与 40+ 工具系统]] — 全文

## 相关
- [[Claude Code]] — part_of
- [[Tool System]] — part_of
- [[bashSecurity.ts]] — implements
- [[Zsh]] — relates_to