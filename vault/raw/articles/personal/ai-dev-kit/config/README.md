# config 目录说明

## 用途

此目录包含用于生成 `ai-dev-kit` 文档的配置文件和构建脚本相关文档。

**重要**：此目录中的文件不是给 AI 使用的文档，而是用于生成文档的配置和说明。

## 目录结构

```
config/
├── README.md                      # 本文件
├── examples-config.yaml           # 示例配置（核心）
├── examples-config.md             # 配置说明文档
├── EXAMPLES_README.md             # 快速指南
├── EXAMPLES_SYSTEM.md             # 系统架构
├── NEW_FEATURE_SUMMARY.md         # 功能总结
└── 示例系统说明.md                # 中文使用指南
```

## 文件说明

### 核心配置

- **`examples-config.yaml`** - 示例系统配置文件
  - 定义 25+ 个示例的元信息
  - 包括源文件、目标文件、分类、难度、API等
  - 修改此文件后需运行 `tools/process_examples.py` 重新生成文档

### 文档

- **`examples-config.md`** - 配置文件详细说明（英文）
- **`EXAMPLES_README.md`** - 快速开始指南（英文）
- **`EXAMPLES_SYSTEM.md`** - 系统架构文档（英文）
- **`NEW_FEATURE_SUMMARY.md`** - 新特性功能总结（英文）
- **`示例系统说明.md`** - 中文使用指南

## 使用流程

### 1. 查看配置
```bash
# 查看当前配置
cat ai-dev-kit/config/examples-config.yaml
```

### 2. 验证配置
```bash
# 验证配置是否正确
python tools/process_examples.py --validate
```

### 3. 生成文档
```bash
# 生成示例文件和索引文档
python tools/process_examples.py
```

这会生成：
- `ai-dev-kit/examples/*.lua` - 示例代码文件
- `ai-dev-kit/examples/index.md` - 示例索引
- `ai-dev-kit/examples/api-index.md` - API索引

## 添加新示例

1. 编辑 `examples-config.yaml`
2. 添加新的示例条目
3. 运行 `python tools/process_examples.py --validate`
4. 运行 `python tools/process_examples.py`

详细步骤见 [EXAMPLES_README.md](EXAMPLES_README.md) 或 [示例系统说明.md](示例系统说明.md)。

## 目录命名说明

使用 `config/` 的原因：
- 清晰表达"配置目录"的用途
- 符合行业通用命名惯例
- 主目录 `ai-dev-kit` 保持干净，只包含给 AI 使用的文档

## AI 使用说明

**AI coding assistants** 应该：
- ✅ 读取 `ai-dev-kit/engine-docs/`（所有文档）
  - `engine-docs/api/*.md`（API 参考）
  - `examples/*.lua`（示例代码）
  - `engine-docs/*.md`（指南和FAQ）
- ❌ 忽略 `ai-dev-kit/config/`（构建配置）

部署时只需要 `engine-docs/` 目录，`config/` 目录仅用于开发。

## 相关文件

- **处理脚本**: `tools/process_examples.py`
- **生成的索引**: `ai-dev-kit/examples/index.md`
- **API索引**: `ai-dev-kit/examples/api-index.md`

---

**版本**: v1.0  
**最后更新**: 2025-11-17

