# UrhoX Claude Code 工作流配置总结

## ✅ 已完成配置

### 📁 目录结构

```
UrhoX/
├── .claude/                           # Claude Code 工作流配置
│   ├── CLAUDE.md                      # ✅ 项目核心上下文（Claude Code 必读）
│   ├── README.md                      # ✅ 完整使用文档
│   ├── QUICKSTART.md                  # ✅ 快速开始指南
│   ├── settings.json                  # ✅ Hook 配置
│   │
│   ├── agents/                        # ✅ AI 智能代理（3 个）
│   │   ├── code-reviewer.md           # - C++ 代码审查专家
│   │   ├── git-commit-generator.md    # - Git commit 生成专家
│   │   └── tech-design-reviewer.md    # - 技术设计审查专家
│   │
│   ├── commands/                      # ✅ 快捷命令（8 个）
│   │   ├── git-commit.md              # - 生成规范 commit
│   │   ├── create-pr.md               # - 创建 Pull Request
│   │   ├── merge-pr.md                # - 合并 Pull Request
│   │   ├── create-code-review.md      # - 创建代码审查 issue
│   │   ├── apply-code-review.md       # - 应用审查建议
│   │   ├── check-code-review.md       # - 检查审查完成度
│   │   ├── apply-pr-reviews.md        # - 应用 PR 审查
│   │   └── git-merge.md               # - 合并分支
│   │
│   └── hooks/                         # ✅ 自动化钩子（1 个）
│       └── format-code.py             # - 代码自动格式化
│
├── .clang-format                      # ✅ C++ 代码风格配置（Urho3D 风格）
└── docs/
    └── technical-debt.md              # ✅ 技术债务追踪文档
```

---

## 🎯 核心功能

### 1. 自动化 Git 工作流

✅ **自动生成规范的 commit message**
- Gitmoji + Conventional Commits
- 英文祈使语气
- 自动提取 issue 上下文
- 使用 heredoc 格式避免转义问题

✅ **PR 管理**
- 自动生成中文 PR 描述
- Merge commit 策略（保留完整历史）
- 规范的 merge commit message

### 2. C++ 代码审查

✅ **全面的代码质量审查**
- 内存安全（泄漏、野指针、未初始化变量）
- 性能分析（热路径、内存分配、缓存友好性）
- 线程安全（数据竞争、锁机制、死锁）
- 跨平台兼容性（平台 API、字节序、编译器差异）
- Lua API 设计（类型安全、错误处理、易用性）

✅ **基于 Linus Torvalds "Good Taste" 哲学**
- 数据结构优先思维
- 消除特殊情况
- 务实主义 vs 理论完美
- 简洁性原则（>3 层缩进 = 重新设计）

### 3. 代码自动格式化

✅ **多语言格式化支持**
- C++ 文件：clang-format（Allman 风格，4 空格缩进）
- Lua 文件：lua-format
- CMake 文件：cmake-format
- Python 文件：black

✅ **智能跳过第三方代码**
- 自动识别 `3rd/`、`ThirdParty/` 等目录
- 工具不可用时优雅降级

### 4. 技术债务管理

✅ **结构化债务追踪**
- P0-P3 优先级分类
- 明确的记录条件和格式
- 已解决债务归档

---

## 🚀 立即开始

### 第一步：安装依赖

```bash
# 必需：GitHub CLI
gh auth login

# 推荐：格式化工具
# Windows
scoop install llvm
pip install lua-format cmake-format black

# macOS
brew install clang-format lua-format cmake-format black
```

### 第二步：试用命令

```bash
# 1. 修改一些代码
# 2. 暂存变更
git add .

# 3. 生成 commit
/git-commit

# 4. 推送
git push
```

### 第三步：查看文档

- [快速开始指南](quickstart.md) - 5 分钟上手
- [完整指南](guide.md) - 所有功能详解
- [项目规范](../../../CLAUDE.md) - 代码规范和上下文

---

## 📊 配置对比

### vs 原始 `code` 项目配置

| 功能 | code 项目 | UrhoX 项目 | 说明 |
|------|-----------|------------|------|
| **代码审查** | TypeScript/JavaScript | C++ 游戏引擎 | ✅ 适配 C++ 特性 |
| **格式化工具** | ESLint + Prettier | clang-format | ✅ 适配 C++ 工具链 |
| **Linter** | ESLint | 无（C++ 静态分析可选） | ✅ C++ 项目特点 |
| **审查维度** | 6 维 | 8 维 | ✅ 增加跨平台和 Lua API |
| **Web 相关命令** | 有（fake-login 等） | 无 | ✅ 移除不相关功能 |
| **Commit 规范** | 相同 | 相同 | ✅ 保留最佳实践 |
| **PR 策略** | Merge commit | Merge commit | ✅ 保留最佳实践 |

---

## 🎨 代码风格亮点

### C++ 风格（符合 Urho3D 规范）

```cpp
// 命名规范
class StaticModel;              // PascalCase（类名）
void GetComponent();            // PascalCase（函数名）
Vector3 position_;              // camelCase_（成员变量）
const int MAX_TEXTURE_UNITS;    // UPPER_SNAKE_CASE（常量）

// Allman 风格大括号
void Update()
{
    if (condition)
    {
        // 代码
    }
}

// 4 空格缩进，禁用 Tab
void Process()
{
    for (auto item : items)
    {
        ProcessItem(item);
    }
}
```

### Git Commit 风格

```
✨ feat(graphics): implement BGFX deferred rendering (#123)

- ✨ add G-buffer generation pass
- ⚡️ optimize light accumulation with compute shader
- 🐛 fix texture sampling artifacts
- ✅ add unit tests for render pipeline

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 🔧 配置文件说明

### `.claude/CLAUDE.md`
**用途**: Claude Code 的"大脑"，包含项目所有上下文和规范  
**内容**:
- 项目概述和技术栈
- C++ 代码规范（命名、格式、注释）
- Git commit 规范（Gitmoji + Conventional Commits）
- Code review 标准（8 维审查）
- PR 合并策略
- 语言使用规范

### `.claude/settings.json`
**用途**: Hook 配置，启用自动格式化  
**内容**:
- PostToolUse hook（编辑文件后触发）
- 调用 `format-code.py` 脚本

### `.clang-format`
**用途**: C++ 代码格式化配置  
**风格**:
- BasedOnStyle: LLVM
- BraceWrapping: Allman（大括号独立成行）
- IndentWidth: 4
- ColumnLimit: 120
- Standard: c++17

### `docs/guides/technical-debt.md`
**用途**: 追踪已知但未解决的技术问题  
**分类**:
- P0 (Critical): Memory/Thread Safety
- P1 (Important): Performance/跨平台
- P2 (Nice to Have): 代码质量
- P3 (Future): 长期架构

---

## 📝 使用示例

### 示例 1: 日常开发提交

```
开发者: "我完成了延迟渲染管线的实现，帮我提交"

Claude Code:
1. 运行 git diff --cached
2. 生成 commit message
3. 执行 git commit
4. 显示成功信息

开发者: git push
```

### 示例 2: 创建和审查 PR

```
开发者: "创建 PR"

Claude Code:
- 分析所有变更
- 生成中文描述
- 创建 PR #123

开发者: "review PR 123 的代码"

Claude Code:
1. 提取 PR 的所有变更
2. 全面审查（内存、性能、线程、跨平台）
3. 创建详细 review issue #456

开发者: "应用 review #456 的建议"

Claude Code:
1. 深度分析建议（Linus 思维模式）
2. 生成任务列表
3. 逐一修复
4. 提交 commit（引用 #456）
5. 回复 issue
```

### 示例 3: 自动格式化

```
开发者: （使用 Claude Code 编辑 RenderPath.cpp）

Claude Code:
- 保存文件
- 触发 PostToolUse hook
- 运行 clang-format -i RenderPath.cpp
- 自动格式化完成
```

---

## ✨ 独特优势

### 1. 为 C++ 游戏引擎量身定制

❌ **不适合**:
- TypeScript/JavaScript 项目的 ESLint 规则
- Web 开发的认证流程

✅ **专门优化**:
- C++ 内存安全审查
- 游戏引擎性能分析
- 跨平台兼容性检查
- Lua API 设计评审

### 2. 基于 Urho3D 架构

- 遵循 Urho3D 代码风格（Allman、PascalCase）
- 理解 Urho3D 组件模型
- 熟悉资源缓存机制
- 支持 Lua 脚本绑定

### 3. AI 友好设计

- Lua API 命名清晰（避免缩写）
- 参数顺序直观
- 类型检查完善
- 文档示例丰富

---

## 🔮 未来扩展

### 可选增强（按需添加）

1. **静态分析集成**
   - clang-tidy（C++ 静态分析）
   - cppcheck（C++ 缺陷检测）

2. **性能分析**
   - 自动运行性能基准测试
   - 检测性能退化

3. **跨平台测试**
   - 自动触发多平台 CI/CD
   - 平台特定代码审查

4. **Lua API 文档生成**
   - 自动从 C++ 绑定生成 Lua 文档
   - AI 友好的 API 描述

---

## 🙏 致谢

本配置基于 `code` 项目的最佳实践，针对 UrhoX C++ 游戏引擎项目进行了深度定制。

**核心理念**:
- Linus Torvalds 的"Good Taste"哲学
- 务实主义优于理论完美
- 简洁性和可维护性优先

---

## 📞 支持

遇到问题？

1. 查看 [快速开始指南](quickstart.md)
2. 查看 [完整指南](guide.md)
3. 创建 GitHub issue
4. 联系团队

---

**配置已就绪，开始使用 Claude Code 提升开发效率！🚀**

*配置时间: 2025-10-27*  
*配置版本: v1.0*

