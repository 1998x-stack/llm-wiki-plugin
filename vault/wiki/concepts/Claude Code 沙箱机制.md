---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-security, agent-safety, claude-code]
aliases: [Sandboxing, Claude Code Sandboxing, 沙箱]
relates_to:
  - Claude Code: part_of
  - AI Agent 架构模式: implements
  - 提示工程: compares_to
supersedes: null
---

# Claude Code 沙箱机制

## 概述
Claude Code 沙箱机制是通过 OS 级别的系统调用过滤和资源隔离，在安全性与自主性之间取得平衡的安全基础设施，使 Agent 能在预定义范围内自主工作而无需用户逐操作审批。

## 关键内容

1. **设计哲学转变**：从"逐操作审批"（用户作为实时监督者）转向"授权范围 + 沙箱"（用户作为范围定义者）。会话开始时用户定义工作范围，沙箱保证范围内操作安全，Claude Code 在此范围内自主工作。

2. **分层安全架构**：用户进程（Claude Code）→ 受限系统调用接口 → 沙箱层（系统调用过滤）→ 受控资源访问 → OS 内核。三层隔离确保即使上层被绕过，底层仍有约束。

3. **文件系统隔离**：允许访问项目目录、临时目录、只读系统路径；禁止访问主目录根、系统目录（/etc/、/var/）、其他用户目录、SSH 密钥和密码文件等敏感路径。

4. **网络访问控制**：默认禁止任意外部网络请求和内部网络扫描；仅允许指定包管理器仓库（npm、pypi、cargo）、Anthropic API 和用户显式白名单的域名。

5. **进程控制**：允许生成子进程（测试、编译）和项目目录下的 git 操作；子进程继承父进程沙箱限制；禁止 setuid/setgid 权限提升、修改网络接口、访问原始设备。

6. **三种操作类别**：
   - 类别 A（完全沙箱内，无需审批）：读写项目文件、运行测试、npm/pip install、git commit/push
   - 类别 B（需要一次性确认）：访问项目外文件、新域名网络请求、安装系统级软件
   - 类别 C（始终禁止）：修改系统配置、访问密钥/凭证、向非白名单服务发送数据

7. **提示注入防御**：沙箱在系统层提供注入防御的最后一道防线。即使 Claude 被恶意文件中的注入指令欺骗，网络请求、系统文件修改、跨项目访问等操作仍会被沙箱拦截。

8. **与 Auto Mode 的协同**：形成纵深防御（Defense in Depth）。Auto Mode 分类器在语义层阻止"超出任务范围"的操作，沙箱在系统层阻止"不被允许的系统调用"。两层叠加实现纵深防御。

9. **性能影响**：文件访问 < 5% 开销，进程启动 ~10ms 额外延迟，网络请求 < 1% 开销，对交互式使用几乎不可感知。

## 来源
- [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) — Anthropic Engineering Blog, 2025 年 10 月 20 日

## 相关
- [[Claude Code]] — part_of
- [[AI Agent 架构模式]] — implements
- [[纵深防御]] — implements
- [[提示注入防御]] — prevents
- [[权限模型]] — supersedes
