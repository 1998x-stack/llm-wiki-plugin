# AI Coding Insights - AI 编码问题案例库

## 📚 目的 (Purpose)

这个案例库用于收集和分析在使用 AI 辅助开发 UrhoX 游戏时遇到的各类问题，包括：

- **问题现象**：用户观察到的 Bug 或异常行为
- **根本原因**：技术层面的深层次分析
- **解决方案**：正确的实现方式和代码示例
- **经验教训**：如何避免类似问题，最佳实践
- **AI 局限性分析**：是 LLM 的根本局限，还是知识/经验不足？

**核心价值**：
1. ✅ 帮助 AI 从错误中学习，避免重复犯错
2. ✅ 为开发者提供"踩坑指南"和最佳实践
3. ✅ 识别 AI 编程的局限性和适用边界
4. ✅ 改进引擎 API 设计，降低使用难度
5. ✅ 积累 UrhoX 游戏开发的领域知识

---

## 🗂️ 分类体系 (Categories)

### 1. Math-Algorithm (数学与算法)
数学计算、几何变换、算法逻辑相关问题

**典型问题**：
- 四元数旋转计算错误
- 坐标系变换问题
- 碰撞检测算法缺陷
- 路径规划错误

**已收录案例**：
- [蛇头旋转180度反向问题](Math-Algorithm/snake-head-rotation-flip.md) (2025-11-24)
- [正交相机缩放补偿：orthoSize 的 2x 因子陷阱](Math-Algorithm/orthographic-zoom-compensation.md) (2026-02-05)

### 2. Graphics-Rendering (图形与渲染)
渲染效果、材质、光照、相机相关问题

**典型问题**：
- 材质参数设置错误
- 光照计算不符合预期
- 相机视锥体配置问题
- Z-fighting 和深度缓冲问题

**已收录案例**：
- [使用 CustomGeometry 模拟内置模型缺失的基础形状](Graphics-Rendering/custom-geometry-for-missing-primitives.md) (2025-12-23)

### 3. Performance (性能优化)
性能瓶颈、内存泄漏、卡顿相关问题

**典型问题**：
- 不必要的对象创建
- 热路径上的低效算法
- 内存泄漏和野指针
- 批处理和缓存优化

**已收录案例**：
- (待添加)

### 4. API-Usage (API 使用)
引擎 API 误用、参数错误、调用时序问题

**典型问题**：
- API 调用顺序错误
- 参数类型或单位错误
- 生命周期管理问题
- 回调函数使用不当

**已收录案例**：
- [CollisionShape 尺寸参数使用直径而非半径](API-Usage/collision-shape-diameter-vs-radius.md) (2026-01-06)
- [mouseMove.z 获取滚轮值导致 nil 错误](API-Usage/mouse-wheel-not-on-mousemove.md) (2026-02-08)

### 5. Architecture (架构设计)
代码结构、模块划分、设计模式相关问题

**典型问题**：
- 模块耦合过紧
- 职责划分不清
- 状态管理混乱
- 过度设计或欠设计

**已收录案例**：
- (待添加)

---

## 📝 案例模板 (Case Template)

每个案例文件应包含以下部分：

```markdown
# [问题标题]

**日期**: YYYY-MM-DD
**分类**: [Math-Algorithm / Graphics-Rendering / Performance / API-Usage / Architecture]
**严重程度**: [Critical / High / Medium / Low]
**游戏/项目**: [游戏名称或通用问题]

---

## 🐛 问题现象 (Observed Behavior)

描述用户看到的现象，最好包含：
- 截图或 GIF 动画
- 复现步骤
- 预期行为 vs 实际行为

---

## 🔍 问题原因 (Root Cause Analysis)

深入分析技术层面的根本原因：
- 错误的假设或理解
- 数学/算法错误
- API 误用
- 架构缺陷

---

## ✅ 解决方案 (Solution)

### 错误做法 (Wrong Approach)
```lua
-- 错误的代码示例
```

### 正确做法 (Correct Approach)
```lua
-- 正确的代码示例
```

---

## 💡 经验教训 (Lessons Learned)

- 关键洞察点
- 最佳实践建议
- 如何避免类似问题

---

## 🤖 AI 局限性分析 (AI Limitations Analysis)

**问题性质分类**：
- [ ] LLM 根本局限（数学推理、空间想象等）
- [ ] 知识/经验不足（可通过学习改进）
- [ ] 上下文理解错误
- [ ] 其他（说明）

**改进建议**：
- 对 AI：如何提示可以避免此问题？
- 对引擎：API 设计改进建议
- 对文档：需要补充的知识点

---

## 🔗 相关资源 (Related Resources)

- 相关引擎文档链接
- 参考文章或教程
- 相关 Issue 或 PR
```

---

## 🚀 使用方法 (How to Use)

### 添加新案例

1. **确定分类**：根据问题性质选择合适的目录
2. **创建文件**：使用描述性的文件名（小写-连字符分隔），例如 `snake-head-rotation-flip.md`
3. **填写内容**：按照模板填写完整信息
4. **更新索引**：在本 README 的对应分类下添加链接

### 查找案例

- **按分类浏览**：进入对应目录查看相关问题
- **全文搜索**：使用 VSCode 或 grep 搜索关键词
- **按日期排序**：查看最新收录的案例

### 案例编号规则

文件命名格式：`[简短描述].md`

例如：
- `snake-head-rotation-flip.md`
- `particle-memory-leak.md`
- `quaternion-slerp-path.md`

---

## 📊 统计信息 (Statistics)

- **总案例数**: 5
- **Math-Algorithm**: 2
- **Graphics-Rendering**: 1
- **Performance**: 0
- **API-Usage**: 2
- **Architecture**: 0

最后更新：2026-02-08

---

## 🤝 贡献指南 (Contributing)

欢迎所有 UrhoX 开发者贡献案例！

**贡献流程**：
1. 遇到问题时详细记录现象和解决过程
2. 创建 PR 添加新案例
3. 填写完整的案例模板
4. 更新本 README 索引

**质量标准**：
- ✅ 问题描述清晰，有复现步骤
- ✅ 原因分析深入，有技术细节
- ✅ 解决方案有代码示例
- ✅ 经验教训有可操作性
- ✅ AI 局限性分析客观准确

---

## 📜 许可证 (License)

本案例库遵循 MIT License，与 UrhoX 项目保持一致。
