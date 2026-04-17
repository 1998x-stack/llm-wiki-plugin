# Examples Configuration 示例配置系统

## 概述

`examples-config.yaml` 是一个配置文件，用于管理 UrhoX Lua 示例的复制、重命名和元信息。它的主要用途：

1. **示例管理**：描述从 `engine/bin/Data/LuaScripts/` 复制哪些示例到 `ai-dev-kit/examples/`
2. **元信息存储**：记录每个示例的类型、难度、使用的API、主要功能等
3. **文档生成**：为生成 ai-dev-kit 文档中的示例索引提供数据源
4. **AI辅助**：帮助AI助手更好地理解和推荐示例

## 配置文件结构

### 示例条目 (Example Entry)

每个示例包含以下字段：

```yaml
- source: "01_HelloWorld.lua"           # 源文件路径（相对于 engine/bin/Data/LuaScripts/）
  target: "01-hello-world.lua"          # 目标文件名（存储在 ai-dev-kit/examples/）
  metadata:
    title:                              # 标题（支持多语言）
      en: "Hello World"
      zh: "你好世界"
    category: "ui"                      # 分类ID
    difficulty: "beginner"              # 难度级别
    description: "简短描述"             # 一句话描述
    features:                           # 主要功能列表
      - "功能1"
      - "功能2"
    apis:                               # 使用的主要API
      - "API名称1"
      - "API名称2"
    concepts:                           # 涉及的核心概念
      - "概念1"
      - "概念2"
    tags:                               # 标签（用于搜索）
      - "tag1"
      - "tag2"
    line_count: 100                     # 行数（可选）
    dependencies:                       # 依赖文件（可选）
      - "path/to/dependency.lua"
```

### 分类定义 (Categories)

```yaml
categories:
  - id: "3d-graphics"                   # 分类ID
    name:
      en: "3D Graphics"
      zh: "3D图形"
    description: "分类描述"
    icon: "🎮"                          # 图标（可选）
```

支持的分类：
- `3d-graphics` - 3D图形
- `2d-graphics` - 2D图形
- `physics` - 3D物理
- `physics-2d` - 2D物理
- `ui` - 用户界面
- `audio` - 音频
- `network` - 网络
- `animation` - 动画
- `navigation` - 导航与AI
- `advanced` - 高级特性

### 难度级别 (Difficulty Levels)

```yaml
difficulty_levels:
  - id: "beginner"
    name:
      en: "Beginner"
      zh: "初级"
    description: "适合新手"
    color: "#4CAF50"
    icon: "🌱"
```

支持的难度：
- `beginner` - 初级（🌱 绿色）
- `intermediate` - 中级（🌿 橙色）
- `advanced` - 高级（🌳 红色）

## 使用场景

### 1. 添加新示例

编辑 `examples-config.yaml`，添加新的示例条目：

```yaml
examples:
  - source: "99_NewExample.lua"
    target: "26-new-example.lua"
    metadata:
      title:
        en: "New Example"
        zh: "新示例"
      category: "3d-graphics"
      difficulty: "intermediate"
      description: "这是一个新示例"
      features:
        - "功能A"
        - "功能B"
      apis:
        - "Scene"
        - "Node"
      concepts:
        - "核心概念"
      tags:
        - "3d"
        - "example"
```

### 2. 生成示例索引

运行处理脚本（待实现）：

```bash
python tools/process_examples.py
```

这将：
1. 从 `engine/bin/Data/LuaScripts/` 复制文件到 `ai-dev-kit/examples/`
2. 生成 `ai-dev-kit/examples/index.md`（示例索引文档）
3. 生成 `ai-dev-kit/examples/api-index.md`（API使用索引）
4. 更新 `ai-dev-kit/index.md` 中的示例链接

### 3. 按分类查看示例

生成的文档将包含按分类组织的示例：

```markdown
## 3D Graphics 🎮

### Beginner 🌱
- [Static 3D Scene](examples/04-static-3d-scene.lua) - 创建静态3D场景
- [Animating Scene](examples/05-animating-scene.lua) - 动画场景

### Intermediate 🌿
- [Skeletal Animation](examples/06-skeletal-animation.lua) - 骨骼动画
```

### 4. 按难度查看示例

```markdown
## Beginner Examples 🌱

1. [Hello World](examples/01-hello-world.lua) - UI系统基础
2. [Moving Sprites](examples/02-moving-sprites.lua) - UI精灵动画
3. [2D Sprite](examples/03-2d-sprite.lua) - 2D场景基础
```

### 5. API反向索引

查找使用特定API的所有示例：

```markdown
## Scene API

Used in:
- [Static 3D Scene](examples/04-static-3d-scene.lua)
- [Animating Scene](examples/05-animating-scene.lua)
- [3D Physics](examples/07-physics-3d.lua)
- [2D Sprite](examples/03-2d-sprite.lua)
```

## 配置文件管理

### 文件位置

```
ai-dev-kit/
├── examples-config.yaml        # 配置文件
├── examples-config.md          # 说明文档（本文件）
└── examples/                   # 示例文件目录
    ├── 01-hello-world.lua
    ├── 02-moving-sprites.lua
    └── ...
```

### 版本控制

配置文件应纳入版本控制：
- ✅ 提交 `examples-config.yaml`
- ✅ 提交生成的示例文件
- ✅ 提交生成的索引文档
- ❌ 不要手动编辑生成的索引文档

### 验证配置

运行验证脚本（待实现）：

```bash
python tools/validate_examples_config.py
```

将检查：
- 源文件是否存在
- 分类ID是否有效
- 难度级别是否有效
- 必需字段是否完整
- 标题和描述是否为空
- API名称是否在API文档中存在

## 扩展性

### 添加新分类

在 `categories` 部分添加新分类：

```yaml
categories:
  - id: "new-category"
    name:
      en: "New Category"
      zh: "新分类"
    description: "新分类的描述"
    icon: "🆕"
```

### 添加新元数据字段

可以在 `metadata` 中添加自定义字段：

```yaml
metadata:
  # ... 标准字段 ...
  custom_field: "自定义值"
  related_examples:              # 相关示例
    - "01-hello-world.lua"
  video_url: "https://..."       # 视频教程链接
  min_version: "1.0.0"           # 最低版本要求
```

### 多语言支持

当前支持中英文，可扩展到其他语言：

```yaml
title:
  en: "Hello World"
  zh: "你好世界"
  ja: "こんにちは世界"          # 日语
  ko: "안녕하세요 세계"          # 韩语
```

## 工具脚本（计划开发）

### 1. `tools/process_examples.py`

主要功能：
- 读取配置文件
- 复制示例文件
- 生成索引文档

### 2. `tools/validate_examples_config.py`

验证功能：
- 配置文件语法检查
- 源文件存在性检查
- 字段完整性检查
- API名称有效性检查

### 3. `tools/generate_api_index.py`

生成功能：
- API使用统计
- API示例索引
- API覆盖率报告

### 4. `tools/sync_examples.py`

同步功能：
- 检查源文件变更
- 更新示例文件
- 更新行数统计

## 最佳实践

### 编写元信息

1. **标题**：简洁明了，突出重点
   - ✅ "3D Physics"
   - ❌ "A very detailed example about 3D physics simulation"

2. **描述**：一句话概括，不超过50字
   - ✅ "创建3D物理世界，包含静态和动态物理对象"
   - ❌ "这个示例展示了如何使用PhysicsWorld组件来创建一个完整的3D物理模拟环境，包括..."

3. **功能列表**：3-6个要点，使用动词开头
   - ✅ "创建PhysicsWorld"、"添加刚体组件"
   - ❌ "物理世界"、"刚体"

4. **API列表**：只列主要API，不要列所有用到的
   - ✅ Scene, RigidBody, CollisionShape
   - ❌ Scene, Node, Component, RigidBody, CollisionShape, Vector3, Quaternion, ...

5. **概念列表**：核心学习点，抽象层面
   - ✅ "物理模拟"、"刚体动力学"
   - ❌ "如何使用RigidBody组件"

6. **标签**：关键词，用于搜索
   - ✅ "3d", "physics", "rigidbody"
   - ❌ "this-is-a-very-long-tag-name"

### 文件命名规范

目标文件名格式：`{序号}-{kebab-case-name}.lua`

- 使用两位数序号：`01`, `02`, ..., `25`
- 使用连字符分隔单词：`hello-world`, `physics-3d`
- 小写字母
- 简洁明了

示例：
- ✅ `01-hello-world.lua`
- ✅ `07-physics-3d.lua`
- ✅ `18-2d-platformer-game.lua`
- ❌ `1-HelloWorld.lua`
- ❌ `07_Physics3D.lua`
- ❌ `18-This-Is-A-Very-Long-Name.lua`

### 分类选择

选择最相关的单一分类：
- 3D物理示例 → `physics`（不是 `3d-graphics`）
- 2D瓦片地图 → `2d-graphics`
- 网络聊天（有UI）→ `network`（不是 `ui`）

### 难度评估

- **Beginner**：< 200行，单一功能，无复杂逻辑
- **Intermediate**：200-400行，多个功能，中等复杂度
- **Advanced**：> 400行，复杂系统，高级特性

## 示例统计（当前配置）

- 总示例数：25
- 初级示例：6
- 中级示例：11
- 高级示例：8

按分类：
- 3D图形：6
- 2D图形：5
- 物理（3D）：3
- 物理（2D）：2
- UI：3
- 音频：1
- 网络：2
- 动画：2
- 导航：2
- 高级：1

## 参考

- [UrhoX Documentation](../index.md)
- [API Reference](../api/index.md)
- [Examples Directory](examples/)
- [Tools Directory](../../tools/)

---

**版本**: v1.0  
**最后更新**: 2025-11-17

