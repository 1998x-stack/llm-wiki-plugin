# UrhoX System Prompts
# UrhoX 系统提示词

System prompts for AI-assisted UrhoX game development.

用于 AI 辅助 UrhoX 游戏开发的系统提示词。

---

## 📁 File Structure 文件结构

Each system prompt has **3 versions** 每个系统提示词有 **3 个版本**:

1. **`.en.md`** - Pure English (For LLM use) 纯英文版本（供 LLM 使用）
   - Clean, concise, no translation overhead
   - Optimized for token efficiency
   - **Use this in production**

2. **`.zh.md`** - Pure Chinese (For team reference) 纯中文版本（供团队参考）
   - Complete Chinese translation
   - For human team members to read
   - **Use this for documentation**

3. **`.md`** - Bilingual (Original, kept for reference) 双语版本（原始文件，保留作参考）
   - Both English and Chinese
   - Kept as source of truth
   - Not recommended for LLM use (token inefficient)

**Recommendation 推荐**:
- 🤖 **For LLMs**: Use `.en.md` files
- 👥 **For humans**: Use `.zh.md` files
- 📚 **For editing**: Edit `.md` files, then regenerate `.en.md` and `.zh.md`

---

## 📂 Available Prompts 可用提示词

### 1. Game Planning for TapCode - 游戏策划（TapCode 工作流）

**Files 文件**:
- [game-planning-for-tapcode.en.md](game-planning-for-tapcode.en.md) - English (For LLM) 英文版（供 LLM 使用）⭐
- [game-planning-for-tapcode.zh.md](game-planning-for-tapcode.zh.md) - Chinese (For team) 中文版（供团队参考）
- [game-planning-for-tapcode.md](game-planning-for-tapcode.md) - Bilingual (Source) 双语版（原始文件）
**Mode**: Plan Mode (TapCode Workflow)
**Purpose**: Help users plan and initialize UrhoX game projects with optimal workflow
**用途**: 帮助用户使用最优工作流规划和初始化 UrhoX 游戏项目

**Key Features 核心特性**:
- 🚀 **Auto environment setup** using MCP `create_project` tool
- 🎯 **Complexity assessment**: Simple vs Complex projects
- ⚡ **Fast track for simple projects**: Skip planning, start coding immediately
- 📖 **Full documentation for complex projects**: GDD, Architecture, Requirements, Progress
- 📁 **memory/ folder tracking**: All docs stored in `memory/` folder

**Use when 使用场景**:
- Starting a new game project
- User has game idea (simple or complex)
- Need environment setup
- Need to assess project complexity
- 开始新游戏项目
- 用户有游戏想法（简单或复杂）
- 需要环境搭建
- 需要评估项目复杂度

**Output for Simple Projects 简单项目输出**:
- Environment setup (MCP call)
- Quick tech stack selection
- Immediate coding (no detailed planning)

**Output for Complex Projects 复杂项目输出**:
- Environment setup (MCP call)
- `memory/gdd.md` - Game Design Document
- `memory/architecture.md` - UrhoX technical architecture
- `memory/requirements.md` - Implementation steps & test plans (NO code)
- `memory/progress.md` - Progress tracking

---

### 2. Game Development - 游戏开发

**Files 文件**:
- [game-development.en.md](game-development.en.md) - English (For LLM) 英文版（供 LLM 使用）⭐
- [game-development.zh.md](game-development.zh.md) - Chinese (For team) 中文版（供团队参考）
- [game-development.md](game-development.md) - Bilingual (Source) 双语版（原始文件）

**Mode**: Development Mode
**Purpose**: Guide AI in writing UrhoX Lua game code efficiently
**用途**: 指导 AI 高效编写 UrhoX Lua 游戏代码

**Use when 使用场景**:
- Requirements are clear, ready to code
- Implementing features
- Debugging issues
- Optimizing performance
- 需求明确，准备编码
- 实现功能
- 调试问题
- 优化性能

**Output 输出**:
- Production-quality Lua code
- Following UrhoX best practices
- Avoiding common pitfalls
- With extensive logging (initial delivery)
- 生产级 Lua 代码
- 遵循 UrhoX 最佳实践
- 避免常见陷阱
- 包含详尽日志（首次交付）

---

## 🎯 Usage Guide 使用指南

### Typical Workflow (TapCode) 典型工作流

#### Simple Project (e.g., Flappy Bird) 简单项目
```
1. User: "I want to make a game like Flappy Bird"
   → Use: game-planning-for-tapcode.md

2. Agent:
   - Calls mcp__sce_project_manager__create_project
   - Assesses: Simple project ✓
   - Quick planning (scaffold + examples)
   - Switches to: game-development.md
   - Starts coding immediately

3. Result: Working game in ~1 hour
```

#### Complex Project (e.g., RPG) 复杂项目
```
1. User: "I want to make an RPG with inventory, quests, and combat"
   → Use: game-planning-for-tapcode.md

2. Agent:
   - Calls mcp__sce_project_manager__create_project
   - Assesses: Complex project ✓
   - Asks clarifying questions
   - Creates memory/gdd.md
   - Creates memory/architecture.md
   - Creates memory/requirements.md
   - Creates memory/progress.md

3. User approves documentation
   → Agent switches to: game-development.md
   → Implements Phase 1 (MVP)

4. After each feature:
   - Test against requirements.md
   - Update progress.md
   - Continue to next feature

5. Result: Well-documented, tracked development process
```

### Integration with Claude Code Claude Code 集成

**Option 1: Direct Paste (Temporary) 直接粘贴（临时）**
```
1. Copy content from .en.md files (for LLM) or .zh.md files (for reading)
2. Paste at the start of conversation with Claude Code
3. Proceed with game development
```

**Option 2: Custom Instructions (Persistent) 自定义指令（持久）**
```
1. Go to Claude Code settings
2. Add system prompt from .en.md file (English for LLM)
3. Prompt applies to all future conversations
```

**Option 3: Slash Commands (Recommended for TapCode) 斜杠命令（TapCode 推荐）⭐**
```
# In .claude/commands/
plan-game-tapcode.md    → Contains game-planning-for-tapcode.en.md content
develop-game.md         → Contains game-development.en.md content

# Usage:
/plan-game-tapcode      → Activate TapCode planning mode
/develop-game           → Activate development mode
```

**Important 重要**: Always use `.en.md` files for LLM prompts to optimize token usage!
**重要**：始终使用 `.en.md` 文件作为 LLM 提示词，以优化 token 使用！

---

## 📋 Prompt Comparison 提示词对比

| Aspect | game-planning-for-tapcode.md | game-development.md |
|--------|------------------------------|---------------------|
| **Focus** | Setup + Complexity assessment + Planning | Code implementation |
| **Mode** | Plan Mode (TapCode) | Development Mode |
| **First Step** | MCP create_project call | Read documentation |
| **Simple Projects** | Skip planning, start coding | Implement features |
| **Complex Projects** | Full documentation (GDD, Architecture, Requirements) | Implement per requirements |
| **Questions** | Many (for complex), Few (for simple) | Few (assumes clarity) |
| **Output** | Design docs OR quick start | Working code |
| **Scope** | Adaptive (simple vs complex) | Narrow (specific features) |
| **Documentation** | Creates in memory/ folder | References from engine-docs/ |
| **Timeline** | Define phases (complex only) | Implement now |

---

## 🔄 When to Switch 何时切换

### From Planning to Development 从策划到开发
Switch when:
- ✅ Environment setup complete (MCP call done)
- ✅ **Simple project**: Immediately after complexity assessment
- ✅ **Complex project**: After documentation approved by user
- ✅ User says "let's start coding"

### From Development to Planning 从开发回到策划
Switch when:
- ⚠️ Major feature addition (needs design)
- ⚠️ Scope creep detected
- ⚠️ User says "I want to add..." (major change)
- ⚠️ Technical approach needs reconsideration
- ⚠️ Need to update GDD or architecture documents

---

## 📖 Related Resources 相关资源

**Documentation 文档**:
- `../engine-docs/principles.md` - Development principles
- `../engine-docs/lua-scripting-guide.md` - Lua scripting guide
- `../engine-docs/index.md` - Documentation index

**Examples 示例**:
- `../examples/` - Working game examples
- `../examples/api-index.md` - Find examples by API

**Templates 模板**:
- `../templates/scaffold-2d.lua` - Pure 2D game scaffold
- `../templates/scaffold-2d-physics.lua` - 2D physics game scaffold
- `../templates/scaffold-3d-scene.lua` - 3D scene showcase scaffold (free camera, no character)
- `../templates/scaffold-3d-character.lua` - 3D character game scaffold (Fall Guys, Roblox style)

**Entry Point 入口**:
- `../claude.md` - Main AI entry point (navigation hub)

---

## ✏️ Customization 自定义

These prompts are designed to be customizable. You can:

这些提示词设计为可自定义的。你可以：

1. **Add project-specific rules 添加项目特定规则**
   - Insert after "## CRITICAL RULES"
   - Example: "Always use specific art style"

2. **Modify output format 修改输出格式**
   - Change design document structure
   - Add/remove sections

3. **Add custom examples 添加自定义示例**
   - Reference your own game code
   - Share team conventions

4. **Adjust verbosity 调整详细程度**
   - More/less explanation
   - More/less code comments

---

## 🎓 Best Practices 最佳实践

### For Planning Mode (TapCode) 策划模式
- ✅ **ALWAYS call MCP create_project first**
- ✅ Assess complexity immediately (simple vs complex)
- ✅ **Simple projects**: Skip detailed planning, start coding
- ✅ **Complex projects**: Create full documentation in memory/
- ✅ Ask clarifying questions (for complex projects)
- ✅ Push for MVP first
- ✅ Reference concrete examples
- ❌ Don't over-plan simple projects
- ❌ Don't under-plan complex projects

### For Development Mode 开发模式
- ✅ Always read documentation first
- ✅ Use scaffolds, never start from scratch
- ✅ Add extensive logging initially
- ✅ Follow examples closely
- ❌ Don't code from memory
- ❌ Don't guess APIs

---

## 📊 Success Metrics 成功指标

**Good Planning Prompt Results 良好的策划提示词结果**:
- Environment setup successful (MCP call worked)
- **Simple projects**: Coding starts within 5 minutes
- **Complex projects**: All documents created before coding
- User says "that's exactly what I want"
- MVP is implementable in reasonable time
- No major scope changes during development
- Documents in memory/ folder are well-structured

**Good Development Prompt Results 良好的开发提示词结果**:
- Code runs on first try (or with minor fixes)
- No common pitfalls encountered
- User understands the code
- Code follows UrhoX best practices

---

## 🔍 Troubleshooting 故障排除

### Issue: AI doesn't follow prompt AI 不遵循提示词
**Solution**:
- Ensure prompt is at start of conversation
- Explicitly reference prompt: "Follow game-development.md guidelines"
- Break complex tasks into smaller steps

### Issue: AI skips documentation AI 跳过文档
**Solution**:
- Add explicit reminder: "Did you read lua-scripting-guide.md?"
- Request: "Show me which example you referenced"
- Ask: "What scaffold did you use?"

### Issue: Code doesn't work 代码不工作
**Solution**:
- Check if scaffold was used
- Verify APIs against documentation
- Check for common pitfalls (see game-development.md)
- Add extensive logging to debug

---

## 📝 Version History 版本历史

**v1.2** (2025-11-21)
- Split into language-specific versions
- Created .en.md files (pure English for LLM) - ~30% token reduction
- Created .zh.md files (pure Chinese for team)
- Keep .md files as bilingual source
- Updated file structure documentation

**v1.1** (2025-11-21)
- TapCode Edition
- game-planning-for-tapcode.md: TapCode workflow with MCP integration
- Simple vs Complex project routing
- memory/ folder documentation system
- Auto environment setup
- Engine communication rules (UrhoX/Urho3D)

**v1.0** (2025-11-21)
- Initial release
- game-development.md: Development mode system prompt

---

## 🤝 Contributing 贡献

To improve these prompts:

1. **Identify issues 识别问题**
   - AI makes repeated mistakes
   - Documentation is outdated
   - New patterns emerge

2. **Update prompts 更新提示词**
   - Add new rules to CRITICAL RULES
   - Update examples
   - Add new best practices

3. **Test thoroughly 彻底测试**
   - Use with real game development tasks
   - Verify AI follows new guidelines
   - Check output quality

4. **Document changes 记录变更**
   - Update version number
   - Add to version history
   - Explain rationale

---

**Version**: v1.2 (Language-Specific Editions)
**Last Updated**: 2025-11-21
**Maintainer**: UrhoX Team

---

## 📌 Quick Start 快速开始

**For LLM Integration LLM 集成**:
```bash
# Use English versions for optimal token efficiency
# Copy content from:
ai-dev-kit/prompts/game-planning-for-tapcode.en.md    # For planning
ai-dev-kit/prompts/game-development.en.md             # For coding
```

**For Team Documentation 团队文档**:
```bash
# Read Chinese versions for better understanding
# Open files:
ai-dev-kit/prompts/game-planning-for-tapcode.zh.md    # 策划指南
ai-dev-kit/prompts/game-development.zh.md             # 开发指南
```
