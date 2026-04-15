---
summary: "Runtime animation retargeting design for transparently playing source model animations on target models"
related_paths:
  - engine/Source/Urho3D/Animation/**
last_updated: "2026-04-02"
---

# 运行时动画重定向（Runtime Animation Retargeting）

## 概述

支持在运行时透明地将 SourceModel 的动画播放到 TargetModel 上，脚本层无需感知重定向细节。

**核心目标**：脚本只需正常加载 TargetModel + 创建 AnimationController + 播放 SourceModel 的动画，引擎后台自动完成重定向。

---

## 前置功能：RetargetReferencePose 轻量骨架化

### 背景

当前 `AnimationRetargeter::Setup()` 需要完整的 `Skeleton` 对象来提供源/目标骨架信息。但运行时场景中通常只有 TargetModel，SourceModel 未加载。

分析发现，retargeter 运行时实际使用的 Bone 字段仅有 5 个：

| Bone 字段 | 用途 |
|-----------|------|
| `name_` / `nameHash_` | 骨骼查找、track 匹配 |
| `parentIndex_` | 所有 ComputeWorldRotation/Position 函数的 parent chain 遍历 |
| `initialPosition_` | 参考位置、链长度计算 |
| `initialRotation_` | 参考旋转、世界旋转计算 |
| `initialScale_` | 缩放传递、输出 scale |

而现有 `RetargetReferencePose` 只存了 `boneNames_[]` + `boneTransforms_[]`（Matrix3x4），**缺少 `parentIndex_`**，且 Matrix3x4 存储旋转存在 `Rotation()` 分解 NaN 风险。

### 改造方案

将 `RetargetReferencePose` 从"参考姿态快照"升级为"轻量骨架定义"，使其能完全替代 `Skeleton` 在 retargeter 中的角色。

#### 数据结构变更

使用 AoS（Array of Structs）布局。retargeter 的典型访问模式是沿 parent chain 遍历，每个 bone 读取多个字段（parentIndex + rotation + position + scale），AoS 让同一 bone 的所有字段在同一 cache line 内，缓存命中率优于并行数组（SoA）。

```cpp
// Before
struct RetargetReferencePose
{
    Vector<String> boneNames_;
    Vector<Matrix3x4> boneTransforms_;   // 旋转分解有 NaN 风险，且实际只用了 Translation()
};

// After
struct RetargetBoneDef
{
    String name;
    unsigned parentIndex;
    Vector3 position;
    Quaternion rotation;
    Vector3 scale{Vector3::ONE};
};

struct RetargetReferencePose
{
    Vector<RetargetBoneDef> bones_;
};
```

**为什么 AoS 而非 SoA（并行数组）**：

retargeter 运行时的核心操作是 parent chain walk（`ComputeBoneWorldRotation` 等），每次循环读取同一 bone 的 `parentIndex` + `initialRotation`（有时还有 `initialPosition`、`initialScale`）。AoS 布局下这些字段相邻，一次 cache line 读取即可拿到所有需要的数据；SoA 则需要跨数组跳转，每个字段一次 cache miss。

#### 索引一致性

`BuildFromSkeleton` 按 `skeleton.GetBones()` 的顺序遍历，所以：
- `bones_[i].parentIndex` == `skeleton.GetBones()[i].parentIndex_`（parentIndex 本身就是数组下标，直接拷贝即可）
- `bones_[i].position` == `skeleton.GetBones()[i].initialPosition_`
- `bones_[i].rotation` == `skeleton.GetBones()[i].initialRotation_`
- `bones_[i].scale` == `skeleton.GetBones()[i].initialScale_`

#### BuildFromSkeleton 变更

```cpp
void RetargetReferencePose::BuildFromSkeleton(const Skeleton& skeleton)
{
    const Vector<Bone>& srcBones = skeleton.GetBones();
    unsigned numBones = srcBones.Size();
    bones_.Resize(numBones);
    for (unsigned i = 0; i < numBones; ++i)
    {
        RetargetBoneDef& def = bones_[i];
        def.name = srcBones[i].name_;
        def.parentIndex = srcBones[i].parentIndex_;
        def.position = srcBones[i].initialPosition_;
        def.rotation = srcBones[i].initialRotation_;
        def.scale = srcBones[i].initialScale_;
    }
}
```

#### GetBoneTransform 兼容

保留 `GetBoneTransform()` 接口以保持向后兼容，内部从结构体字段构造：

```cpp
Matrix3x4 RetargetReferencePose::GetBoneTransform(const String& boneName) const
{
    for (unsigned i = 0; i < bones_.Size(); ++i)
    {
        if (bones_[i].name == boneName)
            return Matrix3x4(bones_[i].position, bones_[i].rotation, bones_[i].scale);
    }
    return Matrix3x4::IDENTITY;
}
```

### AnimationRetargeter 适配

#### 目标

让 `Setup()` 和运行时方法可以接受 `RetargetReferencePose` 替代 `Skeleton`。

#### 方案

新增 `Setup` 重载，直接从 profile 内的 reference pose 构建，不需要外部 Skeleton：

```cpp
/// Setup from profile only (uses profile's embedded reference poses as skeleton data).
/// No external Skeleton objects needed — suitable for runtime retargeting
/// where the source model is not loaded.
void Setup(const RetargetProfile* profile);
```

内部实现将 `RetargetBoneDef` 映射到 Bone 字段：
- `refPose.bones_[i].name` → `bone.name_`
- `refPose.bones_[i].parentIndex` → `bone.parentIndex_`
- `refPose.bones_[i].rotation` → `bone.initialRotation_`
- `refPose.bones_[i].position` → `bone.initialPosition_`
- `refPose.bones_[i].scale` → `bone.initialScale_`

分两步实施，先保证正确性再优化：

#### Step 1：构造临时 Skeleton（最小改动，验证正确性）✅ 已完成

新增 `ToSkeleton()` 方法，`Setup(profile)` 内部构造临时 Skeleton 后调用现有 `Setup(profile, srcSkel, tgtSkel)`。

- 改动最小，现有 Setup/RetargetPose/RetargetAnimation 全部不用改
- Skeleton::Define 本身就是内存拷贝，性能开销可忽略（Setup 只调用一次）
- 用现有单元测试验证 retarget 结果与原始 Skeleton 路径完全一致

```cpp
Skeleton RetargetReferencePose::ToSkeleton() const
{
    Skeleton skeleton;
    Vector<Bone>& dstBones = skeleton.GetModifiableBones();
    dstBones.Resize(bones_.Size());
    for (unsigned i = 0; i < bones_.Size(); ++i)
    {
        const RetargetBoneDef& def = bones_[i];
        dstBones[i].name_ = def.name;
        dstBones[i].nameHash_ = StringHash(def.name);
        dstBones[i].parentIndex_ = def.parentIndex;
        dstBones[i].initialPosition_ = def.position;
        dstBones[i].initialRotation_ = def.rotation;
        dstBones[i].initialScale_ = def.scale;
    }
    return skeleton;
}

void AnimationRetargeter::Setup(const RetargetProfile* profile)
{
    Skeleton srcSkel = profile->GetSourceReferencePose().ToSkeleton();
    Skeleton tgtSkel = profile->GetTargetReferencePose().ToSkeleton();
    Setup(profile, srcSkel, tgtSkel);
}
```

#### Step 2：去掉 Skeleton 依赖，直接使用 RetargetReferencePose

**核心思路**：`AnimationRetargeter` 内部不再持有 `Skeleton`，改为持有 `RetargetReferencePose`。所有内部方法直接访问 `RetargetBoneDef` 的字段（`name`、`nameHash`、`parentIndex`、`position`、`rotation`、`scale`），不再经过 `Bone` 结构体。

**好处**：
- 消除 Skeleton 中不需要的字段（node_、offsetMatrix_、collisionMask_ 等）的内存开销
- AoS 布局的 RetargetBoneDef 比 Bone（134 字节含大量无关字段）更紧凑，cache line 利用率更高
- 语义更清晰：retargeter 依赖的是轻量骨架定义，不是完整的 Skeleton
- `Setup(profile, srcSkel, tgtSkel)` 删除，公共 API 只保留 `Setup(profile)`，调用方负责确保 profile 的 reference pose 已构建

##### 2.1 RetargetBoneDef 添加 nameHash

```cpp
struct RetargetBoneDef
{
    String name;
    StringHash nameHash;     // ← 新增，避免运行时重复构造
    unsigned parentIndex{0};
    Vector3 position{Vector3::ZERO};
    Quaternion rotation{Quaternion::IDENTITY};
    Vector3 scale{Vector3::ONE};
};
```

- `BuildFromSkeleton`：赋值 `nameHash = srcBones[i].nameHash_`
- JSON 加载：从 `name` 计算 `nameHash = StringHash(name)`
- `ToSkeleton`：直接用 `def.nameHash`（不再临时构造）

##### 2.2 RetargetReferencePose 添加骨骼查找方法

```cpp
/// Get bone index by name. Returns M_MAX_UNSIGNED if not found.
unsigned GetBoneIndex(const String& boneName) const;
/// Get bone index by name hash. Returns M_MAX_UNSIGNED if not found.
unsigned GetBoneIndex(const StringHash& nameHash) const;
```

线性查找，和 `Skeleton::GetBoneIndex` 行为一致。只在 `Setup` 期间调用（一次性），不在热路径。

##### 2.3 ResolveChain / ComputeRetargetRootWorldY 添加 RetargetReferencePose 重载

```cpp
// RetargetChainDef — 新增重载，保留原 Skeleton 版本不变
static Vector<String> ResolveChain(const RetargetReferencePose& refPose,
                                    const String& startBoneName,
                                    const String& endBoneName);

// RetargetProfile — 新增重载，保留原 Skeleton 版本不变
static float ComputeRetargetRootWorldY(const RetargetReferencePose& refPose,
                                        const String& rootBoneName);
```

原有 `Skeleton` 版本保留（RetargetEditor、AutoDetectChains 仍在使用）。

##### 2.4 AnimationRetargeter 成员替换

```cpp
// Before
Skeleton sourceSkeleton_;
Skeleton targetSkeleton_;

// After
RetargetReferencePose sourcePose_;
RetargetReferencePose targetPose_;
```

头文件 include 从 `Skeleton.h` 改为 `RetargetProfile.h`（需要 `RetargetReferencePose` 完整定义）。

##### 2.5 AnimationRetargeter 公共 API 变更

| Before | After |
|--------|-------|
| `Setup(profile, srcSkel, tgtSkel)` | **删除** |
| `Setup(profile)` | 保留（唯一入口） |
| `RetargetAnimation(ctx, anim, srcSkel, tgtSkel)` | `RetargetAnimation(ctx, anim)` |

调用方在调 `Setup(profile)` 之前负责确保 profile 的 reference pose 已通过 `BuildReferencePoses(srcSkel, tgtSkel)` 构建。

##### 2.6 私有方法简化

Skeleton 参数全部去掉，直接使用成员 `sourcePose_` / `targetPose_`：

```cpp
// Before
void RetargetRoot(
    const HashMap<StringHash, BoneLocalTransform>& sourceLocalTransforms,
    const Skeleton& sourceSkeleton,
    HashMap<StringHash, BoneLocalTransform>& outTargetLocalTransforms,
    const Skeleton& targetSkeleton,
    HashMap<unsigned, Quaternion>& targetRetargetedGlobals) const;

// After
void RetargetRoot(
    const HashMap<StringHash, BoneLocalTransform>& sourceLocalTransforms,
    HashMap<StringHash, BoneLocalTransform>& outTargetLocalTransforms,
    HashMap<unsigned, Quaternion>& targetRetargetedGlobals) const;
```

`RetargetAncestorPosition`、`RetargetChainFK` 同理。

##### 2.7 静态方法改为 RetargetReferencePose

```cpp
// Before
static Quaternion ComputeBoneWorldRotation(unsigned boneIndex, const Skeleton& skeleton);

// After
static Quaternion ComputeBoneWorldRotation(unsigned boneIndex, const RetargetReferencePose& pose);
```

全部 5 个静态方法 + `ComputeChainNormalizedPositions` 同理。

##### 2.8 内部实现字段映射

所有内部方法中的 Bone 字段访问统一替换：

| Skeleton/Bone | RetargetReferencePose/RetargetBoneDef |
|---------------|---------------------------------------|
| `skeleton.GetBones()` | `pose.bones_` |
| `bones[idx].name_` | `bones_[idx].name` |
| `bones[idx].nameHash_` | `bones_[idx].nameHash` |
| `bones[idx].parentIndex_` | `bones_[idx].parentIndex` |
| `bones[idx].initialPosition_` | `bones_[idx].position` |
| `bones[idx].initialRotation_` | `bones_[idx].rotation` |
| `bones[idx].initialScale_` | `bones_[idx].scale` |
| `sourceSkeleton.GetBoneIndex(name)` | `sourcePose_.GetBoneIndex(name)` |

Setup 中所有 `if (!srcRefPose.IsEmpty())` 分支删除——数据统一从 `sourcePose_` / `targetPose_` 读取。

##### 2.9 调用方更新

**RetargetEditor.cpp**（4 处 Setup + 2 处 RetargetAnimation + 2 处静态方法）：

```cpp
// Before
retargeter_.Setup(profile_, sourceAnimModel_->GetSkeleton(), targetAnimModel_->GetSkeleton());
retargeter_.RetargetAnimation(ctx, anim, srcSkel, tgtSkel);
AnimationRetargeter::ComputeRetargetPoseWorldRotation(idx, tgtSkeleton, offsets);

// After（profile 已调过 BuildReferencePoses，reference pose 数据已是最新的）
retargeter_.Setup(profile_);
retargeter_.RetargetAnimation(ctx, anim);
AnimationRetargeter::ComputeRetargetPoseWorldRotation(idx, profile_->GetTargetReferencePose(), offsets);
```

**RetargetAnimCommand.cpp**（1 处 Setup + 1 处 RetargetAnimation）：同上。

**RetargetPostProcess.cpp**（3 处 Setup）：

```cpp
// Before
retargeter_.Setup(profile_.Get(), sourceSkeleton_, animatedModel->GetSkeleton());

// After — 先确保 profile reference pose 最新，再 Setup
profile_->BuildReferencePoses(sourceSkeleton_, animatedModel->GetSkeleton());
retargeter_.Setup(profile_.Get());
```

### JSON 序列化变更

Profile 文件（`.retarget`）的 reference pose 部分需要更新格式：

```json
{
  "sourceReferencePose": {
    "bones": [
      {
        "name": "Hips",
        "parent": -1,
        "position": [0, 0.9, 0],
        "rotation": [0, 0, 0, 1],
        "scale": [1, 1, 1]
      },
      {
        "name": "Spine",
        "parent": 0,
        "position": [0, 0.1, 0],
        "rotation": [0, 0, 0, 1],
        "scale": [1, 1, 1]
      }
    ]
  }
}
```

**向后兼容**：加载时检测是否有 `parent` 字段。如果没有（旧格式），标记 reference pose 为"不完整"，`Setup(profile)` 会失败并提示需要提供外部 Skeleton。

### 影响范围

| 文件 | Step 1 变更 | Step 2 变更 |
|------|-------------|-------------|
| `RetargetProfile.h` | `RetargetBoneDef` AoS 结构 + `RetargetReferencePose` 新方法 | 添加 `nameHash` 字段 + `GetBoneIndex` + `ResolveChain`/`ComputeRetargetRootWorldY` 重载 |
| `RetargetProfile.cpp` | `BuildFromSkeleton` + `ToSkeleton` + JSON 序列化 | 实现新增方法；`BuildFromSkeleton` 赋值 `nameHash`；JSON 加载计算 `nameHash` |
| `AnimationRetargeter.h` | 新增 `Setup(const RetargetProfile*)` 重载 | 删除 `Setup(profile, srcSkel, tgtSkel)` + 成员/方法/静态方法全面改签名 |
| `AnimationRetargeter.cpp` | 实现 `Setup(profile)` 过渡（ToSkeleton） | 全面改写，`Skeleton` → `RetargetReferencePose` |
| `RetargetEditor.cpp` | 无需改动 | 4 处 Setup + 2 处 RetargetAnimation + 2 处静态方法调用更新 |
| `RetargetAnimCommand.cpp` | 无需改动 | 1 处 Setup + 1 处 RetargetAnimation 更新 |
| `RetargetPostProcess.cpp` | 无需改动 | 3 处 Setup 更新（需先调 `BuildReferencePoses`） |

### 验证要点

1. **编译通过**：`cmake --build . --target UrhoXServer --config Release` 零错误
2. **现有单元测试通过**：retarget 结果与 Step 1 完全一致
3. **JSON 向后兼容**：旧格式 .retarget 文件能正常加载（缺少 parentIndex 时降级）
4. **无 NaN 风险**：旋转直接存储为 Quaternion，不再经过 Matrix3x4 往返
5. **离线工具不受影响**：RetargetEditor、RetargetAnimCommand 仍先调 `BuildReferencePoses`，再调 `Setup(profile)`

---

## 运行时重定向方案 ✅ 前置功能已完成，进入实现阶段

### 设计目标

脚本只需正常播放动画，引擎自动检测并完成重定向：

```lua
-- 脚本层完全不感知重定向
local node = scene_:CreateChild("NPC")
local model = node:CreateComponent("AnimatedModel")
model:SetModel(cache:GetResource("Model", "Models/CharacterB.mdl"))
local animCtrl = node:CreateComponent("AnimationController")
animCtrl:Play("Animations/walk.ani", 0, true)  -- 这个动画可能是给 CharacterA 做的
-- 引擎后台自动重定向，脚本无需关心
```

### 核心架构

```
AnimationController::Play("walk.ani")
  │
  ├─ Animation* sourceAnim = cache->GetResource("walk.ani")
  ├─ Model* targetModel = GetModelComponent()->GetModel()
  │
  └─ RuntimeRetargeterCache* rtCache = GetSubsystem<RuntimeRetargeterCache>()
     Animation* finalAnim = rtCache->GetOrBake(targetModel, sourceAnim)
       │
       ├─ 映射表查不到 sourceAnim
       │   └─ return sourceAnim（原样播放，不重定向）
       │
       ├─ 查到 sourceModelPath，和 targetModel path 一致
       │   └─ return sourceAnim（同模型，不需要重定向）
       │
       └─ sourceModelPath != targetModelPath，需要重定向：
           │
           ├─ Profile 缓存命中 {srcModelPath, tgtModelPath}
           │   └─ 复用已有 profile
           ├─ Profile 缓存未命中
           │   ├─ sourceRefPose 从映射表取（轻量骨架，不加载 source model）
           │   ├─ tempSrcSkel = sourceRefPose.ToSkeleton()
           │   ├─ tgtSkel = targetModel->GetSkeleton()
           │   ├─ profile->AutoSetup(tempSrcSkel, tgtSkel)
           │   └─ 缓存 profile
           │
           ├─ Animation 缓存命中 {sourceAnimPath, profileKey}
           │   └─ return 缓存的重定向动画
           └─ Animation 缓存未命中
               ├─ retargeter.Setup(profile)
               ├─ retargetedAnim = retargeter.RetargetAnimation(ctx, sourceAnim)
               ├─ 缓存 retargetedAnim
               └─ return retargetedAnim
```

### 动画映射表（Animation Mapping Table）

#### 设计思路

运行时需要知道一个动画资产属于哪个"体型"（source model），才能判断是否需要重定向。这个映射关系通过一个配置文件维护，由官方定期更新。

#### 文件格式

文件路径：约定为 `Retarget/AnimationMappings.json`（通过 ResourceCache 加载）。

```json
{
    "bodyTypes": {
        "humanoid_a": {
            "modelPath": "Models/HumanoidA.mdl",
            "referencePose": {
                "bones": [
                    {
                        "name": "Bip001",
                        "parent": -1,
                        "position": [0, 0, 0],
                        "rotation": [0, 0, 0, 1],
                        "scale": [1, 1, 1]
                    },
                    {
                        "name": "Bip001 Pelvis",
                        "parent": 0,
                        "position": [0, 0.9, 0],
                        "rotation": [0, 0, 0, 1],
                        "scale": [1, 1, 1]
                    }
                ]
            }
        },
        "humanoid_b": {
            "modelPath": "Models/HumanoidB.mdl",
            "referencePose": {
                "bones": [...]
            }
        }
    },

    "animations": {
        "Animations/walk.ani": "humanoid_a",
        "Animations/run.ani": "humanoid_a",
        "Animations/idle.ani": "humanoid_a",
        "Animations/attack.ani": "humanoid_b"
    }
}
```

#### 数据结构

```
bodyTypes（体型定义）:
  key:   体型标识符（如 "humanoid_a"）
  value: {
    modelPath:     源模型资产路径（用于与 targetModel 比较是否同体型）
    referencePose: RetargetReferencePose 轻量骨架数据（嵌入到映射表中，
                   运行时不需要加载 source model）
  }

animations（动画到体型的映射）:
  key:   动画资产路径（与 ResourceCache 中的资源名一致）
  value: 体型标识符（引用 bodyTypes 中的 key）
```

**设计要点**：

- 体型和动画分开存储，避免重复（大量动画共享同一体型）
- `referencePose` 嵌入在体型定义中，运行时直接读取，**不需要加载 source model**
- 动画的 key 使用资产路径（而非 UUID），与 ResourceCache 资源名一致，查找方便
- 映射表由官方定期维护，通过热更新下发

### RuntimeRetargeterCache 子系统

#### 职责

1. 加载和管理动画映射表
2. 判断动画是否需要重定向
3. 按需创建 RetargetProfile（AutoSetup）并缓存
4. 按需烘焙重定向动画并缓存
5. 对外提供唯一接口 `GetOrBake(targetModel, sourceAnim)`

#### 类设计

```cpp
/// Runtime animation retargeting cache subsystem.
/// Manages animation mapping table, auto-generates RetargetProfiles,
/// and caches baked retargeted animations.
class URHO3D_API RuntimeRetargeterCache : public Object
{
    URHO3D_OBJECT(RuntimeRetargeterCache, Object);

public:
    explicit RuntimeRetargeterCache(Context* context);

    /// Load animation mapping table from JSON file.
    /// @param path Resource path (e.g., "Retarget/AnimationMappings.json").
    bool LoadMappingTable(const String& path);

    /// Core API: get retargeted animation for a target model.
    /// Returns sourceAnim as-is if no retargeting is needed (same model,
    /// or animation not in mapping table).
    /// Returns cached or freshly baked retargeted animation otherwise.
    Animation* GetOrBake(Model* targetModel, Animation* sourceAnim);

    /// Clear all caches (profiles + baked animations).
    void ClearCache();

    /// Get cache statistics for debugging.
    unsigned GetCachedProfileCount() const;
    unsigned GetCachedAnimationCount() const;

private:
    /// Body type definition (from mapping table).
    struct BodyTypeDef
    {
        String modelPath_;
        RetargetReferencePose referencePose_;
    };

    /// Body type definitions keyed by type identifier.
    HashMap<String, BodyTypeDef> bodyTypes_;

    /// Animation path -> body type identifier.
    HashMap<String, String> animationMappings_;

    /// Profile cache: {sourceModelPath + ":" + targetModelPath} -> profile.
    HashMap<String, SharedPtr<RetargetProfile>> profileCache_;

    /// Baked animation cache: {sourceAnimPath + ":" + profileKey} -> retargeted animation.
    HashMap<String, SharedPtr<Animation>> animationCache_;
};
```

#### GetOrBake 核心流程

```cpp
Animation* RuntimeRetargeterCache::GetOrBake(Model* targetModel, Animation* sourceAnim)
{
    if (!targetModel || !sourceAnim)
        return sourceAnim;

    // Step 1: 映射表查找 — 动画属于哪个体型？
    const String& animPath = sourceAnim->GetName();
    auto animIt = animationMappings_.Find(animPath);
    if (animIt == animationMappings_.End())
        return sourceAnim;  // 不在映射表中，原样播放

    // Step 2: 获取体型定义
    auto bodyIt = bodyTypes_.Find(animIt->second_);
    if (bodyIt == bodyTypes_.End())
        return sourceAnim;  // 体型定义缺失，原样播放

    const BodyTypeDef& bodyType = bodyIt->second_;

    // Step 3: 比较 source model 和 target model 是否一致
    const String& targetModelPath = targetModel->GetName();
    if (bodyType.modelPath_ == targetModelPath)
        return sourceAnim;  // 同模型，不需要重定向

    // Step 4: 查找或创建 profile
    String profileKey = bodyType.modelPath_ + ":" + targetModelPath;
    SharedPtr<RetargetProfile>& profile = profileCache_[profileKey];
    if (!profile)
    {
        // 从映射表中的轻量骨架创建临时 Skeleton（不加载 source model）
        Skeleton tempSrcSkel = bodyType.referencePose_.ToSkeleton();
        const Skeleton& tgtSkel = targetModel->GetSkeleton();

        profile = new RetargetProfile(context_);
        profile->AutoSetup(tempSrcSkel, tgtSkel);
    }

    // Step 5: 查找或烘焙重定向动画
    String animCacheKey = animPath + ":" + profileKey;
    auto cachedIt = animationCache_.Find(animCacheKey);
    if (cachedIt != animationCache_.End())
        return cachedIt->second_;  // 缓存命中

    // 同步烘焙
    AnimationRetargeter retargeter;
    retargeter.Setup(profile);

    if (!retargeter.IsSetup())
    {
        URHO3D_LOGWARNING("RuntimeRetargeterCache: retargeter setup failed for "
                          + animPath + " -> " + targetModelPath);
        return sourceAnim;  // 兜底：原样播放
    }

    SharedPtr<Animation> retargetedAnim = retargeter.RetargetAnimation(context_, sourceAnim);
    if (!retargetedAnim)
    {
        URHO3D_LOGWARNING("RuntimeRetargeterCache: bake failed for " + animPath);
        return sourceAnim;  // 兜底：原样播放
    }

    // 保留原始动画名（AnimationController 用 name hash 做 Stop/IsPlaying 查找）
    retargetedAnim->SetName(sourceAnim->GetName());

    animationCache_[animCacheKey] = retargetedAnim;
    return retargetedAnim;
}
```

#### 性能分析

| 操作 | 时机 | 开销 |
|------|------|------|
| LoadMappingTable | 启动时一次 | JSON 解析 + 骨架数据解析，~ms 级 |
| 映射表查找 | 每次 Play | HashMap 查找，O(1) |
| Model path 比较 | 每次 Play（映射表命中时） | 字符串比较，极低 |
| AutoSetup | 每个 {source, target} 对首次 | 链检测 + 映射，~ms 级，仅一次 |
| RetargetAnimation | 每个 {animation, profile} 对首次 | 纯 CPU 四元数运算，~30 骨骼 × ~100 keyframe = 亚毫秒级 |
| 缓存命中 | 后续 Play | HashMap 查找，O(1) |

**同步 vs 异步**：选择同步烘焙。理由：
- `RetargetAnimation` 纯 CPU 数学运算（无 IO），亚毫秒级完成
- 避免异步带来的占位动画、回调、线程安全等复杂度
- 首次 Play 的微小延迟对玩家不可感知

### AnimationController 集成

#### 改动点

在 `AnimationController::Play()` / `PlayExclusive()` 中，获取 Animation 资源后、创建 AnimationState 前，插入重定向检查：

```cpp
const StringHash& AnimationController::Play(const String& name, unsigned char layer,
                                             bool looped, float fadeInTime, float fadeOutTime)
{
    // 获取动画资源（现有逻辑）
    Animation* animation = GetAnimation(name);
    if (!animation)
        return StringHash::ZERO;

    // === 新增：运行时重定向 ===
    auto* rtCache = GetSubsystem<RuntimeRetargeterCache>();
    if (rtCache)
    {
        AnimatedModel* model = GetModelComponent();
        if (model && model->GetModel())
            animation = rtCache->GetOrBake(model->GetModel(), animation);
    }
    // === 新增结束 ===

    // 创建 AnimationState + 设置播放参数（现有逻辑）
    AnimationState* state = AddAnimationState(animation);
    // ...
}
```

#### 改动范围

仅修改 `AnimationController.cpp`，在 `Play` 和 `PlayExclusive` 两个方法中各插入 ~5 行代码。

### Fallback 策略

| 场景 | 行为 |
|------|------|
| 动画不在映射表中 | 原样播放（不重定向） |
| sourceModel == targetModel | 原样播放（不需要重定向） |
| AutoSetup 失败 | 原样播放 + 打 warning 日志 |
| RetargetAnimation 失败 | 原样播放 + 打 warning 日志 |
| RuntimeRetargeterCache 子系统未注册 | 原样播放（兼容无重定向场景） |

所有 fallback 都是静默降级，不影响游戏运行。

### 动画名保留

烘焙出的新 Animation 保留原始动画的 name，确保 AnimationController 的以下操作不受影响：

```lua
animCtrl:Play("walk.ani", 0, true)
animCtrl:Stop("walk.ani")                -- 用原始名停止，正常工作
animCtrl:IsPlaying("walk.ani")           -- 用原始名查询，正常工作
animCtrl:SetSpeed("walk.ani", 2.0)       -- 用原始名设置速度，正常工作
```

### 映射表维护流程

映射表的生产分两步：人工维护动画到体型的映射关系，CLI 工具自动补全骨架数据。

```
Step 1 — 人工维护（官方定期更新）:
  └─ 编辑 AnimationMappings.json，填写 bodyTypes（仅 modelPath）+ animations 映射
     此时 bodyTypes 中没有 referencePose 字段

Step 2 — CLI 工具自动补全:
  └─ UrhoXCLI build-anim-mappings -i AnimationMappings.json -r <资源根目录>
     ├─ 读取 JSON
     ├─ 遍历 bodyTypes，加载各 modelPath 的 .mdl 文件
     ├─ BuildFromSkeleton → RetargetReferencePose
     ├─ 将 referencePose 写入 bodyTypes
     └─ 覆盖写回原 JSON 文件（输出 = 输入）

运行时（UrhoXServer / UrhoXRuntime）:
  ├─ 启动时加载 AnimationMappings.json（已含完整骨架数据）
  ├─ 解析体型定义 + 动画映射
  └─ 后续 Play 时自动查找 + 重定向
```

### CLI 命令：build-anim-mappings

#### 用途

读取人工维护的 AnimationMappings.json（不含 referencePose），自动加载各体型的 source model，提取骨架数据补全 referencePose，覆盖写回原文件。

这样人工只需要维护动画到体型的映射关系，不需要手动填写骨架数据。

#### 命令格式

```bash
UrhoXCLI build-anim-mappings [options]

Required:
  -i, --input <path>      AnimationMappings.json 文件路径
  -r, --resource <path>   资源根目录（用于解析 modelPath 相对路径）

Options:
  -h, --help              显示帮助
```

#### 输入文件格式（人工维护，不含骨架数据）

```json
{
    "bodyTypes": {
        "humanoid_a": {
            "modelPath": "Models/HumanoidA.mdl"
        },
        "humanoid_b": {
            "modelPath": "Models/HumanoidB.mdl"
        }
    },

    "animations": {
        "Animations/walk.ani": "humanoid_a",
        "Animations/run.ani": "humanoid_a",
        "Animations/attack.ani": "humanoid_b"
    }
}
```

#### 输出文件格式（CLI 补全后，覆盖写回）

```json
{
    "bodyTypes": {
        "humanoid_a": {
            "modelPath": "Models/HumanoidA.mdl",
            "referencePose": {
                "bones": [
                    {
                        "name": "Bip001",
                        "parent": -1,
                        "position": [0, 0, 0],
                        "rotation": [0, 0, 0, 1],
                        "scale": [1, 1, 1]
                    },
                    ...
                ]
            }
        },
        ...
    },

    "animations": {
        "Animations/walk.ani": "humanoid_a",
        ...
    }
}
```

#### 处理流程

```cpp
int RunBuildAnimMappings(const Vector<String>& arguments)
{
    // 1. 解析参数：-i (input json path), -r (resource base path)
    // 2. 读取 JSON 文件
    // 3. 遍历 bodyTypes:
    for (auto& bodyType : bodyTypes)
    {
        // 3a. 拼接模型完整路径: resourcePath + "/" + bodyType.modelPath
        // 3b. 加载 .mdl 文件，获取 Skeleton
        Model* model = LoadModelFromFile(context, fullModelPath);
        if (!model || model->GetSkeleton().GetNumBones() == 0)
        {
            PrintLine("Error: Cannot load model or no skeleton: " + modelPath);
            return 1;
        }

        // 3c. BuildFromSkeleton → RetargetReferencePose
        RetargetReferencePose refPose;
        refPose.BuildFromSkeleton(model->GetSkeleton());

        // 3d. 序列化 referencePose 到 JSON
        //     复用 RetargetProfile 中已有的 JSON 序列化逻辑
        JSONValue poseJson;
        // ... 写入 bones 数组（name, parent, position, rotation, scale）

        // 3e. 设置到 bodyType JSON 节点
        bodyTypeJson["referencePose"] = poseJson;

        PrintLine("  " + bodyTypeName + ": " + String(refPose.GetNumBones()) + " bones");
    }

    // 4. 覆盖写回原 JSON 文件
    File outFile(context);
    outFile.Open(inputPath, FILE_WRITE);
    // ... 写入格式化的 JSON

    PrintLine("Updated " + String(bodyTypeCount) + " body types in " + inputPath);
    return 0;
}
```

#### 错误处理

| 场景 | 行为 |
|------|------|
| 模型文件不存在 | 报错并退出（不覆盖原文件） |
| 模型没有骨架 | 报错并退出 |
| bodyType 的 modelPath 为空 | 报错并退出 |
| JSON 格式错误 | 报错并退出 |
| animations 部分引用了不存在的 bodyType | 打 warning，不阻断 |

**设计要点**：任何体型加载失败都终止整个流程，不做部分写入，避免产出不完整的映射表。

#### 使用示例

```bash
# 人工维护的映射表（只有 modelPath 和动画映射）
cat Retarget/AnimationMappings.json
# { "bodyTypes": { "humanoid_a": { "modelPath": "Models/HumanoidA.mdl" } }, ... }

# CLI 补全骨架数据
UrhoXCLI build-anim-mappings -i Retarget/AnimationMappings.json -r C:/Project/Resources

# 输出：
# Loading model: Models/HumanoidA.mdl
#   humanoid_a: 65 bones
# Loading model: Models/HumanoidB.mdl
#   humanoid_b: 42 bones
# Updated 2 body types in Retarget/AnimationMappings.json

# 补全后的文件已包含完整的 referencePose
```

### 文件影响清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `RuntimeRetargeterCache.h` | **新增** | 子系统头文件 |
| `RuntimeRetargeterCache.cpp` | **新增** | 子系统实现（映射表加载 + 缓存 + 烘焙） |
| `AnimationController.cpp` | **修改** | Play / PlayExclusive 插入 GetOrBake 调用（各 ~5 行） |
| `Graphics/RegisterGraphicsLibrary` | **修改** | 注册 RuntimeRetargeterCache 子系统 |
| `BuildAnimMappingsCommand.h` | **新增** | CLI 命令头文件 |
| `BuildAnimMappingsCommand.cpp` | **新增** | CLI 命令实现（加载模型 + 补全骨架 + 写回 JSON） |
| `UrhoXCLI/main.cpp` | **修改** | 注册 build-anim-mappings 命令 |

### 验证要点

1. **编译通过**：UrhoXServer + UrhoXRuntime 零错误
2. **同模型播放**：sourceModel == targetModel 时，行为与改动前完全一致（无性能退化）
3. **跨模型播放**：sourceAnim 在 targetModel 上正确重定向，骨骼姿态与编辑器离线烘焙结果一致
4. **缓存生效**：同一动画第二次 Play 命中缓存，不重复烘焙（日志可验证）
5. **Fallback 正确**：映射表缺失的动画正常播放，不崩溃
6. **动画控制正常**：Stop / IsPlaying / SetSpeed 等接口通过原始动画名正常工作

---

*创建日期: 2026-03-26*
*关联文档: [animation-retargeting-design.md](./animation-retargeting-design.md)*
