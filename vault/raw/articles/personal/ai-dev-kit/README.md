# UrhoX AI Dev Kit

UrhoX Lua 游戏开发的 AI 助手参考文档系统。

## 📁 目录结构

```
ai-dev-kit/
├── claude.md                      # 🤖 AI 入口（首先阅读）
├── README.md                      # 📖 项目说明
│
├── config/                        # 📋 配置和构建（不部署）
│   ├── examples-config.yaml       # 示例配置文件
│   ├── EXAMPLES_README.md         # 配置说明
│   └── ...                        # 其他构建文档
│
├── examples/                      # 💾 示例代码（部署）
│   ├── 01-nanovg-standalone.lua
│   ├── 02-nanovg-ui-component.lua
│   ├── 03-flappy-bird-game.lua
│   ├── 04-box2d-platformer.lua
│   ├── 12-fruit-ninja-3d-game.lua # ⭐ 3D 休闲游戏（PBR 材质）
│   └── api-index.md               # API 索引
│
├── engine-docs/                          # 📖 文档（部署）
│   ├── index.md                   # 主索引
│   ├── principles.md              # 开发准则
│   ├── lua-scripting-guide.md     # Lua 开发指南
│   ├── api/                       # API 参考（20+ 文件）
│   └── recipes/                   # 解决方案
│       ├── ui-layout-guide.md     # UI Layout 系统指南
│       ├── create-menu.md         # 菜单系统
│       ├── materials.md           # 材质
│       └── rendering.md           # 渲染
│
└── templates/                     # 🏗️ 项目脚手架（部署）
    ├── scaffold-2d.lua            # 2D 游戏纯净脚手架（无物理）
    ├── scaffold-2d-physics.lua    # 2D 游戏物理脚手架（Box2D）
    ├── scaffold-3d-scene.lua      # 3D 场景脚手架（展示/可视化/自由相机）
    ├── scaffold-3d-character.lua  # 3D 第三人称角色游戏脚手架 ⭐新增
    └── README.md                  # 脚手架选择指南
```

## 🚀 使用方式

### 对于 AI 助手

**阅读顺序**：
1. 首先阅读 [`CLAUDE.md`](CLAUDE.md) - AI 入口和导航
2. 然后使用 `engine-docs/` 和 `examples/` 目录

```
ai-dev-kit/
├── CLAUDE.md     ← 🤖 从这里开始
├── examples/     ← 💾 示例代码
├── engine-docs/         ← 📖 技术文档
│   └── recipes/
│       └── ui-layout-guide.md  ← UI Layout 唯一文档
└── templates/    ← 🏗️ 项目脚手架
```

**部署时需要**：`CLAUDE.md` + `examples/` + `engine-docs/` + `templates/`

详见：[engine-docs/README.md](engine-docs/README.md)

### 对于开发者

**修改配置**：
```bash
# 编辑配置
vim config/examples-config.yaml

# 验证
python tools/process_examples.py --validate

# 生成
python tools/process_examples.py
```

详见：[config/README.md](config/README.md)

## 📚 快速链接

| 用途 | 链接 |
|------|------|
| **AI 入口** | [CLAUDE.md](CLAUDE.md) |
| **开发准则** | [engine-docs/principles.md](engine-docs/principles.md) |
| **Lua 指南** | [engine-docs/lua-scripting-guide.md](engine-docs/lua-scripting-guide.md) |
| **UI Layout** | [engine-docs/recipes/ui-layout-guide.md](engine-docs/recipes/ui-layout-guide.md) |
| **API 参考** | [engine-docs/api/](engine-docs/api/) |
| **代码示例** | [examples/](examples/) |
| **项目脚手架** | [templates/](templates/) |
| **配置系统** | [config/](config/) |

## ⚠️ 重要提示

### 3D 开发模型尺寸

**开发 3D 游戏时，获取模型尺寸的正确方法**：

- **推荐**: 使用 `model.boundingBox.size` 动态获取
- **备用**: 查阅 [engine-docs/built-in-models.md](engine-docs/built-in-models.md)

**绝不要假设所有模型都是 1×1×1！**

## 🎨 核心特性

### NanoVG 作为 Canvas 替代方案

UrhoX 使用 **NanoVG** 作为 2D 矢量绘图引擎，功能类似于 Web Canvas API：

- **路径绘制** - 直线、曲线、矩形、圆形等
- **填充和描边** - 支持纯色、渐变、图案
- **文本渲染** - 支持自定义字体、对齐、换行
- **变换矩阵** - 平移、旋转、缩放、斜切
- **图像处理** - 加载、绘制、缩放、裁剪

当用户或 AI 提到 Canvas 绘图时，推荐使用 NanoVG 实现。

详见: `engine-docs/api/nanovg.md` 和 `examples/01-nanovg-standalone.lua`

## 🎯 设计理念

### 关注点分离

- **`claude.md`** - AI 入口
  - 导航文档
  - 快速规则

- **`config/`** - 配置和构建
  - 不部署
  - 仅开发时使用

- **`examples/`** - 示例代码
  - 直接部署
  - 独立于文档

- **`engine-docs/`** - 技术文档
  - 直接部署
  - 完整、独立

- **`templates/`** - 项目脚手架
  - 直接部署
  - 快速启动

### 部署方式

```bash
# 方式 1: 完整部署
cp -r ai-dev-kit/claude.md /target/
cp -r ai-dev-kit/examples/ /target/
cp -r ai-dev-kit/engine-docs/ /target/
cp -r ai-dev-kit/templates/ /target/

# 方式 2: 只部署文档（不含示例代码）
cp -r ai-dev-kit/claude.md /target/
cp -r ai-dev-kit/engine-docs/ /target/
```

## 📊 统计信息

- **API 文件**: 20+
- **代码示例**: 4 个
- **分类**: 10 个
- **难度级别**: 3 个（初级、中级、高级）

## 🔧 维护

### 添加新示例

1. 编辑 `config/examples-config.yaml`
2. 运行 `python tools/process_examples.py`
3. 新示例自动生成到 `examples/`

### 文档更新

- 示例代码：`examples/`（自动生成）
- API 文档：`engine-docs/api/`（手动维护）
- 其他文档：`engine-docs/`（手动维护）

## 📖 详细文档

- **AI 使用**: [engine-docs/README.md](engine-docs/README.md)
- **配置说明**: [config/README.md](config/README.md)
- **系统架构**: [config/EXAMPLES_SYSTEM.md](config/EXAMPLES_SYSTEM.md)
- **中文指南**: [config/示例系统说明.md](config/示例系统说明.md)

---

**版本**: v1.0  
**最后更新**: 2025-11-18  
**结构**: claude.md + config/ + examples/ + engine-docs/ + templates/

## 🧠 AI 编码案例库

新增 **coding-insights/** 目录，用于收集和分析 AI 辅助开发中遇到的问题：

- **Math-Algorithm**: 数学和算法相关问题
- **Graphics-Rendering**: 图形和渲染相关问题
- **Performance**: 性能优化问题
- **API-Usage**: API 使用问题
- **Architecture**: 架构设计问题

详见：[coding-insights/README.md](coding-insights/README.md)

### 已收录案例

- [蛇头旋转180度反向问题](coding-insights/Math-Algorithm/snake-head-rotation-flip.md) - 四元数 Slerp 路径选择问题（2025-11-24）
