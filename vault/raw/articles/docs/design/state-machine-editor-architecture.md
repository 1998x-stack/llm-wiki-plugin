---
summary: "AnimationStateMachine visual editor for creating, editing, deleting, and saving states and transitions"
related_paths:
  - engine/Source/Tools/UrhoXEditor/Animation*
  - engine/Source/Urho3D/Animation/**
last_updated: "2026-04-02"
---

# State Machine Editor Architecture

基于 UrhoX Editor 的 AnimationStateMachine 可视化编辑器，支持状态/过渡的创建、编辑、删除和保存。

---

## 功能模块

| 模块 | 说明 |
|------|------|
| 文件管理 | Open / Save / Save As / New |
| 状态 CRUD | 创建、删除、设为默认状态 |
| 过渡 CRUD | 拖拽连线创建、删除、双向偏移显示 |
| 参数管理 | Float/Int/Bool/Trigger 创建、删除、重命名、范围编辑 |
| 属性编辑 | 状态属性 + 过渡属性面板 |
| 资源浏览器集成 | 双击 .fsm 打开、右键新建、拖拽资源 |
| BoneMask 管理 | 创建、删除、Start Bone / Bones List 编辑、骨架导入 |

---

## 文件管理

### 打开方式
- **从组件打开**: 选中 Node → Window → State Machine Editor
- **从文件打开**: 资源浏览器双击 .fsm 文件
- **新建文件**: 资源浏览器右键 → New State Machine...

### 保存功能
- File → Save (Ctrl+S) / Save As...
- UUID 路径自动解析为真实路径
- 未保存修改提示（窗口标题显示 *）

```cpp
bool OpenFile(const String& filePath);
bool OpenFromComponent(AnimationStateMachine* stateMachine);
bool CreateNew(const String& filePath);
bool Save();
bool SaveAs(const String& filePath);
```

---

## 状态 CRUD

| 操作 | 交互方式 |
|------|----------|
| 创建 | 右键画布空白处 → Create State，弹出对话框输入名称 |
| 删除 | 选中后 Del 键，或右键 → Delete（同时删除相关过渡） |
| 设为默认 | 右键 → Set as Default |

```cpp
void CreateState(const String& name, const Vector2& position);
void DeleteState(const String& name);
void SetStateAsDefault(const String& name);
```

---

## 过渡 CRUD

| 操作 | 交互方式 |
|------|----------|
| 创建 | 右键状态 → Create Transition，拖拽连线到目标，ESC 取消 |
| 删除 | 选中后 Del 键，或右键 → Delete |
| 双向显示 | 正向和反向箭头自动偏移，避免重叠 |

```cpp
void CreateTransition(const String& fromState, const String& toState);
void DeleteTransition(int index);
void HandleConnectionDrawing();
void RenderConnectionPreview();
```

---

## 参数管理

- Parameters 面板 "+" 按钮创建（Float/Int/Bool/Trigger）
- "X" 按钮删除
- 双击名称重命名（Enter 确认，ESC 取消）
- Float/Int 支持 Min/Max 范围编辑

```cpp
void CreateParameter(const String& name, int type);
void DeleteParameter(const String& name);
bool RenameParameter(const String& oldName, const String& newName);
void SetParameterRange(const String& name, float minValue, float maxValue);
```

---

## 属性编辑

### 状态属性（右侧面板）
- 状态名称、类型（Animation / BlendSpace / Empty）
- 动画/BlendSpace 路径选择（56x56 预览缩略图，拖拽资源，UUID 支持）
- Loop / Speed / Blend In/Out Time
- Bone Mask 下拉选择

### 过渡属性
- From/To 状态显示
- 条件表达式编辑（多行文本）
- Priority / Blend Time / Exit Time

---

## Layer 管理

- 层列表: 点击切换编辑层，显示状态数/过渡数
- 层重命名: 双击 → Enter 确认
- 层属性: Weight 权重、Blend Mode（Lerp / Additive）、Bone Mask

---

## BoneMask 管理

- "+" 创建 / "X" 删除
- **Start Bone**: 子树根骨骼名称（高效模式，优先级高于 Bones List）
- **Bones List**: 明确骨骼白名单，支持手动添加和"Clear All"
- **骨架导入**: Import All Bones / Import Subtree（从 AnimatedModel 获取）

```cpp
void CreateBoneMask(const String& name);
void DeleteBoneMask(const String& name);
const BoneMaskDef* GetBoneMask(const String& name) const;
void SetBoneMask(const String& name, const BoneMaskDef& mask);
void RemoveBoneMask(const String& name);
void SetBoneWhitelist(const Vector<String>& boneNames);  // AnimationState
```

---

## BoneMask 使用示例

```json
{
  "boneMasks": {
    "UpperBody": { "startBone": "Spine" }
  },
  "layers": [
    { "name": "Base", "defaultState": "Idle", "boneMask": "" },
    {
      "name": "UpperBody", "defaultState": "Empty", "boneMask": "",
      "states": {
        "Gun_Idle": { "boneMask": "" },
        "Gun_Walk": { "boneMask": "UpperBody" },
        "Gun_Run":  { "boneMask": "UpperBody" }
      }
    }
  ]
}
```

| Layer | State | BoneMask | 效果 |
|-------|-------|----------|------|
| Base | Idle/Walk/Run | (空) | 全身播放 |
| UpperBody | Gun_Idle | (空) | 全身覆盖 Base 层 |
| UpperBody | Gun_Walk/Run | UpperBody | 只覆盖上半身 |

---

## UI 布局

```
+------------------------------------------------------------------+
|  File  Edit  View                                    [X]         |
+------------------------------------------------------------------+
|           |                                      |               |
| Layers    |       Canvas (Node Graph)            |  Properties   |
| --------  |                                      |  ----------   |
| > Base    |    [Idle] -----> [Walk]              |  State: Idle  |
|   Upper   |      |             |                 |  Type: Anim   |
|           |      v             v                 |  Path: ...    |
| Params    |    [Jump] <---- [Run]                |  Loop: [x]    |
| --------  |                                      |  Speed: 1.0   |
| Speed     |                                      |  BoneMask: [] |
| IsRun     |                                      |               |
|           |                                      |---------------|
| BoneMasks |                                      |  Layer Props  |
| --------  |                                      |  Weight: 1.0  |
| UpperBody |                                      |  BlendMode:[] |
|           |                                      |  BoneMask: [] |
+-----------+--------------------------------------+---------------+
```

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+S | 保存 |
| Del | 删除选中的状态/过渡 |
| ESC | 取消连线绘制 |
| 中键拖拽 | 平移画布 |
| 滚轮 | 缩放画布 |

---

## 已修复的关键问题

| 问题 | 解决方案 |
|------|----------|
| 双向过渡箭头重叠无法选中 | 添加垂直偏移，渲染和点击检测使用相同逻辑 |
| 保存后 ResourceCache 缓存问题 | UUID 路径解析 + LoadFromJSON 清空现有数据 |
| SetBoneWeight 效果不同于 SetStartBone | 新增 SetBoneWhitelist 方法，重建 stateTracks_ |

---

## 相关文件

### 编辑器
- `engine/Source/Tools/UrhoXEditor/StateMachineEditor.h`
- `engine/Source/Tools/UrhoXEditor/StateMachineEditor.cpp`

### 引擎
- `engine/Source/Urho3D/Animation/AnimationStateMachine.h` / `.cpp`
- `engine/Source/Urho3D/Animation/ParameterContext.h` / `.cpp`
- `engine/Source/Urho3D/Graphics/AnimationState.h` / `.cpp`

### 资源浏览器
- `engine/Source/Tools/UrhoXEditor/ResourceBrowser.h` / `.cpp`

---

## 当前状态

完整编辑功能已实现。未来方向:

- Undo/Redo 支持
- 复制/粘贴状态
- 多选批量操作
- BlendSpace 可视化编辑器
- 动画事件编辑器

---

*最后更新: 2026-04-02*
