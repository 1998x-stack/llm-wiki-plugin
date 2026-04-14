---
summary: "Animation retargeting system based on UE5 IK Retargeter architecture, adapted for UrhoX engine"
related_paths:
  - engine/Source/Urho3D/Animation/**
last_updated: "2026-03-25"
---

# Animation Retargeting System Design

> 基于 UE5 IK Retargeter 架构设计，适配 UrhoX 引擎。
>
> @Date: 2026/03/25

---

## 1. 设计目标

将**源骨架**（Source Skeleton）的动画数据迁移到**目标骨架**（Target Skeleton）上播放，支持：

- 不同的骨骼命名（Bip001 vs mixamorig vs UE Mannequin）
- 不同的骨骼数量（Source 和 Target 的 chain 骨骼数可以不同）
- 不同的体型比例（身高、四肢长度）
- 不同的参考姿势（T-Pose vs A-Pose）

---

## 2. 架构总览

### 2.1 三阶段管线（按 UE5 设计）

重定向按固定顺序执行三个阶段：

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Phase 1:    │ ──> │   Phase 2:       │ ──> │  Phase 3:    │
│  Root        │     │   FK Chains      │     │  IK (可选)   │
│  Retarget    │     │   Retarget       │     │  Retarget    │
└──────────────┘     └──────────────────┘     └──────────────┘
```

- **Phase 1 — Root Retarget**：单独处理 Retarget Root 骨骼（通常是 Pelvis/Hips），它是唯一同时重定向位移和旋转的骨骼
- **Phase 1.5 — Ancestor Position**：将 retarget root 祖先骨骼（如 Bip001）的位移 delta 传递到 target root
- **Phase 2 — FK Chain Retarget**：对所有已映射的骨骼链进行旋转（和可选的位移）重定向，使用 per-chain re-rooting 消除祖先帧差异
- **Phase 3 — IK Retarget（可选/未来）**：IK 求解器，用于脚底固定、手部校正等

### 2.2 核心原则

1. **Retarget Root 不属于任何 Chain**，有独立的处理逻辑和参数
2. **未映射的骨骼保持 Reference Pose**，不做任何重定向（UE5 明确设计）
3. **变换存储使用分离的 pos/rot/scale**，不经过 Matrix3x4 打包/拆解
4. **高度比例从 Retarget Root 的世界空间 Y 坐标计算**
5. **Delta 公式使用 LEFT delta**（`delta = srcAnimWorld * srcRefWorld⁻¹`），与 UE5 源码一致

---

## 3. 数据结构

### 3.1 BoneLocalTransform（分离变换存储）

```cpp
/// 分离的本地变换，避免 Matrix3x4 的有损 Rotation() 分解。
struct BoneLocalTransform
{
    Vector3 position_;
    Quaternion rotation_;
    Vector3 scale_{Vector3::ONE};
};
```

**为什么不用 Matrix3x4？**

`Matrix3x4::Rotation()` 需要从矩阵中提取旋转分量，必须先除以 scale。当 scale 接近零、为负数、或数值精度问题时，`Rotation()` 会返回 NaN。实际已在测试中复现：Root 骨骼的 scale 异常导致 NaN 传播，整个模型消失。

UE5 使用 `FTransform`（FVector + FQuat + FVector），始终保持分离存储。

### 3.2 RetargetProfile（.retarget 资源文件）

```
RetargetProfile
├── sourceModelPath_          // 源模型路径
├── targetModelPath_          // 目标模型路径
├── retargetRootSettings_     // Retarget Root 设置
│   ├── sourceBoneName_       //   源骨骼名（如 "Bip001 Pelvis"）
│   ├── targetBoneName_       //   目标骨骼名（如 "mixamorig:Hips"）
│   ├── translationMode_     //   位移模式（GloballyScaled / Absolute / None）
│   ├── scaleHorizontal_     //   水平位移缩放因子
│   ├── scaleVertical_       //   垂直位移缩放因子
│   ├── translationOffset_   //   静态位移偏移
│   └── rotationOffset_      //   静态旋转偏移
├── sourceChains_[]           // 源骨架的 Chain 定义（startBone + endBone）
├── targetChains_[]           // 目标骨架的 Chain 定义（startBone + endBone）
├── chainMappings_[]          // Chain 之间的映射关系
├── chainSettings_[]          // 每个映射的 FK 设置（与 chainMappings_ 平行数组）
│   ├── fkRotationMode_      //   旋转模式
│   └── fkTranslationMode_   //   位移模式
├── sourceReferencePose_      // 源骨架参考姿势
├── targetReferencePose_      // 目标骨架参考姿势
├── sourceBoneRotationOffsets_  // 源骨骼旋转偏移（Retarget Pose）
├── targetBoneRotationOffsets_  // 目标骨骼旋转偏移（Retarget Pose）
└── settings_                 // 全局设置
    └── heightRatioOverride_  //   高度比例手动覆盖（0 = 自动计算）
```

### 3.3 RetargetChainDef（Chain 定义 — UE5 对齐）

```cpp
struct RetargetChainDef
{
    String chainName_;           // 如 "Spine", "LeftArm", "RightLeg"
    String startBoneName_;       // 链的起始骨骼（靠近 root 端）
    String endBoneName_;         // 链的末端骨骼（靠近 tip 端）

    bool IsValid() const { return !startBoneName_.Empty() && !endBoneName_.Empty(); }

    /// 从 endBone 沿 parentIndex_ 回溯到 startBone，填充中间骨骼列表。
    static Vector<String> ResolveChain(const Skeleton& skeleton,
                                        const String& startBoneName,
                                        const String& endBoneName);
};
```

**UE5 设计**：Chain 只存储 **(startBone, endBone)**，不枚举中间骨骼。中间骨骼在需要时通过 `ResolveChain(skeleton)` 从 endBone 沿 `parentIndex_` 回溯到 startBone 自动填充。

**为什么不存 `boneNames_[]`？**

之前的设计按关键字搜索所有匹配角色的骨骼，然后按深度排序。这在有辅助骨骼（`_S`、`_SF`、`Nub`、`Rig_` 等）的骨架上会把旁支骨骼混入链中。例如 3ds Max Biped 的 `Bip001 Spine_S` 与 `Bip001 Spine` 深度相邻，被错误归入 Spine chain。

Parent chain walk 天然只包含直系血缘路径上的骨骼：

```
Bip001 L Thigh
├── Bip001 L Calf
│   ├── Bip001 L Foot         ← endBone
│   └── Bip001 L Calf_S       ← 旁支，不在回溯路径上
└── Bip001 L Thigh_S           ← 旁支，不在回溯路径上

Walk: Foot → Calf → Thigh = [Thigh, Calf, Foot]  ← 干净
```

**重要设计**：Chain 本身不存储 `rotationMode_` 和 `translationMode_`。这些设置在 `RetargetChainSettings` 中，跟随映射关系而不是 Chain 定义。

### 3.4 RetargetRootSettings（Retarget Root 设置）

```cpp
/// Retarget Root 独立设置（UE5: FTargetRootSettings）
struct RetargetRootSettings
{
    String sourceBoneName_;
    String targetBoneName_;
    RetargetTranslationMode translationMode_{RTM_GLOBALLY_SCALED};
    float scaleHorizontal_{1.0f};
    float scaleVertical_{1.0f};
    Vector3 translationOffset_{Vector3::ZERO};
    Quaternion rotationOffset_{Quaternion::IDENTITY};
};
```

### 3.5 RetargetChainSettings（每个映射的 FK 设置）

```cpp
/// 每个 Chain 映射的 FK 设置（UE5: FTargetChainFKSettings）
struct RetargetChainSettings
{
    RetargetRotationMode fkRotationMode_{RRM_INTERPOLATED};
    RetargetTranslationMode fkTranslationMode_{RTM_NONE};
};
```

### 3.6 RetargetRootData（缓存的 Root 阶段数据）

```cpp
/// Setup() 时预计算的 Root 重定向缓存数据。
struct RetargetRootData
{
    unsigned sourceBoneIndex_, targetBoneIndex_;
    Quaternion sourceRefRotation_, targetRefRotation_;           // local space
    Quaternion sourceRefWorldRotation_, targetRefWorldRotation_; // world space
    Vector3 sourceRefPosition_, targetRefPosition_;             // local space
    Vector3 sourceRefWorldPosition_, targetRefWorldPosition_;   // world space
    int translationMode_;
    float scaleHorizontal_, scaleVertical_;
    Vector3 translationOffset_;
    Quaternion rotationOffset_;
    bool isValid_;
};
```

### 3.7 RetargetChainData（缓存的 FK Chain 阶段数据）

```cpp
/// Setup() 时预计算的每条 Chain 的 FK 重定向缓存数据。
struct RetargetChainData
{
    Vector<unsigned> sourceBoneIndices_, targetBoneIndices_;     // root-to-tip 顺序
    Vector<Quaternion> sourceRefRotations_, targetRefRotations_; // local space
    Vector<Quaternion> sourceRefWorldRotations_, targetRefWorldRotations_; // world space
    Vector<Vector3> sourceRefPositions_, targetRefPositions_;
    Vector<float> sourceNormalizedPositions_, targetNormalizedPositions_; // [0, 1]
    Quaternion sourceChainParentWorldRotation_;  // per-chain re-rooting 用
    Quaternion targetChainParentWorldRotation_;
    int fkRotationMode_;      // from ChainSettings
    int fkTranslationMode_;   // from ChainSettings
};
```

---

## 4. 枚举类型

### 4.1 RetargetRotationMode（对齐 UE5）

```cpp
enum RetargetRotationMode
{
    /// [默认] 归一化插值：将 source chain 和 target chain 按累积骨骼长度归一化到 [0,1]，
    /// 每个 target 骨骼在 source chain 上采样对应位置，插值邻近 source 骨骼的 delta 旋转。
    RRM_INTERPOLATED = 0,
    /// 按索引一一对应（从 root 端开始）。Target 比 Source 多的骨骼使用最后一个 source 骨骼。
    RRM_ONE_TO_ONE,
    /// 按索引一一对应（从 tip 端开始）。
    RRM_ONE_TO_ONE_REVERSED,
    /// 不重定向旋转，保持 Target 的 Reference Pose 旋转。
    RRM_NONE
};
```

### 4.2 RetargetTranslationMode（对齐 UE5）

```cpp
enum RetargetTranslationMode
{
    /// 不重定向位移，保持 Target Reference Pose 位置。
    RTM_NONE = 0,
    /// 按高度比例缩放位移 delta。
    /// deltaPos = srcAnimPos - srcRefPos
    /// result = tgtRefPos + deltaPos * heightRatio
    RTM_GLOBALLY_SCALED,
    /// 直接复制源动画的位移值（不缩放）。
    RTM_ABSOLUTE
};
```

---

## 5. 导入时骨骼轴标准化（Standardize Bone Axes）

### 5.0 问题背景

不同 DCC 工具（3ds Max Biped、Maya/Mixamo、Blender）的骨骼局部坐标轴约定不同。即使两个骨架视觉上都是 T-pose，对应骨骼的 world-space 旋转可能差异巨大（如源 pelvis ~180° vs 目标 hips ~10°）。

UE5 通过导入时统一骨骼轴来保证不同来源的骨架具有可比较的 world rotation。UrhoX 采用相同策略。

### 5.1 标准化算法

在 FBX 导入后处理阶段（SFbxConvert），对每根骨骼基于"瞄准子骨骼"方向重建标准化旋转。

**坐标系适配**：UE5 使用 Z-up，UrhoX 导入设置使用 Y-up。标准化参考 up 轴使用 UrhoX 的 **+Y**。标准化结果数值与 UE5 不同，但功能等价 — 只要源和目标在 UrhoX 内部使用同一套约定。

**标准化约定**：aim → local +Y（骨骼长轴方向），参考 up → world +Y

**步骤：**

```
StandardizeBoneAxes(skeleton, animations):

  // Step 1: 计算原始 bind-pose world transforms
  for each bone i (hierarchy order):
    old_bind_world[i] = parent_old_bind_world * M(initialPos, initialRot, initialScale)

  // Step 2: 计算标准化 world rotation
  for each bone i:
    if has_children:
      aim = normalize(avg(child_world_pos) - bone_world_pos)
    else (leaf):
      aim = normalize(bone_world_pos - parent_world_pos)
    if aim nearly parallel to world_up:
      ref_up = world_forward  // 避免退化
    else:
      ref_up = world_up
    std_world_rot[i] = LookRotation(aim, ref_up)
    // LookRotation: Y → aim, Z → up (Gram-Schmidt), X → cross

  // Step 3: 计算新的 local transforms（保持世界位置不变）
  for each bone i (hierarchy order):
    bone.initialRotation_ = parent_std_world_rot⁻¹ * std_world_rot[i]
    bone.initialPosition_ = parent_std_world⁻¹ * bone_world_pos

  // Step 4: 更新 offsetMatrix（新的逆绑定矩阵）
  for each bone i:
    std_world_matrix = M(bone_world_pos, std_world_rot[i], bone_world_scale)
    bone.offsetMatrix_ = std_world_matrix.Inverse()

  // Step 5: 转换动画轨道（保持蒙皮视觉不变）
  // 原理: new_world * new_bind⁻¹ = old_world * old_bind⁻¹
  // => new_world = old_world * old_bind⁻¹ * new_bind
  for each animation, for each frame t:
    for each bone i (hierarchy order):
      old_anim_world[i] = parent_old_anim_world * M(track_pos, track_rot, track_scale)
      new_anim_world[i] = old_anim_world[i] * old_bind_world[i]⁻¹ * new_bind_world[i]
      new_anim_local = parent_new_anim_world⁻¹ * new_anim_world[i]
      track[i][t] = Decompose(new_anim_local)
```

### 5.2 边界情况

- **叶骨骼**（无子节点）：使用"父到自身"方向作为 aim
- **重叠骨骼**（aim 长度接近 0）：保持原始旋转不标准化
- **aim 接近 world up**（spine 等竖直骨骼）：使用 world forward (+Z) 作为参考 up 避免退化
- **单骨骼链**：只有一根骨骼且无子节点 → 跳过标准化
- **无动画的模型**：只标准化骨架，跳过 Step 5

### 5.3 实现位置

- **SFbxImportConfig.h**：`SFbxSceneConvertConfig` 新增 `bool standardizeBoneAxes_{true}`
- **SFbxConvert.cpp**：在 `ConvertFbxScene()` 完成后（skeleton + animation 提取完毕）调用 `StandardizeBoneAxes()`
- **SFbxConvert.h**：声明新函数
- **ModelImporter**：UI 设置面板新增"统一骨骼轴"checkbox（默认开启）

---

## 6. 核心算法

### 6.1 Height Ratio 计算

**方法**：从 Retarget Root 骨骼在 Reference Pose 中的**世界空间 Y 坐标**计算。

```
heightRatio = targetRootWorldY / sourceRootWorldY
```

**世界空间 Y 坐标计算**：从骨骼沿 parent chain 向上累积变换，得到该骨骼在 bind pose 中的世界空间位置，取 Y 分量。

```cpp
static float ComputeRetargetRootWorldY(const Skeleton& skeleton, const String& rootBoneName)
{
    // 从 boneIndex 沿 parent chain 到 root，累积世界变换
    // ... 与 ComputeBoneWorldRotation 类似的 parent chain walk ...
    return worldTransform.Translation().y_;
}
```

**为什么不用 bounding box？** Bounding box 包含所有辅助骨骼（squash/stretch helpers），对高度估计不准确。而 Retarget Root（pelvis/hips）的世界 Y 坐标直接反映模型的"站立高度基准"，更稳定、更有意义。

### 6.2 Phase 1: Root Retarget（LEFT Delta — World Space）

Retarget Root 是整个骨架的"锚点"，通常是 Pelvis/Hips。

**使用 UE5 的 world-space LEFT delta 算法**（与 UE5 `IKRetargetProcessor.cpp` 一致）：

```
输入：
  - 源动画中 Root 骨骼的 animated world rotation (srcAnimWorld)
  - 源 Reference Pose 中 Root 骨骼的 world rotation (srcRefWorld)
  - 目标 Reference Pose 中 Root 骨骼的 world rotation (tgtRefWorld)
  - heightRatio, scaleHorizontal, scaleVertical

处理：
  1. 计算 world-space delta（LEFT delta，UE5 IKRetargetProcessor.cpp:738-743）:
     deltaWorld = srcAnimWorld * srcRefWorld⁻¹

  2. 应用到 target:
     retargetedWorld = deltaWorld * tgtRefWorld

  3. 转回 local space:
     retargetedLocal = tgtParentWorld⁻¹ * retargetedWorld

  4. 计算位移 (GloballyScaled 模式):
     deltaPos = srcAnimPos - srcRefPos
     scaledDelta.x = deltaPos.x * heightRatio * scaleHorizontal
     scaledDelta.y = deltaPos.y * heightRatio * scaleVertical
     scaledDelta.z = deltaPos.z * heightRatio * scaleHorizontal
     retargetedPos = tgtRefPos + scaledDelta

  5. 应用偏移:
     retargetedPos += translationOffset
     retargetedRot = rotationOffset * retargetedRot

输出：
  - Target Root 骨骼的 retargeted local transform
  - retargetedWorld 存入 targetRetargetedGlobals（供后续 FK chain 使用）
```

### 6.3 Phase 1.5: Ancestor Position（祖先骨骼位移传递）

当源骨架的 retarget root 上方有祖先骨骼（如 `Bip001`）携带位移动画时，该位移需要传递到目标的 root 骨骼。否则角色会缺少整体位移（如 die 动画中的倒地位移）。

**条件**：`enableAncestorPosition_ == true` 且 root 的 `translationMode_ == RTM_GLOBALLY_SCALED`

```
处理：
  1. 找到源 retarget root 的父骨骼（ancestor，如 Bip001 Pelvis 的父骨骼 Bip001）
  2. 读取 ancestor 的动画位置和 bind pose 位置
  3. 计算 local delta:
     localDelta = ancestorAnimPos - ancestorBindPos
  4. 转换到 world space（使用 ancestor 的父骨骼的 bind pose rotation + scale）:
     worldDelta = rootBoneBindRot * (rootBoneBindScale * localDelta)
  5. 转换到 target root 的 local space:
     targetLocalDelta = tgtParentWorldRot⁻¹ * worldDelta / parentWorldScale
  6. 按 heightRatio 缩放后加到 target root position:
     curPos.x += targetLocalDelta.x * heightRatio * scaleHorizontal
     curPos.y += targetLocalDelta.y * heightRatio * scaleVertical
     curPos.z += targetLocalDelta.z * heightRatio * scaleHorizontal
```

### 6.4 Phase 2: FK Chain Retarget（Per-chain Re-rooting + LEFT Delta）

对每对已映射的 Chain，使用 UE5 per-chain re-rooting 消除祖先帧差异，然后用 LEFT delta 传递旋转。

#### 6.4.1 Per-chain Re-rooting（UE5 IKRetargetProcessor.cpp:647-655）

```
目的：在 source chain 的 global rotation 计算中，将 source 的祖先帧
      替换为 target 的祖先帧，避免祖先帧差异污染 chain delta。

步骤：
  1. parentDelta = tgtChainParentInitWorld⁻¹ × srcChainParentInitWorld
  2. tgtParentCurrent = 从 targetRetargetedGlobals 查找（如果父骨骼已被重定向）
                        否则使用 tgtChainParentInitWorld
  3. newParent = tgtParentCurrent × parentDelta

  4. 用 source 的 LOCAL 动画旋转在 newParent 下重建 global:
     reRootedGlobal[0] = newParent × srcLocalAnim[0]
     reRootedGlobal[i] = reRootedGlobal[i-1] × srcLocalAnim[i]
```

#### 6.4.2 Chain 归一化

每条 Chain 按累积骨骼长度归一化到 [0, 1]：

```
Chain: [BoneA] --2.0-- [BoneB] --3.0-- [BoneC]
Total length: 5.0
Normalized: BoneA=0.0, BoneB=0.4, BoneC=1.0
```

#### 6.4.3 Per-bone LEFT delta 计算

```
对于每根 Target bone T[t]:
  1. 根据 rotationMode 确定对应的 source global transforms (srcCurrentGlobal, srcInitialGlobal)
  2. 计算 LEFT delta:
     delta = srcCurrentGlobal * srcInitialGlobal⁻¹
  3. 应用到 target reference:
     tgtOutGlobal = delta * tgtRefWorld[t]
  4. 从 chain root 到 tip 逐骨骼转回 local space:
     retargetedLocal = parentGlobal⁻¹ * tgtOutGlobal
```

#### 6.4.4 Interpolated 模式（默认）

```
对于 Target Chain 中的每根骨骼 T[t]:
  1. 计算 T[t] 在 target chain 中的归一化位置 normPos
  2. 在 source chain 归一化位置中找到 normPos 落入的区间 [S[lo], S[hi]]
  3. 计算插值因子 lerpFactor
  4. 插值 source 的 re-rooted global:
     srcCurrentGlobal = Slerp(reRootedGlobal[lo], reRootedGlobal[hi], lerpFactor)
     srcInitialGlobal = Slerp(srcRefWorld[lo], srcRefWorld[hi], lerpFactor)
  5. 计算 LEFT delta 并应用:
     delta = srcCurrentGlobal * srcInitialGlobal⁻¹
     tgtOutGlobal = delta * tgtRefWorld[t]
  6. 位移处理:
     - RTM_NONE: retargetedPos = tgtRefPos[t]
     - RTM_GLOBALLY_SCALED: retargetedPos = tgtRefPos[t] + (srcAnimPos - srcRefPos) * heightRatio
     - RTM_ABSOLUTE: retargetedPos = srcAnimPos
```

#### 6.4.5 OneToOne 模式

```
对于 Target Chain 中的 T[t]:
  - 如果 t < sourceChainSize:
      使用 reRootedGlobal[t] 和 srcRefWorld[t]
  - 如果 t >= sourceChainSize:
      使用最后一个 source 骨骼的 global（UE5 行为）
```

#### 6.4.6 OneToOneReversed 模式

```
对于 Target Chain 中的 T[t]:
  targetStartIndex = max(0, tgtChainSize - srcChainSize)
  sourceStartIndex = max(0, srcChainSize - tgtChainSize)
  - 如果 t < targetStartIndex: delta = 0（保持 reference）
  - 否则: sourceIdx = sourceStartIndex + (t - targetStartIndex)
```

### 6.5 未映射骨骼处理

**所有不属于 Retarget Root 且不在任何已映射 Chain 中的骨骼，保持 Target Reference Pose。不做任何重定向。**

这是 UE5 的明确设计决策。原因：

1. 辅助骨骼（squash/stretch/roll/twist）通常由引擎的约束系统或后处理驱动，不应被动画重定向覆盖
2. IK 骨骼有自己的求解器，不应被 FK 重定向干扰
3. 强制重定向未映射骨骼会产生不可预测的结果

**例外**：同骨架重定向（`heightRatio ≈ 1.0`）时，离线 bake 模式会 pass-through 未映射但同名的骨骼轨道。

### 6.6 Phase 3: IK Retarget（未来扩展）

当前阶段不实现 IK 重定向。未来可扩展：

- 脚底 IK 固定（防止脚滑）
- 手部 IK 校正
- Stride Warping（步幅调整）

---

## 7. Retarget Pose（Bone Rotation Offsets）

RetargetProfile 支持存储每根骨骼的**旋转偏移**（`sourceBoneRotationOffsets_` / `targetBoneRotationOffsets_`），用于定义 **Retarget Pose**。

**Retarget Pose = Bind Pose × Per-bone Rotation Offset**

编辑器提供 **AlignTarget** 功能（UE5: IKRetargeterPoseGenerator），使用链方向匹配算法自动计算 target 骨骼的旋转偏移，使 target 的链方向与 source 对齐。这在 T-Pose vs A-Pose 的跨姿势重定向中尤为重要。

```cpp
/// Per-bone rotation offsets (LOCAL space delta).
void SetBoneRotationOffset(bool isSource, const String& boneName, const Quaternion& offset);
Quaternion GetBoneRotationOffset(bool isSource, const String& boneName) const;

/// Compute world rotation using retarget pose (bind pose × offset).
static Quaternion ComputeRetargetPoseWorldRotation(
    unsigned boneIndex, const Skeleton& skeleton,
    const HashMap<String, Quaternion>& boneRotationOffsets);
```

---

## 8. 自动检测算法

### 8.1 Retarget Root 自动检测

在两个骨架中分别查找 root/pelvis/hips 骨骼：

```
查找策略（按优先级）：
1. 名字包含 "hips" 或 "pelvis"（不区分大小写）
2. 名字包含 "root" 且不是骨架的第一个骨骼（skeleton root 通常不是 retarget root）
3. 如果都找不到，选择深度为 1 的第一个骨骼（skeleton root 的第一个子骨骼）
```

### 8.2 Chain 自动检测（UE5 对齐：startBone + endBone）

自动检测只需要识别每条链模板的 **首尾角色对应的骨骼**，中间骨骼由 `ResolveChain()` 通过 parent chain walk 自动填充。

#### 检测流程

1. **名字归一化**：去除前缀（Bip001、mixamorig:、def_ 等），统一分隔符，转小写
2. **关键词匹配**：将每根骨骼分类到 BoneRole（SPINE、UPPER_ARM、LOWER_ARM 等）
3. **左右判定**：先查名字中的 L/R 标记，回退到空间位置（X 坐标正负）
4. **Chain 模板（仅定义首尾角色）**：

```
ChainTemplate:
  Spine:  startRole=SPINE,    endRole=CHEST
  Head:   startRole=NECK,     endRole=HEAD
  Arm:    startRole=CLAVICLE, endRole=HAND     (lateralized)
  Leg:    startRole=THIGH,    endRole=FOOT     (lateralized)
```

5. **按模板查找首尾骨骼**：对每个模板，在分类结果中找到 startRole 和 endRole 对应的骨骼
   - 如果同一角色有多个匹配骨骼，取**深度最浅**的作为 startBone，**深度最深**的作为 endBone
6. **ResolveChain 验证**：调用 `ResolveChain(skeleton, startBone, endBone)` 确认 startBone 是 endBone 的祖先
7. **侧向展开**：Arm、Leg 自动生成 Left/Right 变体

#### 为什么不再需要 IsHelperBone()

辅助骨骼（`_S`、`_SF`、`Nub`、`Rig_` 等）是主骨骼的旁支子节点，不在 startBone → endBone 的直系路径上。Parent chain walk 从 endBone 回溯只经过直系祖先，旁支天然被排除。

### 8.3 Chain 自动映射

按 Chain 名称匹配 Source 和 Target 的 Chain：

```
Source "LeftArm" <-> Target "LeftArm"
Source "Spine"   <-> Target "Spine"
```

---

## 9. 文件格式

### 9.1 .retarget JSON 格式

```json
{
  "version": 2,
  "sourceModel": "Characters/Source/model.mdl",
  "targetModel": "Characters/Target/model.mdl",

  "retargetRoot": {
    "sourceBone": "Bip001 Pelvis",
    "targetBone": "mixamorig:Hips",
    "translationMode": "globallyScaled",
    "scaleHorizontal": 1.0,
    "scaleVertical": 1.0,
    "translationOffset": [0, 0, 0],
    "rotationOffset": [1, 0, 0, 0]
  },

  "sourceChains": [
    {
      "name": "Spine",
      "startBone": "Bip001 Spine",
      "endBone": "Bip001 Spine2"
    }
  ],

  "targetChains": [
    {
      "name": "Spine",
      "startBone": "mixamorig:Spine",
      "endBone": "mixamorig:Spine2"
    }
  ],

  "chainMappings": [
    {
      "sourceChain": 0,
      "targetChain": 0,
      "fkRotationMode": "interpolated",
      "fkTranslationMode": "none"
    }
  ],

  "settings": {
    "heightRatioOverride": 0
  },

  "sourceReferencePose": { ... },
  "targetReferencePose": { ... }
}
```

---

## 10. 类设计

### 10.1 AnimationRetargeter（核心引擎类）

```cpp
class AnimationRetargeter
{
public:
    /// 从 Profile 和两个 Skeleton 构建缓存数据。
    void Setup(const RetargetProfile* profile,
               const Skeleton& sourceSkeleton,
               const Skeleton& targetSkeleton);

    /// 运行时：单帧重定向（用于 PostProcess 管线）。
    void RetargetPose(const HashMap<StringHash, BoneLocalTransform>& sourceTransforms,
                      HashMap<StringHash, BoneLocalTransform>& outTargetTransforms) const;

    /// 离线：将整个 Animation 重定向为新的 Animation 资源。
    /// 包含 ancestor position 传递和同骨架 pass-through。
    SharedPtr<Animation> RetargetAnimation(Context* context,
                                            Animation* sourceAnim,
                                            const Skeleton& sourceSkeleton,
                                            const Skeleton& targetSkeleton) const;

    /// Height ratio (target / source).
    float GetHeightRatio() const;

    /// Ancestor position: 将 retarget root 祖先骨骼的位移传递到 target root。
    void SetEnableAncestorPosition(bool enable);
    bool GetEnableAncestorPosition() const;

    /// Bone world rotation 计算辅助函数。
    static Quaternion ComputeAnimatedWorldRotation(
        unsigned boneIndex, const Skeleton& skeleton,
        const HashMap<StringHash, BoneLocalTransform>& localTransforms,
        const HashSet<StringHash>* retargetScope = nullptr);
    static Quaternion ComputeBoneWorldRotation(unsigned boneIndex, const Skeleton& skeleton);
    static Quaternion ComputeRetargetPoseWorldRotation(
        unsigned boneIndex, const Skeleton& skeleton,
        const HashMap<String, Quaternion>& boneRotationOffsets);
    static Vector3 ComputeAnimatedWorldPosition(
        unsigned boneIndex, const Skeleton& skeleton,
        const HashMap<StringHash, BoneLocalTransform>& localTransforms);
    static Vector3 ComputeRetargetPoseWorldPosition(
        unsigned boneIndex, const Skeleton& skeleton,
        const HashMap<String, Quaternion>& boneRotationOffsets);

private:
    void RetargetRoot(...) const;
    void RetargetChainFK(...) const;
    static Quaternion RetargetRotation(
        const Quaternion& srcCurrent, const Quaternion& srcRef, const Quaternion& tgtRef);
    static void ComputeChainNormalizedPositions(...);

    RetargetRootData rootData_;
    Vector<RetargetChainData> chainData_;
    float heightRatio_{1.0f};
    bool isSetup_{false};
    bool enableAncestorPosition_{true};
    Skeleton sourceSkeleton_, targetSkeleton_;  // 缓存副本
    HashMap<unsigned, StringHash> sourceBoneIndexToHash_, targetBoneIndexToHash_;
    HashMap<StringHash, unsigned> sourceBoneHashToIndex_, targetBoneHashToIndex_;
};
```

### 10.2 RetargetProfile（资源类）

```cpp
class RetargetProfile : public Resource
{
    // 序列化/反序列化 (JSON)
    bool BeginLoad(Deserializer& source) override;
    bool Save(Serializer& dest) const override;
    bool LoadJSON(const JSONValue& root);
    bool SaveJSON(JSONValue& root) const;

    // 数据
    String sourceModelPath_, targetModelPath_;
    RetargetRootSettings retargetRootSettings_;
    Vector<RetargetChainDef> sourceChains_, targetChains_;
    Vector<RetargetChainMapping> chainMappings_;
    Vector<RetargetChainSettings> chainSettings_;  // 与 chainMappings_ 平行
    RetargetReferencePose sourceReferencePose_, targetReferencePose_;
    RetargetSettings settings_;

    // Retarget Pose (per-bone rotation offsets)
    HashMap<String, Quaternion> sourceBoneRotationOffsets_;
    HashMap<String, Quaternion> targetBoneRotationOffsets_;

    // 自动检测
    static String AutoDetectRetargetRoot(const Skeleton& skeleton);
    static void AutoDetectChains(const Skeleton& skeleton, Vector<RetargetChainDef>& outChains,
                                 const String& retargetRootBoneName = String::EMPTY);
    void AutoMapChains();
    void AutoSetup(const Skeleton& sourceSkeleton, const Skeleton& targetSkeleton);
};
```

### 10.3 RetargetPostProcess（运行时后处理）

```cpp
class RetargetPostProcess : public AnimationPostProcess
{
public:
    /// 初始化（由 AnimatedModel::AddPostProcess 调用）。
    void Initialize(AnimatedModel* animatedModel) override;

    /// Setup 方式一：profile + sourceSkeleton，target skeleton 从 AnimatedModel 获取。
    void Setup(RetargetProfile* profile, const Skeleton& sourceSkeleton);
    /// Setup 方式二：profile + sourceSkeleton + targetSkeleton 显式指定。
    void Setup(RetargetProfile* profile, const Skeleton& sourceSkeleton, const Skeleton& targetSkeleton);

    /// 设置源 AnimatedModel，Update() 从该模型的骨骼节点读取实时变换。
    /// 用于编辑器双模型预览：source model 播放动画，target model 通过 PostProcess 重定向。
    void SetSourceAnimatedModel(AnimatedModel* sourceModel);

    RetargetProfile* GetProfile() const;
    const AnimationRetargeter& GetRetargeter() const;
    bool IsReady() const;

protected:
    /// 执行重定向：
    /// - 若 sourceAnimatedModel_ 已设置：从 source model 的骨骼节点读取 live transforms
    /// - 否则：从 CSPose 读取（假设 pose 骨骼名 == source 骨骼名）
    /// 然后执行 Phase 1 (Root) → Phase 1.5 (Ancestor Position) → Phase 2 (FK Chains)，
    /// 最后将结果写回 CSPose 和骨骼节点。
    void Update(AnimationContext& ctx) override;

private:
    SharedPtr<RetargetProfile> profile_;
    Skeleton sourceSkeleton_;
    AnimationRetargeter retargeter_;
    WeakPtr<AnimatedModel> sourceAnimatedModel_;
};
```

**Update() 工作流**：

1. 构建 `sourceLocalTransforms`（source bone nameHash → BoneLocalTransform）
   - **有 sourceAnimatedModel_**：从 source model 的骨骼节点读取实时 local transforms
   - **无 sourceAnimatedModel_**：从 CSPose 读取（假设 CSPose 骨骼名 == source 骨骼名）
2. Phase 1：Root retarget（LEFT delta），写入 CSPose
3. Phase 1.5：Ancestor position 传递
4. Phase 2：FK chains（per-chain re-rooting + LEFT delta），写入 CSPose
5. 将 CSPose 中的 retargeted transforms 直接设置到骨骼节点（`SetTransformSilent`）

### 10.4 RetargetEditor（编辑器 UI）

编辑器负责：
- 加载源/目标模型，显示双 3D 视口预览（独立 Scene + RenderTexture）
- 自动检测 Chain + 自动映射
- 手动编辑 Retarget Root 设置（骨骼选择、位移模式、缩放因子、偏移）
- 手动编辑 Chain 定义（startBone/endBone）和映射
- 每个 Chain 映射可配置旋转模式和位移模式
- AlignTarget：自动计算骨骼旋转偏移对齐 target 到 source
- 动画播放预览：
  - **Offline 模式**：bake 后的 Animation 播放
  - **Runtime 模式**：source model 播放动画，target model 通过 RetargetPostProcess + SetSourceAnimatedModel 实时重定向
- 骨骼可视化（skeleton debug drawing、bone pick、bone info panel）
- 导出 Bake 后的 Animation 文件
- 保存/加载 .retarget Profile

---

## 11. 实施状态

### 全部已完成

| # | 改动 | 状态 |
|---|------|------|
| 1 | Root 单独处理，不属于任何 Chain | ✅ |
| 2 | 未映射骨骼保持 Reference Pose | ✅ |
| 3 | Height ratio 从 Retarget Root 世界空间 Y 坐标计算 | ✅ |
| 4 | 全程使用 BoneLocalTransform | ✅ |
| 5 | 模式跟随映射关系（ChainSettings） | ✅ |
| 6 | 四种旋转模式（Interpolated/OneToOne/OneToOneReversed/None） | ✅ |
| 7 | RetargetPostProcess 改用 BoneLocalTransform | ✅ |
| 8 | Editor UI 适配（Root 面板、映射模式选择等） | ✅ |
| 9 | Chain 定义重构为 (startBone, endBone) + ResolveChain | ✅ |
| 10 | AutoDetect 按首尾角色识别 + ResolveChain 验证 | ✅ |
| 11 | 导入时骨骼轴标准化（StandardizeBoneAxes） | ✅ |
| 12 | UE5 LEFT delta 算法 + per-chain re-rooting | ✅ |
| 13 | Ancestor position 传递（Bip001 等祖先骨骼位移） | ✅ |
| 14 | Retarget Pose（BoneRotationOffsets + AlignTarget） | ✅ |

### 待完成

| # | 改动 | 说明 |
|---|------|------|
| 15 | 脚本 runtime 透明化 | PostProcess 应支持单 AnimatedModel 场景（脚本只创建 target model 并播放 source 动画），当前编辑器使用双模型 + SetSourceAnimatedModel |
| 16 | IK Retarget (Phase 3) | 脚底 IK 固定、手部 IK 校正等 |

---

## 12. 影响的文件

| 文件 | 职责 |
|------|------|
| `engine/Source/Urho3D/Graphics/AnimationRetargeter.h` | 核心数据结构（BoneLocalTransform, RetargetRootData, RetargetChainData）+ AnimationRetargeter 类 |
| `engine/Source/Urho3D/Graphics/AnimationRetargeter.cpp` | 三阶段管线实现（Setup, RetargetRoot, RetargetChainFK, RetargetPose, RetargetAnimation） |
| `engine/Source/Urho3D/Graphics/RetargetProfile.h` | 资源数据结构（RetargetRootSettings, RetargetChainDef, RetargetChainSettings 等）+ RetargetProfile 类 |
| `engine/Source/Urho3D/Graphics/RetargetProfile.cpp` | JSON 序列化、AutoDetect、AutoMap |
| `engine/Source/Urho3D/Graphics/RetargetPostProcess.h` | RetargetPostProcess 声明 |
| `engine/Source/Urho3D/Graphics/RetargetPostProcess.cpp` | 运行时后处理实现（从 source model 或 CSPose 读取 → 三阶段重定向 → 写回 CSPose + bone nodes） |
| `engine/Source/Tools/SFbxImport/SFbxConvert.cpp` | StandardizeBoneAxes() 骨骼轴标准化 |
| `engine/Source/Tools/SFbxImport/SFbxConvert.h` | StandardizeBoneAxes 声明 |
| `engine/Source/Tools/SFbxImport/SFbxImportConfig.h` | standardizeBoneAxes_ 配置项 |
| `engine/Source/Tools/UrhoXEditor/ModelImporter.cpp/h` | UI checkbox 传入标准化设置 |
| `engine/Source/Tools/UrhoXEditor/RetargetEditor.cpp/h` | 编辑器 UI（双视口预览、Chain 编辑、动画预览、AlignTarget） |

---

## 附录 A：UE5 参考资料

- [UE5 IK Rig Animation Retargeting](https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine)
- [Retargeting Bipeds with IK Rig](https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine)
- [Wicked Engine - Animation Retargeting](https://wickedengine.net/2022/09/animation-retargeting/)（开源实现，算法与 UE5 一致）
- UE5 源码：`IKRetargetProcessor.cpp`（lines 627-812: FK chain retarget, lines 738-743: root delta）

## 附录 B：术语表

| 术语 | 含义 |
|------|------|
| **Retarget Root** | 重定向根骨骼（Pelvis/Hips），唯一同时重定向位移和旋转的骨骼 |
| **Reference Pose** | 参考姿势（T-Pose 或 A-Pose），delta 计算的基准 |
| **Retarget Pose** | 重定向姿势 = Bind Pose × BoneRotationOffsets，用于 T-Pose vs A-Pose 的跨姿势对齐 |
| **LEFT Delta** | `delta = srcAnimWorld * srcRefWorld⁻¹`，源骨骼相对于参考姿势的旋转变化量（UE5 实际实现） |
| **Height Ratio** | `targetRootWorldY / sourceRootWorldY`，用于缩放位移 |
| **Chain Normalization** | 将 chain 中的骨骼按累积长度映射到 [0, 1] 范围 |
| **Per-chain Re-rooting** | UE5 技术：将 source chain 的 global 计算重建在 target 的祖先帧下，消除祖先帧差异 |
| **Ancestor Position** | 将 retarget root 上方祖先骨骼（如 Bip001）的位移动画传递到 target root |
| **FK Retarget** | Forward Kinematics 重定向，基于旋转传递 |
| **IK Retarget** | Inverse Kinematics 重定向，基于目标位置求解（未来） |
