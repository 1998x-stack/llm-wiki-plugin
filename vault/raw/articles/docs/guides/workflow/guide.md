# UrhoX Claude Code 工作流

本目录包含 UrhoX 项目的 Claude Code 工作流配置，用于自动化代码审查、格式化和 Git 操作。

## 📁 目录结构

```
.claude/
├── CLAUDE.md              # 项目核心上下文和规范（Claude Code 必读）
├── README.md              # 本文件
├── settings.json          # Hook 配置
├── agents/                # AI 智能代理
│   ├── code-reviewer.md         # C++ 代码审查代理
│   ├── git-commit-generator.md  # Git commit 生成代理
│   └── tech-design-reviewer.md  # 技术设计审查代理
├── commands/              # 快捷命令
│   ├── git-commit.md           # 生成 commit
│   ├── create-pr.md            # 创建 PR
│   ├── merge-pr.md             # 合并 PR
│   ├── create-code-review.md   # 创建代码审查
│   ├── apply-code-review.md    # 应用审查建议
│   ├── check-code-review.md    # 检查审查完成度
│   ├── apply-pr-reviews.md     # 应用 PR 审查
│   └── git-merge.md            # 合并分支
└── hooks/                 # 自动化钩子
    └── format-code.py          # 代码自动格式化
```

---

## 🚀 快速开始

### 前置要求

1. **Claude Code**: 确保已安装 Claude Code（Cursor 内置）
2. **GitHub CLI**: 安装 `gh` 命令行工具
3. **格式化工具**（可选，但推荐）:
   - `clang-format`: C++ 代码格式化
   - `lua-format`: Lua 代码格式化（可选）
   - `cmake-format`: CMake 文件格式化（可选）
   - `black`: Python 代码格式化（可选）

### 安装格式化工具

**Windows**:
```powershell
# 使用 scoop 安装
scoop install llvm  # 包含 clang-format

# 或使用 pip 安装
pip install clang-format lua-format cmake-format black
```

**macOS**:
```bash
brew install clang-format lua-format cmake-format black
```

**Linux**:
```bash
sudo apt install clang-format  # 或 yum/dnf
pip install lua-format cmake-format black
```

---

## 📝 命令使用

### Git 工作流

#### 1. 提交代码

```
/git-commit [issue_id]
```

自动生成符合 Gitmoji + Conventional Commits 规范的 commit 消息。

**示例**:
```
/git-commit 123
```

生成的 commit message:
```
✨ feat(graphics): add deferred rendering pipeline (#123)

- ✨ implement G-buffer generation pass
- ⚡️ optimize light accumulation
- ✅ add unit tests

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 2. 创建 Pull Request

```
/create-pr
```

从当前分支创建 PR 到 `main` 分支，自动生成中文描述。

#### 3. 合并 Pull Request

```
/merge-pr <pr_number>
```

使用 merge commit 策略合并 PR（保留完整历史）。

#### 4. 合并分支

```
/git-merge <branch_name>
```

合并指定分支到当前分支，并生成规范的 merge commit message。

---

### Code Review 工作流

#### 1. 创建代码审查

```
/create-code-review <commit_sha>
```

对指定 commit 进行全面审查，自动创建 GitHub issue。

**审查维度**:
- ✅ C++ 代码质量（内存安全、性能、线程安全）
- ✅ 跨平台兼容性
- ✅ Lua API 设计（如适用）
- ✅ 架构设计
- ✅ 测试覆盖
- ✅ 文档完整性

**示例**:
```
/create-code-review abc123f
```

生成 issue:
```markdown
## Code Review: add deferred rendering

### 严重问题
- [ ] **[RenderPath.cpp:45]** 内存泄漏风险
  - 原因：SharedPtr 未正确释放
  - 影响：长时间运行可能内存耗尽
  - 建议：使用 RAII 模式管理资源

### 建议改进
- [ ] **[RenderPath.cpp:78]** 性能优化
  - 当前实现：每帧重新分配缓冲区
  - 更好方案：缓存并重用缓冲区
  - 收益：减少 30% 内存分配开销

### 认可的部分
- **Shader 管理**: 使用资源缓存模式，避免重复加载
```

#### 2. 应用审查建议

```
/apply-code-review <issue_id>
```

读取 code review issue，深度分析并应用建议：
- 自动分类问题（Critical/High/Medium/Low）
- 生成任务列表
- 逐一修复问题
- 提交 commit 并回复 issue

#### 3. 检查审查完成度

```
/check-code-review <issue_id>
```

验证所有问题是否已解决，决定是否关闭 issue。

#### 4. 应用 PR 审查

```
/apply-pr-reviews <pr_number>
```

批量处理 PR 中的所有 review comments：
- 过滤已处理的建议
- 深度分析未处理建议
- 应用修复
- 单独回复每条 comment
- 添加 reaction 和 resolve conversation

#### 5. 快速修复 Issue

```
/fix-issue <issue_id>
```

自动修复 GitHub issue 中描述的问题：
- 自动识别问题类型（CI 失败、Code Review、Bug 等）
- 执行相应的修复操作
- 提交修复并回复 issue

**示例**:
```bash
# 修复自动创建的 CI 失败 issue
/fix-issue 5

# 修复 bug 报告
/fix-issue 10

# 修复任何类型的 issue
/fix-issue 123
```

**自动处理的问题类型**:
- ✅ CI 检查失败（代码格式、CMake、Commit 消息）
- ✅ Code Review 建议（自动调用 apply-code-review）
- ✅ Bug 报告（定位并修复）
- ✅ 其他类型 issue（智能分析并修复）

---

## 🤖 Agents（智能代理）

### code-reviewer

精通 C++ 游戏引擎开发的代码审查专家。

**使用场景**:
- 用户完成功能开发后
- 需要深度技术审查时
- PR 合并前的质量把控

**特点**:
- ✅ C++ 特定检查（内存、性能、线程）
- ✅ 跨平台兼容性审查
- ✅ Lua API 设计评审
- ✅ 基于 Linus Torvalds "Good Taste" 哲学

### git-commit-generator

Git commit 消息生成专家。

**使用场景**:
- 暂存文件后需要提交
- 需要符合项目规范的 commit message

**特点**:
- ✅ Gitmoji + Conventional Commits
- ✅ 自动提取上下文（issue、历史 commits）
- ✅ 英文祈使语气，简洁精确

### tech-design-reviewer

技术方案和架构设计审查专家。

**使用场景**:
- GitHub issue 中提出技术方案
- 需要架构决策审查
- 评估设计文档

**特点**:
- ✅ Linus Torvalds 五层分析法
- ✅ 数据结构优先思维
- ✅ 务实主义 vs 理论完美
- ✅ 游戏引擎特定考量（性能、跨平台）

---

## 🔧 Hooks（自动化钩子）

### format-code.py

编辑文件后自动格式化。

**触发时机**: PostToolUse（Edit/Write 工具成功后）

**支持格式化**:
- **C++ 文件** (`.h`, `.hpp`, `.cpp`, `.cc`, `.cxx`): `clang-format`
- **Lua 文件** (`.lua`): `lua-format`（可选）
- **CMake 文件** (`CMakeLists.txt`, `*.cmake`): `cmake-format`（可选）
- **Python 文件** (`.py`): `black`（可选）

**特性**:
- ✅ 自动跳过第三方代码（`3rd/`, `ThirdParty/` 等）
- ✅ 工具不可用时优雅降级
- ✅ 非致命错误（格式化失败不阻塞工作流）

**配置**: 参见根目录 `.clang-format` 文件

---

## 📖 代码规范

### C++ 代码风格

详见 [CLAUDE.md - 代码规范](../../../CLAUDE.md#代码规范) 章节。

**核心要点**:
- **命名**: PascalCase（类/函数），camelCase_（成员变量）
- **缩进**: 4 空格，禁用 Tab
- **大括号**: Allman 风格（独立成行）
- **行宽**: 120 字符
- **注释**: 英文，解释 WHY

### Git Commit 规范

详见 [CLAUDE.md - Git Commit 规范](../../../CLAUDE.md#git-commit-规范) 章节。

**格式模板**:
```
<emoji> <type>(<scope>): <description> (#issue)

- <emoji> change 1
- <emoji> change 2

💥 BREAKING CHANGE:  # if applicable
- breaking change description

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**常用 Type**:
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构
- `perf`: 性能优化
- `docs`: 文档
- `test`: 测试
- `build`: 构建系统
- `chore`: 杂项

**常用 Scope**:
- `graphics`: 渲染系统
- `lua`: Lua 脚本
- `scene`: 场景管理
- `physics`: 物理系统
- `tools`: 开发工具
- `cmake`: 构建配置

---

## 🔍 最佳实践

### 1. 提交前格式化

虽然有自动 hook，但建议手动验证：

```bash
# C++ 文件
clang-format -i src/GameEngine.cpp

# Lua 文件
lua-format -i scripts/main.lua

# 批量格式化
find engine/Source -name "*.cpp" -o -name "*.h" | xargs clang-format -i
```

### 2. Code Review 流程

**开发者**:
1. 完成功能开发
2. `/git-commit` 提交代码
3. `/create-pr` 创建 PR
4. 等待 code review

**审查者** (Claude Code):
1. 自动或手动触发 `/create-code-review`
2. 生成详细 review report（GitHub issue）

**开发者**:
1. `/apply-code-review <issue_id>` 应用建议
2. 修复问题并提交
3. 回复 issue 说明修复情况

**审查者**:
1. `/check-code-review <issue_id>` 验证修复
2. 关闭 issue 或要求进一步修改

### 3. PR 合并策略

**默认**: Merge Commit（保留完整历史）
```bash
/merge-pr 123
```

**原因**:
- ✅ 保留完整开发历史
- ✅ 便于追溯功能开发过程
- ✅ 便于 cherry-pick 和 revert

**禁止** 使用 `--squash` 或 `--rebase`，除非有特殊理由。

### 4. 技术债务管理

未解决的建议记录到 `docs/guides/technical-debt.md`。

**记录条件**:
- ✅ 有明确收益（安全、性能、可维护性）
- ✅ 非紧急（不影响当前功能）
- ✅ 真实问题（非过度设计）

**优先级**:
- **P0**: Memory Safety、Thread Safety
- **P1**: Performance、跨平台兼容性
- **P2**: 代码质量改进
- **P3**: 长期架构改进

---

## 🛠️ 故障排除

### Hook 未生效

1. 检查 `settings.json` 是否正确
2. 确认 Python 在 PATH 中
3. 查看 Claude Code 输出日志

### 格式化工具不可用

Hook 会优雅降级，但建议安装所有工具以获得最佳体验：

```bash
# 检查工具是否可用
clang-format --version
lua-format --version
cmake-format --version
black --version
```

### GitHub CLI 认证问题

```bash
# 登录 GitHub
gh auth login

# 检查认证状态
gh auth status
```

---

## 📚 参考资料

- [Gitmoji](https://gitmoji.dev/) - Git commit emoji 指南
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit 消息规范
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) - C++ 格式化工具
- [Urho3D 代码风格](https://urho3d.github.io/documentation/HEAD/_coding_conventions.html) - Urho3D 编码规范

---

## 🤝 贡献

如需改进工作流配置，请：

1. 在 GitHub 创建 issue 讨论
2. 提交 PR 并说明改进理由
3. 更新相关文档

---

## 📄 许可证

本工作流配置遵循 UrhoX 项目的 MIT License。

---

*最后更新: 2025-10-27*

