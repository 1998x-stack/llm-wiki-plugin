# Examples System Architecture 示例系统架构

## 系统概述

示例系统是一个配置驱动的文档生成系统，用于管理 UrhoX Lua 示例代码的组织、分类和索引。

## 设计目标

1. **统一管理**：通过配置文件统一管理所有示例的元信息
2. **易于扩展**：添加新示例只需编辑配置文件
3. **自动生成**：自动生成多种视图的索引文档
4. **AI友好**：为AI助手提供结构化的示例信息
5. **多语言支持**：支持中英文双语

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  examples-config.yaml                    │
│  (配置文件：示例源、目标、元信息、分类、难度定义)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│             tools/process_examples.py                    │
│  (处理脚本：加载、验证、复制、生成)                        │
└─────┬──────────────┬──────────────┬─────────────────────┘
      │              │              │
      ↓              ↓              ↓
┌──────────┐  ┌──────────┐  ┌──────────────┐
│ 复制文件  │  │ 生成索引  │  │ 生成API索引   │
└─────┬────┘  └─────┬────┘  └──────┬───────┘
      │             │               │
      ↓             ↓               ↓
┌─────────────────────────────────────────────────────────┐
│              ai-dev-kit/examples/                        │
│  ├── 01-hello-world.lua       (示例文件)                 │
│  ├── 02-moving-sprites.lua    (示例文件)                 │
│  ├── ...                                                │
│  ├── index.md                 (主索引：按分类、难度)      │
│  └── api-index.md             (API索引：反向查找)        │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 配置文件 (`examples-config.yaml`)

**位置**: `ai-dev-kit/examples-config.yaml`

**职责**:
- 定义示例列表及其元信息
- 定义分类和难度级别
- 作为单一真实来源（Single Source of Truth）

**数据结构**:
```yaml
version: "1.0"

examples:
  - source: "源文件路径"
    target: "目标文件名"
    metadata:
      title: {en: "", zh: ""}
      category: "分类ID"
      difficulty: "难度ID"
      description: "描述"
      features: [...]
      apis: [...]
      concepts: [...]
      tags: [...]
      line_count: 数字
      dependencies: [...]

categories:
  - id: "分类ID"
    name: {en: "", zh: ""}
    description: "描述"
    icon: "图标"

difficulty_levels:
  - id: "难度ID"
    name: {en: "", zh: ""}
    description: "描述"
    color: "颜色"
    icon: "图标"

api_index:
  # 自动生成
```

### 2. 处理脚本 (`tools/process_examples.py`)

**位置**: `tools/process_examples.py`

**职责**:
- 加载和解析配置文件
- 验证配置完整性和正确性
- 复制示例文件
- 生成索引文档

**主要功能模块**:

```python
class ExamplesProcessor:
    def load_config()          # 加载 YAML 配置
    def validate_config()      # 验证配置
    def copy_examples()        # 复制文件
    def generate_examples_index()  # 生成主索引
    def generate_api_index()   # 生成 API 索引
    def process()              # 完整流程
```

**命令行接口**:
```bash
# 完整处理
python tools/process_examples.py

# 预览模式（不写文件）
python tools/process_examples.py --dry-run

# 只验证配置
python tools/process_examples.py --validate
```

### 3. 生成的文档

#### 3.1 主索引 (`examples/index.md`)

**视图**:
1. **统计信息** - 示例总数、难度分布
2. **按分类浏览** - 每个分类下按难度分组
3. **按难度浏览** - 每个难度下的所有示例
4. **快速查找表** - 表格形式的所有示例

**结构**:
```markdown
# Examples Index

## 统计信息
- 总数：25
- 初级：6, 中级：11, 高级：8

## 按分类浏览
### 🎮 3D图形
#### 🌱 初级
- [示例1](file1.lua) - 描述
- [示例2](file2.lua) - 描述

### 🎨 2D图形
...

## 按难度浏览
### 🌱 初级
1. [示例1](file1.lua) - 描述
2. [示例2](file2.lua) - 描述
...

## 快速查找
| 编号 | 名称 | 分类 | 难度 | 文件 |
|------|------|------|------|------|
| 01   | ... | ... | ... | ... |
```

#### 3.2 API索引 (`examples/api-index.md`)

**视图**:
- API到示例的反向映射
- 每个API列出所有使用它的示例

**用途**:
- AI助手查找使用特定API的示例
- 开发者学习API用法
- 评估API覆盖率

**结构**:
```markdown
# API Usage Index

## 统计信息
- API总数：XX
- 示例总数：XX

## `Scene`
在 5 个示例中使用：
- 🌱 [Static 3D Scene](04-static-3d-scene.lua)
- 🌱 [Animating Scene](05-animating-scene.lua)
...

## `RigidBody`
在 3 个示例中使用：
...
```

## 数据流

### 添加新示例流程

```
1. 开发者编辑 examples-config.yaml
   ↓
2. 添加新的示例条目（source, target, metadata）
   ↓
3. 运行: python tools/process_examples.py --validate
   ↓
4. 修复验证错误（如果有）
   ↓
5. 运行: python tools/process_examples.py
   ↓
6. 生成：
   - ai-dev-kit/examples/XX-new-example.lua
   - ai-dev-kit/examples/index.md (更新)
   - ai-dev-kit/examples/api-index.md (更新)
```

### 自动化流程

```
配置文件 (YAML)
    ↓
[加载] → 内存数据结构
    ↓
[验证] → 检查完整性和正确性
    ↓
[复制] → 文件系统操作
    ↓
[生成] → Markdown 文档
    ↓
输出文件 (Lua + MD)
```

## 扩展点

### 1. 添加新分类

在 `examples-config.yaml` 的 `categories` 部分添加：

```yaml
categories:
  - id: "new-category"
    name:
      en: "New Category"
      zh: "新分类"
    description: "分类描述"
    icon: "🆕"
```

### 2. 添加新元数据字段

在示例的 `metadata` 中添加自定义字段，脚本会保留它们。

### 3. 添加新生成器

扩展 `ExamplesProcessor` 类：

```python
def generate_custom_view(self) -> str:
    """生成自定义视图"""
    # 实现逻辑
    pass
```

### 4. 添加新验证规则

在 `validate_config()` 方法中添加验证逻辑。

## 文件清单

### 配置和文档

```
ai-dev-kit/
├── examples-config.yaml          # 核心配置文件
├── examples-config.md            # 配置说明文档
├── EXAMPLES_README.md            # 快速指南
├── EXAMPLES_SYSTEM.md            # 系统架构（本文件）
└── examples/
    ├── index.md                  # 生成的主索引
    ├── api-index.md              # 生成的API索引
    └── *.lua                     # 示例文件
```

### 工具脚本

```
tools/
└── process_examples.py           # 处理脚本
```

## 设计决策

### 为什么使用 YAML？

1. ✅ 人类可读性强
2. ✅ 支持注释
3. ✅ 支持多行字符串
4. ✅ 支持复杂嵌套结构
5. ✅ Python 有成熟的库支持

### 为什么分离配置和代码？

1. ✅ 非程序员也可以编辑配置
2. ✅ 配置变更不需要修改代码
3. ✅ 易于验证和测试
4. ✅ 配置可以被其他工具使用

### 为什么生成而不是手写索引？

1. ✅ 避免手工维护导致的不一致
2. ✅ 确保所有视图同步更新
3. ✅ 减少人为错误
4. ✅ 易于重新组织

### 为什么使用文件复制而不是符号链接？

1. ✅ Windows 兼容性更好
2. ✅ 可以独立分发 ai-dev-kit
3. ✅ 避免路径问题
4. ✅ 可以在复制时进行转换（如果需要）

## 使用场景

### 场景 1：AI 助手查找示例

**问题**: "如何使用 RigidBody？"

**流程**:
1. AI 查看 `examples/api-index.md`
2. 找到 RigidBody 条目
3. 看到 3 个相关示例
4. 推荐最适合的示例

### 场景 2：用户浏览示例

**流程**:
1. 打开 `examples/index.md`
2. 选择分类（如 "3D图形"）
3. 选择难度（如 "初级"）
4. 查看示例列表和描述
5. 点击链接查看代码

### 场景 3：开发者添加示例

**流程**:
1. 编辑 `examples-config.yaml`
2. 添加新条目
3. 运行验证
4. 运行生成
5. 检查生成的文档
6. 提交更改

### 场景 4：文档生成器使用配置

**流程**:
1. 其他脚本读取 `examples-config.yaml`
2. 解析示例元信息
3. 生成其他形式的文档（如 HTML）

## 最佳实践

### 配置文件

- ✅ 保持 YAML 格式正确
- ✅ 使用一致的缩进（2空格）
- ✅ 标题使用中英文双语
- ✅ 描述简洁明了
- ✅ API 列表只包含主要 API
- ✅ 标签使用小写 kebab-case

### 示例文件

- ✅ 源文件路径正确
- ✅ 目标文件名符合规范
- ✅ 元信息完整
- ✅ 分类和难度正确
- ✅ 功能列表清晰

### 生成文档

- ✅ 不要手动编辑生成的文档
- ✅ 如需修改，编辑配置后重新生成
- ✅ 提交生成的文档到版本控制
- ✅ 定期重新生成以保持同步

## 未来改进

### 短期

- [ ] 添加示例预览截图支持
- [ ] 添加难度自动评估（基于行数、API 复杂度）
- [ ] 添加相关示例推荐
- [ ] 生成 HTML 版本的索引

### 中期

- [ ] 集成到 CI/CD 流程
- [ ] 自动检测源文件变更
- [ ] 生成 API 覆盖率报告
- [ ] 添加示例搜索功能

### 长期

- [ ] Web 界面配置编辑器
- [ ] 在线示例浏览器
- [ ] 示例评分和反馈系统
- [ ] 自动从代码提取元信息

## 参考

- [examples-config.yaml](examples-config.yaml) - 配置文件
- [examples-config.md](examples-config.md) - 配置说明
- [EXAMPLES_README.md](EXAMPLES_README.md) - 快速指南
- [examples/index.md](examples/index.md) - 主索引
- [examples/api-index.md](examples/api-index.md) - API 索引
- [tools/process_examples.py](../tools/process_examples.py) - 处理脚本

## 维护者

系统维护清单：

1. **定期验证**: 运行 `--validate` 检查配置
2. **源文件同步**: 检查原始示例是否有更新
3. **元信息更新**: 保持描述和 API 列表最新
4. **分类调整**: 根据需要添加或修改分类
5. **文档重新生成**: 配置变更后重新生成文档

---

**版本**: v1.0  
**最后更新**: 2025-11-17  
**作者**: UrhoX AI Dev Kit Team

