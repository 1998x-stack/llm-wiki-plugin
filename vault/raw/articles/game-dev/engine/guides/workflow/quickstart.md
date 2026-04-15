# UrhoX Claude Code 快速开始指南

## 🎯 5 分钟快速上手

### 1️⃣ 安装依赖

**必需**:
```bash
# GitHub CLI（用于自动化 PR 和 issue 管理）
# Windows (scoop)
scoop install gh

# macOS
brew install gh

# Linux
# 参考 https://github.com/cli/cli#installation
```

**可选但推荐**（用于代码格式化）:
```bash
# Windows
scoop install llvm  # 包含 clang-format
pip install lua-format cmake-format black

# macOS
brew install clang-format lua-format cmake-format black

# Linux
sudo apt install clang-format  # 或 yum/dnf
pip install lua-format cmake-format black
```

### 2️⃣ GitHub 认证

```bash
gh auth login
```

按提示选择：
- GitHub.com
- HTTPS
- Login with a web browser

### 3️⃣ 验证配置

```bash
# 检查 GitHub CLI
gh auth status

# 检查格式化工具
clang-format --version
```

---

## 🚀 常见工作流

### 工作流 1: 日常开发提交

```
┌─────────────────┐
│  1. 编写代码    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. git add .    │  暂存变更
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. /git-commit  │  生成规范的 commit
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. git push     │  推送到远程
└─────────────────┘
```

**示例对话**:
```
你: "我完成了 BGFX 渲染管线的实现，帮我提交代码"

Claude Code:
1. 运行 git diff --cached 查看变更
2. 生成 commit message:
   ✨ feat(graphics): implement BGFX rendering pipeline
   
   - ✨ add deferred rendering pass
   - ⚡️ optimize shader compilation
   - ✅ add unit tests for render path
   
   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>
3. 执行 git commit
4. 显示 commit 成功信息
```

### 工作流 2: 创建和合并 PR

```
┌──────────────────┐
│ 1. 完成功能开发  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. /create-pr    │  创建 Pull Request
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. 等待 review   │  （可选：手动触发 code review）
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 4. /merge-pr XX  │  合并 PR
└──────────────────┘
```

**示例对话**:
```
你: "功能已完成，创建 PR"

Claude Code:
1. 分析当前分支的所有变更
2. 生成中文 PR 描述:
   ## 变更概述
   - 实现 BGFX 延迟渲染管线
   - 优化 shader 编译流程
   - 添加单元测试
   
   ## 测试计划
   - [ ] Windows DX11 渲染测试
   - [ ] Linux OpenGL 渲染测试
   - [ ] 性能基准测试
3. 创建 PR #123
4. 输出 PR URL
```

```
你: "合并 PR 123"

Claude Code:
1. 检查 PR 状态（CI/CD）
2. 生成 merge commit message
3. 执行 gh pr merge 123 --merge
4. 确认合并成功
```

### 工作流 3: 完整 Code Review 流程

```
┌─────────────────────┐
│ 1. 提交代码         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. /create-code-    │  创建代码审查
│    review <sha>     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. 查看生成的       │  GitHub Issue
│    review report    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. /apply-code-     │  应用审查建议
│    review <issue>   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. /check-code-     │  检查修复完成度
│    review <issue>   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 6. 关闭 issue       │  （自动或手动）
└─────────────────────┘
```

**示例对话**:
```
你: "review 我最新的 commit"

Claude Code:
1. 运行 git show HEAD 获取变更
2. 全面审查代码（C++、内存、性能、线程安全）
3. 创建 GitHub issue #234:
   
   ## Code Review: implement BGFX pipeline
   
   ### 严重问题
   - [ ] **[RenderPath.cpp:123]** 内存泄漏风险
     SharedPtr 未正确释放
   
   ### 建议改进
   - [ ] **[Shader.cpp:45]** 性能优化
     缓存 shader 编译结果
   
   ### 认可的部分
   - **资源管理**: 正确使用 ResourceCache
   
4. 输出 issue URL
```

```
你: "应用 code review #234 的建议"

Claude Code:
1. 读取 issue #234
2. 深度分析（Linus Torvalds 思维模式）
3. 生成任务列表:
   ✅ Critical: 修复内存泄漏
   ⚠️ Medium: 优化 shader 缓存
4. 逐一执行修复
5. 提交 commit（引用 #234）
6. 回复 issue 说明修复情况
```

---

## 📋 命令速查表

| 命令 | 用途 | 示例 |
|------|------|------|
| `/git-commit [issue]` | 生成 commit | `/git-commit 123` |
| `/create-pr` | 创建 PR | `/create-pr` |
| `/merge-pr <pr>` | 合并 PR | `/merge-pr 456` |
| `/create-code-review <sha>` | 创建代码审查 | `/create-code-review abc123f` |
| `/apply-code-review <issue>` | 应用审查建议 | `/apply-code-review 789` |
| `/check-code-review <issue>` | 检查审查完成 | `/check-code-review 789` |
| `/apply-pr-reviews <pr>` | 应用 PR 审查 | `/apply-pr-reviews 456` |
| `/git-merge <branch>` | 合并分支 | `/git-merge feature/new-render` |
| `/fix-issue <issue>` | 自动修复 issue | `/fix-issue 123` |

---

## 💡 实用技巧

### Tip 1: 批量格式化代码

虽然有自动 hook，但有时需要批量格式化：

```bash
# 格式化所有 C++ 文件
find engine/Source -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# 仅格式化 git 跟踪的文件
git ls-files '*.cpp' '*.h' | xargs clang-format -i
```

### Tip 2: 检查 commit 规范

在提交前验证 commit message：

```bash
# 查看最近的 commits 风格
git log --oneline -10

# 查看完整 commit message
git log -1 --pretty=format:"%B"
```

### Tip 3: 跳过自动格式化

如果需要暂时禁用 hook：

```bash
# 设置环境变量
export CLAUDE_HOOK_DRY_RUN=1  # Linux/macOS
$env:CLAUDE_HOOK_DRY_RUN="1"  # Windows PowerShell
```

或直接编辑 `.claude/settings.json`，临时禁用 hook。

### Tip 4: 自定义 code review 深度

Code review 默认全面审查。如果只需检查特定方面：

```
你: "只 review 一下这个 commit 的内存安全问题"

Claude Code:
（会聚焦内存安全审查）
```

### Tip 5: PR 描述模板

创建 PR 时，Claude Code 会自动生成描述。如需自定义：

```
你: "创建 PR，重点说明性能改进"

Claude Code:
（会在描述中强调性能相关变更）
```

---

## ⚠️ 常见问题

### Q: Hook 没有自动格式化？

**A**: 检查：
1. `settings.json` 配置是否正确
2. Python 是否在 PATH 中
3. 格式化工具是否已安装（`clang-format --version`）

### Q: commit message 格式不符合要求？

**A**: 使用 `/git-commit` 命令而非手动编写。如需修改已提交的 commit：
```bash
git commit --amend
```

### Q: GitHub CLI 认证失败？

**A**: 重新认证：
```bash
gh auth logout
gh auth login
```

### Q: Code review 生成的 issue 太详细？

**A**: 这是特性，不是 bug。详细的 review 有助于提高代码质量。可以选择性应用建议。

### Q: 如何禁用某个文件的格式化？

**A**: 在文件中添加注释：
```cpp
// clang-format off
// 你的代码
// clang-format on
```

---

## 📚 进阶学习

- [完整指南](guide.md) - 所有功能的详细说明
- [配置总结](setup.md) - 配置细节和对比
- [项目规范](../../../CLAUDE.md) - 代码规范和上下文
- [Gitmoji](https://gitmoji.dev/) - Emoji 使用指南
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit 规范

---

## 🆘 获取帮助

遇到问题？

1. 查看 [完整指南](guide.md)
2. 查看 [故障排除](guide.md#故障排除) 章节
3. 在 GitHub 创建 issue
4. 联系团队成员

---

**祝你开发愉快！🚀**

*最后更新: 2025-10-27*

