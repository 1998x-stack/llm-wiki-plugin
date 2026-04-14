# UrhoX 完整自动化工作流说明

## 🎯 解决的两个核心问题

### ✅ 问题 1: Claude Code 自动审查

**之前**: 需要手动运行 `/create-code-review`  
**现在**: PR 创建后**自动触发** Claude API 审查

**实现方式**:
- 使用官方 `anthropics/claude-code-action@v1`
- 配置文件: `.github/workflows/claude-code-review.yml`
- 触发条件: PR 创建/更新，且变更 ≥50 行

**自动化流程**:
```
PR 创建
  ↓
claude-code-review.yml 自动运行
  ↓
调用 Claude API 审查代码
  ↓
自动创建 Code Review issue（中文）
  ├─ 严重问题（必须修复）
  ├─ 建议改进（可选优化）
  ├─ 认可的部分
  └─ 总体评价
  ↓
在 PR 中添加评论，引用 issue
```

### ✅ 问题 2: 检查失败自动创建 Issue

**之前**: 检查失败后需要手动复制错误信息  
**现在**: 自动创建包含完整错误的 issue

**实现方式**:
- 在 `pr-checks.yml` 添加 `create-fix-issue-on-failure` job
- 失败时自动收集错误信息
- 创建 issue 并分配给 PR 作者

**自动化流程**:
```
质量检查失败
  ↓
create-fix-issue-on-failure 运行
  ↓
创建 issue #XX
  ├─ 标题: 🔧 [Auto-Fix] PR #YY 质量检查失败
  ├─ 标签: auto-fix-needed, ci-failure
  ├─ 分配: PR 作者
  └─ 内容:
      ├─ 完整错误信息
      ├─ AI 修复建议
      └─ 手动修复步骤
  ↓
在 PR 中添加评论引用 issue
  ↓
开发者只需: "@claude 修复 issue #XX"
```

---

## 🤖 三层自动化架构

### 第一层：基础质量检查（1-2 分钟）

**Workflow**: `pr-checks.yml`

**检查项目**:
- ✅ 代码格式（clang-format）
- ✅ CMake 配置
- ✅ Commit 消息规范

**失败处理**:
- 🔧 自动创建修复 issue
- 💬 在 PR 中添加评论
- 🚫 阻止 PR 合并

### 第二层：AI 深度审查（2-5 分钟）

**Workflow**: `claude-code-review.yml`

**审查内容**:
- 🧠 C++ 代码质量（内存、性能、线程）
- 🌐 跨平台兼容性
- 🌙 Lua API 设计
- 🏗️ 架构设计

**输出**:
- 📋 详细 Code Review issue（中文）
- 💬 PR 评论（引用 issue）

**触发条件**:
- PR 创建/更新
- 非 draft PR
- 变更 ≥50 行

### 第三层：按需 AI 助手

**Workflow**: `claude.yml`

**触发方式**:
```bash
# 任何 issue/PR 评论中提到 @claude
@claude 请 review 这段代码
@claude 修复 issue #123
@claude 这个实现有性能问题吗？
```

**功能**:
- 🎯 针对性回答
- 🔧 可以直接执行修复
- 📖 可以读取代码和文档

---

## 📊 完整的 PR 生命周期

```
┌─────────────────────────────────┐
│ 1. 开发者创建 PR               │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ 2. GitHub Actions 自动运行      │
│                                 │
│  ├─ 基础检查 (pr-checks.yml)   │
│  │  ├─ 代码格式                │
│  │  ├─ CMake 配置              │
│  │  └─ Commit 消息             │
│  │                              │
│  ├─ 自动标签 (auto-label.yml)  │
│  │  └─ 添加模块和大小标签      │
│  │                              │
│  └─ Claude 审查 (claude-code-review.yml)
│     ├─ C++ 代码质量分析        │
│     ├─ 创建 review issue       │
│     └─ PR 中添加评论           │
└─────────────┬───────────────────┘
              │
              ├─ 检查通过 ────────┐
              │                   │
              └─ 检查失败         │
                  ↓               │
      ┌─────────────────┐         │
      │ 自动创建 issue  │         │
      │ - 完整错误信息  │         │
      │ - AI 修复建议   │         │
      └────────┬────────┘         │
               │                  │
               ▼                  │
      ┌─────────────────┐         │
      │ 开发者修复      │         │
      │ "@claude 修复   │         │
      │  issue #XX"     │         │
      └────────┬────────┘         │
               │                  │
               └──────────────────┤
                                  │
                                  ▼
                      ┌───────────────────┐
                      │ 3. 查看 review    │
                      │    issue          │
                      └──────┬────────────┘
                             │
                             ▼
                      ┌───────────────────┐
                      │ 4. 应用修复       │
                      │ /apply-code-review│
                      └──────┬────────────┘
                             │
                             ▼
                      ┌───────────────────┐
                      │ 5. 推送更新       │
                      │ git push          │
                      └──────┬────────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ 6. 重新触发检查和审查     │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │ 7. 所有通过，合并 PR      │
              │ /merge-pr <number>         │
              └────────────────────────────┘
```

---

## 🚀 快速开始

### 第一步：配置 API Key

```bash
# 在 GitHub 仓库设置中添加 secret
Settings → Secrets and variables → Actions → New repository secret
Name: ANTHROPIC_API_KEY
Value: <your-api-key>
```

### 第二步：创建 PR 测试

```bash
# 本地开发
git checkout -b feature/test
# ... 编写代码 ...
git add .
/git-commit
git push

# 创建 PR（会自动触发所有检查）
/create-pr
```

### 第三步：观察自动化

1. ✅ 基础检查运行（1-2 分钟）
2. ✅ Claude 审查运行（2-5 分钟）
3. ✅ 自动标签添加
4. ✅ 如果失败，自动创建 issue

### 第四步：使用 @claude

在任何 issue/PR 中:
```
@claude 请帮我 review 这个 PR
@claude 修复 issue #123
```

---

## 💡 实用技巧

### Tip 1: 跳过 Claude 审查

如果某个 PR 不需要 Claude 审查（如纯文档变更）：

```markdown
<!-- 在 PR 描述中添加 -->
[skip-claude-review]
```

（注：目前 workflow 已根据变更行数自动跳过小改动）

### Tip 2: 查看 Claude 审查进度

```bash
# 查看 workflow 运行状态
gh run list --workflow="Claude Code Review"

# 查看具体运行日志
gh run view <run_id>
```

### Tip 3: 手动触发 Claude 审查

如果 PR 已存在但想重新审查：

```bash
# 在 PR 评论中
@claude 请重新 review 这个 PR
```

### Tip 4: 修复自动创建的 issue

```bash
# 方式 1: 直接让 AI 修复
在 issue 中评论: @claude 修复这些问题

# 方式 2: 本地使用 Claude Code
查看 issue 内容
/apply-code-review <issue_id>
```

---

## ⚙️ 高级配置

### 自定义 Claude 审查范围

编辑 `.github/workflows/claude-code-review.yml`:

```yaml
# 调整触发条件
if: |
  github.event.pull_request.draft == false &&
  (github.event.pull_request.additions + github.event.pull_request.deletions) >= 100  # 改为 100 行
```

### 自定义审查重点

编辑 prompt 部分，调整审查维度和重点。

### 禁用某个检查

在 `.github/workflows/pr-checks.yml` 中注释掉不需要的 job。

---

## 🐛 故障排除

### Claude 审查没有触发

**可能原因**:
1. PR 变更 <50 行（自动跳过）
2. PR 是 draft 状态
3. `ANTHROPIC_API_KEY` 未配置

**解决方法**:
```bash
# 检查 API Key
Settings → Secrets and variables → Actions
确认 ANTHROPIC_API_KEY 存在

# 手动触发
@claude 请 review 这个 PR
```

### 检查失败但没创建 issue

**可能原因**:
1. Workflow 权限不足
2. 标签不存在（`auto-fix-needed`, `ci-failure`）

**解决方法**:
```bash
# 创建缺失的标签
bash .github/scripts/setup-labels.sh <owner/repo>

# 检查 workflow 权限
.github/workflows/pr-checks.yml 中的 permissions
```

### @claude 没有响应

**可能原因**:
1. `claude.yml` workflow 未启用
2. `ANTHROPIC_API_KEY` 未配置
3. 权限不足

**解决方法**:
```bash
# 检查 workflow 是否存在
gh workflow list | grep -i claude

# 检查最近的运行
gh run list --workflow=claude.yml
```

---

## 📚 相关文档

- [GitHub Workflows](../.github/WORKFLOWS.md) - GitHub 配置详解
- [完整指南](guide.md) - 所有功能说明
- [快速开始](quickstart.md) - 5 分钟上手

---

## 🎉 总结

现在你拥有三层全自动审查：

1. **基础检查** - 快速、自动、阻塞性
2. **AI 深度审查** - 自动创建 review issue
3. **按需助手** - @claude 随时可用

所有检查失败都会自动创建 issue，包含完整上下文供 AI 修复。再也不需要手动复制粘贴错误信息了！🚀

---

*最后更新: 2025-10-27*

