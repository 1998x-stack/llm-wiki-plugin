# Examples System 示例系统

## 快速开始

### 查看示例

浏览已生成的示例索引：
- [examples/index.md](examples/index.md) - 完整示例索引（按分类、难度）
- [examples/api-index.md](examples/api-index.md) - API使用索引

### 添加新示例

1. 编辑配置文件：`ai-dev-kit/examples-config.yaml`
2. 添加新的示例条目（参考现有格式）
3. 运行处理脚本：

```bash
# 验证配置
python tools/process_examples.py --validate

# 预览（不实际写文件）
python tools/process_examples.py --dry-run

# 正式处理
python tools/process_examples.py
```

### 配置文件结构

```yaml
examples:
  - source: "01_HelloWorld.lua"      # 源文件
    target: "01-hello-world.lua"     # 目标文件名
    metadata:
      title:
        en: "Hello World"
        zh: "你好世界"
      category: "ui"                 # 分类
      difficulty: "beginner"         # 难度
      description: "简短描述"
      features:                      # 功能列表
        - "创建UI文本元素"
      apis:                          # API列表
        - "Text"
        - "UI.root"
      concepts:                      # 概念列表
        - "UI系统基础"
      tags:                          # 标签
        - "ui"
        - "beginner"
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `examples-config.yaml` | 示例配置文件（核心） |
| `examples-config.md` | 配置说明文档 |
| `EXAMPLES_README.md` | 本文件（快速指南） |
| `examples/` | 示例文件目录 |
| `examples/index.md` | 生成的示例索引 |
| `examples/api-index.md` | 生成的API索引 |
| `../tools/process_examples.py` | 处理脚本 |

## 工作流程

```
examples-config.yaml
        ↓
  [处理脚本]
        ↓
    ┌───┴───┐
    ↓       ↓
 复制文件  生成文档
    ↓       ↓
examples/ + index.md
```

## 命令参考

```bash
# 验证配置（不修改文件）
python tools/process_examples.py --validate

# 预览模式（显示将要做什么，但不实际执行）
python tools/process_examples.py --dry-run

# 正式处理（复制文件 + 生成文档）
python tools/process_examples.py

# 需要 PyYAML
pip install pyyaml
```

## 支持的分类

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

## 支持的难度

- `beginner` 🌱 - 初级（< 200行）
- `intermediate` 🌿 - 中级（200-400行）
- `advanced` 🌳 - 高级（> 400行）

## 详细文档

- [examples-config.md](examples-config.md) - 完整配置说明
- [examples/index.md](examples/index.md) - 示例索引
- [examples/api-index.md](examples/api-index.md) - API索引

## 贡献

添加新示例时：
1. 选择合适的分类和难度
2. 填写完整的元信息
3. 只列出主要API（不是全部）
4. 使用 kebab-case 命名
5. 运行验证检查

---

**版本**: v1.0  
**最后更新**: 2025-11-17

