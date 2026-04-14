---
summary: "UrhoX Editor animation editing tools architecture with three core modules (Animation, State Machine, Retargeting)"
related_paths:
  - engine/Source/Tools/UrhoXEditor/Animation*
  - engine/Source/Urho3D/Animation/**
last_updated: "2026-04-02"
---

# Animation Editor Architecture

UrhoX Editor 的动画系统编辑工具，基于 Unity 风格设计，包含三个核心模块。

---

## 模块概览

| 模块 | 功能 | 入口 |
|------|------|------|
| Inspector Preview | 动画预览面板 | 选中 AnimatedModel 组件 |
| Animation Window | 关键帧只读查看器 | 双击动画 |
| State Machine Editor | 状态机可视化编辑器 | Window → State Machine Editor |

> State Machine Editor 的完整编辑功能详见 [state-machine-editor-architecture.md](state-machine-editor-architecture.md)

---

## Inspector Preview - 动画预览面板

在 Inspector 中选中 AnimatedModel 组件时，显示动画预览面板。

**功能**:
- 动画列表显示（来自模型的所有动画）
- 播放/暂停控制、进度条拖拽
- 播放速度调节、循环播放开关
- 当前时间/总时长显示
- 双击动画打开 Animation Window

**相关文件**:
- `engine/Source/Tools/UrhoXEditor/AnimationPreview.h`
- `engine/Source/Tools/UrhoXEditor/AnimationPreview.cpp`

---

## Animation Window - 关键帧只读查看器

独立窗口显示动画的关键帧数据，类似 Unity 的 Animation 窗口（只读模式）。

**功能**:
- **轨道列表**（左侧面板）: 骨骼名称树形显示，Position/Rotation/Scale 子轨道
- **时间轴**（右侧面板）: 时间刻度尺、关键帧菱形标记、网格背景
- **播放控制**: 播放/暂停按钮、播放头（红色竖线）、与 AnimationPreview 同步
- **滚动同步**: 左右面板垂直滚动同步，手动滚动处理（避免抖动）
- **缩放**: Ctrl+滚轮，以鼠标位置为中心缩放

**相关文件**:
- `engine/Source/Tools/UrhoXEditor/AnimationWindow.h`
- `engine/Source/Tools/UrhoXEditor/AnimationWindow.cpp`

---

## State Machine Editor - 状态机编辑界面

节点式可视化编辑器，用于查看、编辑和调试 AnimationStateMachine。

### 画布功能

- 网格背景 + 状态节点显示（默认/当前/选中/BlendSpace/Empty 各有不同颜色标记）
- 过渡连线（箭头指示方向，Any State 过渡从上方）
- 交互操作: 滚轮缩放（25%-200%）、中键平移、左键选中、拖动定位
- Auto Layout 自动布局、Fit View 重置视图

### 左侧面板

- **Layers 列表**: 切换动画层，显示层信息（状态数、过渡数、权重、当前状态）
- **Parameters 面板**: Float/Int 滑块、Bool 复选框、Trigger 按钮，实时修改生效

### 右侧面板

- **State Properties**: 名称、类型、动画路径、Loop、Speed、BlendTime、Bone Mask、Events
- **Transition Properties**: From/To 状态、条件表达式、优先级

### 集成

- 菜单入口: Window → State Machine Editor
- 自动同步: 选中 AnimationStateMachine 组件时自动加载
- PlayMode 实时预览

**相关文件**:
- `engine/Source/Tools/UrhoXEditor/StateMachineEditor.h`
- `engine/Source/Tools/UrhoXEditor/StateMachineEditor.cpp`

---

## 附加功能

### AnimationStateMachine 配置文件支持

Inspector 中为 AnimationStateMachine 组件提供 Config File 属性，支持 .fsm 文件加载。

- `SetConfigFileAttr` / `GetConfigFileAttr` 属性绑定
- 资源浏览器支持 .fsm 和 .blendspace 扩展名
- 拖拽或选择文件自动加载

**相关文件**:
- `engine/Source/Urho3D/Animation/AnimationStateMachine.h`
- `engine/Source/Urho3D/Animation/AnimationStateMachine.cpp`
- `engine/Source/Tools/UrhoXEditor/ResourceBrowser.cpp`
- `engine/Source/Tools/UrhoXEditor/UUID/AssetsFileWatcher.cpp`

### 自定义属性编辑器注册系统

扩展机制，为特定组件的特定属性注册自定义 Inspector UI，避免在 RenderAttribute 中堆积 if-else。

```cpp
RegisterCustomAttributeEditor(ComponentType::GetTypeStatic(), "AttributeName",
    [](Serializable* s, const AttributeInfo& attr, Variant& value) -> bool {
        bool changed = false;
        // ... 自定义 ImGui UI 代码 ...
        return changed;
    });
```

**相关文件**:
- `engine/Source/Tools/UrhoXEditor/UrhoXEditor.h` - 类型定义和注册表
- `engine/Source/Tools/UrhoXEditor/UrhoXEditor.cpp` - 实现

### AimOffset 组件属性绑定

为 AimOffset 组件提供完整的属性反射绑定，包括 Bones 列表的自定义编辑器。

**属性**: Is Enabled, Max Pitch, Max Yaw, Smooth Speed, Yaw Compensation, Stabilize, Stabilize Parent Count, Bones (VariantVector, 自定义编辑器)

**Bones 编辑器 UI**: 可折叠 TreeNode、"+" 添加、每行骨骼名称 + Pitch/Yaw 权重 + "X" 删除

**相关文件**:
- `engine/Source/Urho3D/Animation/AimOffset.h`
- `engine/Source/Urho3D/Animation/AimOffset.cpp`
- `engine/Source/Tools/UrhoXEditor/UrhoXEditor.cpp`

---

## 示例资源

- 状态机配置: `engine/bin/Data/urhox-libs/Animation/FSM/DefaultMaleCharacterFSM.fsm`
- BlendSpace 配置: `engine/bin/Data/urhox-libs/Animation/FSM/DefaultMaleMovementBlendSpace.blendspace`

---

## 当前状态

三个核心模块均已实现。State Machine Editor 支持完整的 CRUD 编辑功能（状态、过渡、参数、BoneMask）。

**未实现**:
- Undo/Redo 支持
- 复制/粘贴状态
- 多选批量操作
- BlendSpace 可视化编辑器
- 动画事件编辑器

---

*最后更新: 2026-04-02*
