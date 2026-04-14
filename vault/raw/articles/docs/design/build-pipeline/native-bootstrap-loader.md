---
summary: "Native platform (Windows/Android/iOS) bootstrap download system redesign with Pipeline + Step architecture"
related_paths:
  - tools/generators/**
last_updated: "2025-12-15"
---

# 原生启动加载器 v2 - Pipeline + Step 架构

本文档描述 UrhoX 原生平台（Windows/Android/iOS）启动下载系统的重构设计。

---

## 📋 目录

- [重构背景](#重构背景)
- [架构设计](#架构设计)
- [目录结构](#目录结构)
- [核心组件](#核心组件)
- [Step 详解](#step-详解)
- [错误处理与重试策略](#错误处理与重试策略)
- [平台差异处理](#平台差异处理)
- [数据流](#数据流)
- [扩展指南](#扩展指南)

---

## 重构背景

### 原有问题

1. **巨型类问题**：`BootstrapLoader` 类承担了所有阶段的逻辑（700+ 行），难以维护和扩展
2. **硬编码的阶段流程**：阶段转换通过 `EnterPhase` + `switch-case` 硬编码，添加新阶段需要修改多处
3. **平台差异难以处理**：不同平台需要不同流程时，需要大量条件判断
4. **职责不清晰**：下载、解析、更新检查等逻辑混杂在一起

### 设计目标

| 目标 | 说明 |
|------|------|
| **可扩展性** | 添加新阶段只需新增一个 Step 类 |
| **可配置性** | 每个 Step 的重试策略、权重等可独立配置 |
| **平台适配** | 工厂方法集中管理不同平台的启动流程 |
| **可测试性** | 每个 Step 可独立测试 |
| **松耦合** | 通过共享上下文传递数据，Step 之间不直接依赖 |

---

## 架构设计

### 核心模式：Pipeline + Step

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Pipeline + Step 架构                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   BootstrapManager（对外入口）                                              │
│        │                                                                    │
│        ▼                                                                    │
│   BootstrapPipeline（执行器）                                               │
│        │                                                                    │
│        ├── BootstrapContext（共享上下文）                                   │
│        │        ├── gameUrl, cacheRoot                                     │
│        │        ├── version, manifestHash                                  │
│        │        ├── gameManifest, sourceManifests                          │
│        │        ├── resolver                                               │
│        │        └── UI 回调、错误处理回调                                   │
│        │                                                                    │
│        └── Steps（步骤列表）                                                │
│             ├── LoadVersionStep                                            │
│             ├── LoadProjectManifestStep                                    │
│             ├── LoadSourceManifestsStep (可选)                             │
│             ├── DownloadInitialPackageStep (可选，首次启动时触发)           │
│             ├── LoadPreloadResourcesStep                                   │
│             ├── InitializeResourceRouterStep                                     │
│             └── CleanupStep                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 执行流程

```
Pipeline.Execute()
    │
    ├── 计算总权重
    │
    └── for each Step:
            │
            ├── ShouldSkip() ? ───▶ 跳过，继续下一个
            │
            ├── Execute()
            │     │
            │     ├── 成功 ─────────────────────────▶ 继续下一个
            │     │
            │     └── 失败
            │           │
            │           ├── 需要阻塞重试？
            │           │     └── 显示对话框 ─▶ 用户选择
            │           │           ├── 重试 ─▶ 重新执行当前 Step
            │           │           └── 退出 ─▶ 终止 Pipeline
            │           │
            │           └── 不需要阻塞重试
            │                 └── 打印报告，继续下一个
            │
            └── 更新总进度
```

---

## 目录结构

```
Bootstrap/
├── CMakeLists.txt              # 构建配置
├── Define.h                    # 导出宏定义
├── BootstrapContext.h          # 共享上下文
├── BootstrapPipeline.h/.cpp    # Pipeline 执行器
├── BootstrapManager.h/.cpp     # 对外入口（接口不变）
│
├── Steps/                      # 所有启动步骤
│   ├── IBootstrapStep.h        # 步骤基类接口
│   ├── LoadVersionStep.h/.cpp
│   ├── LoadProjectManifestStep.h/.cpp
│   ├── LoadSourceManifestsStep.h/.cpp
│   ├── DownloadInitialPackageStep.h/.cpp  # 首次启动整包下载
│   ├── LoadPreloadResourcesStep.h/.cpp
│   ├── InitializeResourceRouterStep.h/.cpp      # 初始化资源系统
│   └── CleanupStep.h/.cpp
│
├── Manifest/                   # Manifest 相关
│   ├── ManifestData.h/.cpp
│   ├── ManifestResolver.h/.cpp
│   └── ManifestResourceRouter.h/.cpp
│
└── UI/                         # UI 相关
    ├── LoadingUI.h/.cpp
    └── DialogUI.h/.cpp
```

---

## 核心组件

### IBootstrapStep（步骤基类）

```cpp
/// 启动步骤基类
class IBootstrapStep : public Object
{
    URHO3D_OBJECT(IBootstrapStep, Object);
    
public:
    using StepCallback = std::function<void(bool success, const String& error)>;
    
    /// 步骤名称（用于日志和调试）
    virtual String GetName() const = 0;
    
    /// 步骤权重（用于总进度计算，默认 1.0）
    virtual float GetWeight() const { return 1.0f; }
    
    /// 是否需要阻塞重试（失败后弹框让用户选择重试/退出）
    virtual bool RequiresBlockingRetry() const { return true; }
    
    /// 是否应该跳过此步骤
    virtual bool ShouldSkip() { return false; }
    
    /// 执行步骤
    virtual void Execute(StepCallback onComplete) = 0;
    
    /// 取消执行
    virtual void Cancel() {}
    
    /// 报告进度（0.0 - 1.0）
    void ReportProgress(float progress, const String& status = String::EMPTY);
    
    /// 设置共享上下文
    void SetContext(BootstrapContext* ctx) { ctx_ = ctx; }
    
protected:
    BootstrapContext* ctx_{nullptr};
};
```

### BootstrapContext（共享上下文）

```cpp
/// 启动流程共享上下文
/// 步骤之间通过此上下文传递数据
struct BootstrapContext
{
    // ========== 配置 ==========
    String gameUrl;           // 游戏资源 URL
    String cacheRoot;         // 本地缓存根目录
    unsigned concurrency{5};  // 下载并发数
    
    // ========== 状态数据 ==========
    String version;           // 版本号
    String manifestHash;      // manifest hash
    
    SharedPtr<ManifestData> gameManifest;                      // 游戏 manifest
    HashMap<String, SharedPtr<ManifestData>> sourceManifests;  // 依赖源 manifest
    SharedPtr<ManifestResolver> resolver;                      // 资源解析器
    
    // 需要下载的文件列表: {url, localPath}
    Vector<std::pair<String, String>> filesToDownload;
    uint64_t expectedTotalBytes{0};
    
    // 需要清理的文件列表
    Vector<String> filesToDelete;
    // 已加载完整 manifest 的 source 列表（只有这些才会在 Cleanup 阶段清理）
    HashSet<String> loadedSourcesWithFullManifest;
    
    // ========== 回调 ==========
    /// 进度报告：(totalProgress 0.0-1.0, status)
    std::function<void(float, const String&)> onProgress;
    
    /// 请求用户确认（阻塞重试）：(message, callback(retry))
    std::function<void(const String&, std::function<void(bool)>)> onConfirmRetry;
    
    /// 请求退出应用
    std::function<void()> onRequestExit;
};
```

### BootstrapPipeline（执行器）

```cpp
/// 启动流程 Pipeline
class BootstrapPipeline : public Object
{
    URHO3D_OBJECT(BootstrapPipeline, Object);
    
public:
    using PipelineCallback = std::function<void(bool success, const String& error)>;
    
    /// 添加步骤
    BootstrapPipeline* AddStep(SharedPtr<IBootstrapStep> step);
    
    /// 在指定步骤后插入
    BootstrapPipeline* InsertAfter(const String& afterName, SharedPtr<IBootstrapStep> step);
    
    /// 移除步骤
    BootstrapPipeline* RemoveStep(const String& name);
    
    /// 执行 Pipeline
    void Execute(PipelineCallback onComplete);
    
    /// 取消执行
    void Cancel();
    
    /// 获取共享上下文
    BootstrapContext* GetContext() { return &context_; }
    
private:
    void RunStep(unsigned index);
    void OnStepComplete(unsigned index, bool success, const String& error);
    void UpdateTotalProgress();
    
    Vector<SharedPtr<IBootstrapStep>> steps_;
    BootstrapContext context_;
    PipelineCallback onComplete_;
    unsigned currentStepIndex_{0};
    float totalWeight_{0.0f};
    bool isCancelled_{false};
};
```

---

## Step 详解

### LoadVersionStep

**职责**：加载版本信息

**子阶段**：
1. 下载并解析 `{tag}.json`（如 `latest.json`）
2. 下载并解析 `{version}/version.json`（锚定版本信息）

**输出**：
- `ctx->version`
- `ctx->manifestHash`

**重试策略**：阻塞重试（失败后弹框）

```cpp
class LoadVersionStep : public IBootstrapStep
{
public:
    String GetName() const override { return "LoadVersion"; }
    float GetWeight() const override { return 0.05f; }
    bool RequiresBlockingRetry() const override { return true; }
    
    void Execute(StepCallback onComplete) override;
    
private:
    void DownloadTagJson();
    void DownloadVersionJson();
};
```

### LoadProjectManifestStep

**职责**：加载项目（游戏）的 Manifest

**流程**：
1. 计算 manifest URL: `{gameUrl}/{version}/manifest-{hash}.json`
2. 优先读取本地缓存
3. 缓存未命中则下载
4. 解析并加载到 resolver

**输出**：
- `ctx->gameManifest`
- 更新 `ctx->resolver`

**重试策略**：阻塞重试

```cpp
class LoadProjectManifestStep : public IBootstrapStep
{
public:
    String GetName() const override { return "LoadProjectManifest"; }
    float GetWeight() const override { return 0.05f; }
    bool RequiresBlockingRetry() const override { return true; }
    
    void Execute(StepCallback onComplete) override;
};
```

### LoadSourceManifestsStep

**职责**：加载所有依赖源的 Manifest

**流程**：
1. 遍历 `gameManifest->sources`
2. 对每个远程 source：
   - 下载 `{base_url}/{tag}.json`
   - 下载 `{base_url}/{version}/manifest-{hash}.json`
   - 解析并加载到 resolver

**输出**：
- `ctx->sourceManifests`
- `ctx->loadedSourcesWithFullManifest`
- 更新 `ctx->resolver`

**特点**：
- 可选阶段（前期资源不大时可跳过）
- 某个 source 失败不影响其他

**重试策略**：阻塞重试（单个 source 失败时询问）

```cpp
class LoadSourceManifestsStep : public IBootstrapStep
{
public:
    String GetName() const override { return "LoadSourceManifests"; }
    float GetWeight() const override { return 0.08f; }
    bool RequiresBlockingRetry() const override { return true; }
    
    /// 设置是否跳过
    void SetEnabled(bool enabled) { enabled_ = enabled; }
    bool ShouldSkip() override { return !enabled_; }
    
    void Execute(StepCallback onComplete) override;
    
private:
    bool enabled_{true};
};
```

### DownloadInitialPackageStep

**职责**：首次启动时下载整包资源

**触发条件**：
- `ctx->needsFullPackageDownload == true`（本地无 manifest 时设置）
- `ctx->sourcesNeedingPackage` 非空

**流程**：
1. 遍历需要下载整包的 source 列表
2. 下载 `{base_url}/assets.7z?_t={timestamp}`（assets.7z 位于 CDN 根目录）
3. 使用 7z 库解压到 `{GetUrlLocalAbsPath(base_url)}/`
4. 删除下载的 7z 文件（节省空间）

**CDN 目录结构**：
```
CDN/
├── assets.7z                    # 整包（根目录，所有版本共用内容）
├── latest.json                  # 最新版本索引
└── {version}/
    ├── manifest-{hash}.json
    └── assets/
        └── {uuid}-{hash}.{ext}
```

**解压目录**：
- 7z 包内结构：`assets/{uuid}-{hash}.{ext}`
- project: 解压到 `{cacheRoot}/{gameUrl 去协议}/assets/`
- 其他 source: 解压到 `{cacheRoot}/{source.baseUrl 去协议}/assets/`

**输出**：
- 资源文件解压到本地缓存，路径与增量下载一致

**重试策略**：阻塞重试

```cpp
class DownloadInitialPackageStep : public IBootstrapStep
{
public:
    String GetName() const override { return "DownloadInitialPackage"; }
    float GetWeight() const override { return 0.50f; }
    bool RequiresBlockingRetry() const override { return true; }
    
    bool ShouldSkip() override {
        return !ctx_->needsFullPackageDownload || ctx_->sourcesNeedingPackage.Empty();
    }
    
    void Execute(StepCallback onComplete) override;
    
private:
    void DownloadPackage(const String& sourceName);
    bool Extract7z(const String& archivePath, const String& destDir);
};
```

**构建配置**：

在 `settings.json` 中配置自动生成阈值（默认 50）：

```json
{
  "build": {
    "assets_7z_threshold": 50
  }
}
```

构建命令：

```bash
# 自动判断（文件数 >= 50 时生成）
python project_builder.py --project ./MyGame

# 强制生成整包
python project_builder.py --project ./MyGame --7z

# 强制跳过整包生成
python project_builder.py --project ./MyGame --no-7z
```

### LoadPreloadResourcesStep

**职责**：下载预加载资源

**流程**：
1. 从 resolver 获取 preload 资源列表
2. 检查本地缓存，过滤出需要下载的
3. 批量并发下载
4. 报告下载进度

**输出**：
- 资源文件写入本地缓存

**重试策略**：非阻塞（失败的资源记录并打印报告，不阻塞流程）

```cpp
class LoadPreloadResourcesStep : public IBootstrapStep
{
public:
    String GetName() const override { return "LoadPreloadResources"; }
    float GetWeight() const override { return 0.60f; }
    bool RequiresBlockingRetry() const override { return false; }  // 资源缺失不阻塞
    
    void OnExecute() override;
    
private:
    void CalculateFilesToDownload();
    void StartDownload();
    void PrintCompletionReport(const Vector<FailedTaskInfo>& failed);
};
```

### InitializeResourceRouterStep

**职责**：初始化资源系统

**流程**：
1. 创建 `ManifestResourceRouter` 并注册到 `ResourceCache`
2. 添加缓存目录到资源路径

**输出**：
- `ctx->resourceRouter`：资源路由器实例

**重试策略**：阻塞重试（初始化失败则无法继续）

```cpp
class InitializeResourceRouterStep : public IBootstrapStep
{
public:
    String GetName() const override { return "InitializeResource"; }
    float GetWeight() const override { return 0.02f; }
    bool RequiresBlockingRetry() const override { return true; }
    
    void OnExecute() override;
};
```

### InitializeShaderCacheStep

**职责**：安装预编译 shader 缓存

**流程**：
1. 根据平台确定 shader cache 包名（dx11/essl/metal/glsl）
2. 在资源目录中搜索 `shadercache_runtime/{packageName}`
3. 加载 shader cache 包到 ResourceCache

**平台包名**：
| 平台 | 包名 |
|------|------|
| Windows | `shadercache_dx11.pak` |
| Android | `shadercache_essl.pak` |
| iOS | `shadercache_metal.pak` |
| Web | `shadercache_essl.pak` |
| Linux | `shadercache_glsl.pak` |

**重试策略**：非阻塞（加载失败不影响启动，只是首次运行会编译 shader）

```cpp
class InitializeShaderCacheStep : public IBootstrapStep
{
public:
    String GetName() const override { return "InstallShaderCache"; }
    float GetWeight() const override { return 0.02f; }
    bool RequiresBlockingRetry() const override { return false; }
    
    void OnExecute() override;
    
private:
    String GetPlatformPackageName() const;
};
```

### CleanupStep

**职责**：清理本地无用缓存

**规则**：
- 对于每个已加载完整 manifest 的 source
- 扫描对应的 `assets/` 目录
- 删除不在当前 manifest 中的文件

**触发条件**：
- 仅当 `ctx->loadedSourcesWithFullManifest` 非空时执行

**重试策略**：非阻塞（清理失败不影响启动）

```cpp
class CleanupStep : public IBootstrapStep
{
public:
    String GetName() const override { return "Cleanup"; }
    float GetWeight() const override { return 0.05f; }
    bool RequiresBlockingRetry() const override { return false; }
    
    bool ShouldSkip() override {
        return ctx_->loadedSourcesWithFullManifest.Empty();
    }
    
    void Execute(StepCallback onComplete) override;
    
private:
    void ScanAndCleanSource(const String& source);
};
```

---

## 错误处理与重试策略

### 策略类型

| 策略 | 适用场景 | 行为 |
|------|---------|------|
| **阻塞重试** | Manifest 下载/解析 | 失败后弹框，用户选择"重试"或"退出" |
| **非阻塞** | 资源下载、缓存清理 | 失败后打印报告，继续执行 |

### 配置方式

每个 Step 通过 `RequiresBlockingRetry()` 声明自己的策略：

```cpp
class LoadVersionStep : public IBootstrapStep
{
    bool RequiresBlockingRetry() const override { return true; }  // 阻塞重试
};

class LoadPreloadResourcesStep : public IBootstrapStep
{
    bool RequiresBlockingRetry() const override { return false; } // 非阻塞
};
```

### 阻塞重试流程

```
Step.Execute() 失败
    │
    └── RequiresBlockingRetry() == true
            │
            ▼
        ctx_->onConfirmRetry(message, callback)
            │
            ├── 显示 DialogUI
            │
            └── 用户选择
                    ├── "重试" ─▶ 重新执行 Step.Execute()
                    └── "退出" ─▶ ctx_->onRequestExit()
```

### 非阻塞流程

```
Step.Execute() 失败
    │
    └── RequiresBlockingRetry() == false
            │
            ▼
        打印失败报告（日志 + 可选 UI 提示）
            │
            ▼
        继续执行下一个 Step
```

---

## 平台差异处理

### 平台检测

使用编译时宏判断平台：

```cpp
#if defined(__EMSCRIPTEN__)
    #define BOOTSTRAP_PLATFORM_WEB
#elif defined(__ANDROID__)
    #define BOOTSTRAP_PLATFORM_ANDROID
#elif defined(__APPLE__)
    #include <TargetConditionals.h>
    #if TARGET_OS_IOS
        #define BOOTSTRAP_PLATFORM_IOS
    #else
        #define BOOTSTRAP_PLATFORM_MACOS
    #endif
#elif defined(_WIN32)
    #define BOOTSTRAP_PLATFORM_WINDOWS
#else
    #define BOOTSTRAP_PLATFORM_LINUX
#endif
```

### 平台特定 Pipeline 配置

```cpp
SharedPtr<BootstrapPipeline> BootstrapManager::CreatePipeline()
{
    auto pipeline = MakeShared<BootstrapPipeline>(context_);
    
#ifdef BOOTSTRAP_PLATFORM_WEB
    // WebGL：资源已打包，流程简化
    pipeline
        ->AddStep(MakeShared<LoadBundledManifestStep>(context_));
        
#else
    // 原生平台：完整流程
    pipeline
        ->AddStep(MakeShared<LoadVersionStep>(context_))
        ->AddStep(MakeShared<LoadProjectManifestStep>(context_))
        ->AddStep(MakeShared<LoadSourceManifestsStep>(context_))
        ->AddStep(MakeShared<DownloadInitialPackageStep>(context_))  // 首次启动整包下载
        ->AddStep(MakeShared<LoadPreloadResourcesStep>(context_))
        ->AddStep(MakeShared<InitializeResourceRouterStep>(context_))      // 初始化资源系统
        ->AddStep(MakeShared<CleanupStep>(context_));
        
#ifdef BOOTSTRAP_PLATFORM_ANDROID
    // Android 可能需要额外的权限检查
    // pipeline->InsertBefore("LoadVersion", MakeShared<RequestPermissionStep>(context_));
#endif

#endif

    return pipeline;
}
```

---

## 数据流

### 步骤间数据传递

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           数据流                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LoadVersionStep                                                             │
│      │                                                                       │
│      ├── 读取: ctx->gameUrl                                                 │
│      └── 写入: ctx->version, ctx->manifestHash                              │
│                    │                                                         │
│                    ▼                                                         │
│  LoadProjectManifestStep                                                     │
│      │                                                                       │
│      ├── 读取: ctx->gameUrl, ctx->version, ctx->manifestHash                │
│      └── 写入: ctx->gameManifest, ctx->resolver                             │
│                    │                                                         │
│                    ▼                                                         │
│  LoadSourceManifestsStep                                                     │
│      │                                                                       │
│      ├── 读取: ctx->gameManifest->sources, ctx->cacheRoot                   │
│      └── 写入: ctx->sourceManifests, ctx->loadedSourcesWithFullManifest     │
│               ctx->needsFullPackageDownload, ctx->sourcesNeedingPackage     │
│                    │                                                         │
│                    ▼                                                         │
│  DownloadInitialPackageStep（首次启动时触发）                                 │
│      │                                                                       │
│      ├── 读取: ctx->sourcesNeedingPackage, ctx->gameUrl, ctx->version       │
│      └── 写入: 解压资源到本地缓存目录                                         │
│                    │                                                         │
│                    ▼                                                         │
│  LoadPreloadResourcesStep                                                    │
│      │                                                                       │
│      ├── 读取: ctx->resolver->GetPreloadFiles(), ctx->cacheRoot             │
│      └── 写入: 文件到本地缓存目录                                            │
│                    │                                                         │
│                    ▼                                                         │
│  InitializeResourceRouterStep                                                      │
│      │                                                                       │
│      ├── 读取: ctx->resolver, ctx->cacheRoot                                │
│      └── 写入: ctx->resourceRouter, 注册到 ResourceCache                    │
│                    │                                                         │
│                    ▼                                                         │
│  CleanupStep                                                                 │
│      │                                                                       │
│      ├── 读取: ctx->loadedSourcesWithFullManifest, ctx->resolver            │
│      └── 写入: 删除废弃文件                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 进度计算

```
总进度 = Σ(已完成步骤权重 + 当前步骤权重 × 当前步骤进度) / 总权重

例如（首次启动，需要下载整包）：
- LoadVersionStep (0.05) - 完成
- LoadProjectManifestStep (0.05) - 完成
- LoadSourceManifestsStep (0.08) - 完成
- DownloadInitialPackageStep (0.50) - 进行中，60%
- LoadPreloadResourcesStep (0.60) - 未开始
- InitializeResourceRouterStep (0.02) - 未开始
- CleanupStep (0.05) - 未开始

总权重 = 0.05 + 0.05 + 0.08 + 0.50 + 0.60 + 0.02 + 0.02 + 0.05 = 1.37
当前进度 = (0.05 + 0.05 + 0.08 + 0.50 × 0.6) / 1.37 = 0.35 (35%)

**进度条平滑过渡**：LoadingUI 会限制进度条最大增长速度（默认 0.5/秒），
当步骤被跳过时进度条会平滑过渡而非跳跃。
```

---

## 扩展指南

### 添加新步骤

1. 创建新的 Step 类：

```cpp
// Steps/MyNewStep.h
class MyNewStep : public IBootstrapStep
{
    URHO3D_OBJECT(MyNewStep, IBootstrapStep);
    
public:
    explicit MyNewStep(Context* context) : IBootstrapStep(context) {}
    
    String GetName() const override { return "MyNewStep"; }
    float GetWeight() const override { return 0.1f; }
    bool RequiresBlockingRetry() const override { return false; }
    
    void Execute(StepCallback onComplete) override
    {
        // 实现逻辑
        ReportProgress(0.5f, "Processing...");
        
        // 完成
        onComplete(true, String::EMPTY);
    }
};
```

2. 在 Pipeline 中添加：

```cpp
pipeline->AddStep(MakeShared<MyNewStep>(context_));
// 或
pipeline->InsertAfter("LoadProjectManifest", MakeShared<MyNewStep>(context_));
```

### 动态调整流程

```cpp
// 根据条件移除步骤
if (IsOfflineMode())
{
    pipeline->RemoveStep("LoadSourceManifests");
}

// 根据条件插入步骤
if (IsFirstLaunch())
{
    pipeline->InsertBefore("LoadVersion", MakeShared<ShowWelcomeStep>(context_));
}
```

### 自定义重试策略

可以在 Step 中实现更复杂的重试逻辑：

```cpp
class CustomRetryStep : public IBootstrapStep
{
public:
    void Execute(StepCallback onComplete) override
    {
        DoWork([this, onComplete](bool success, const String& error) {
            if (!success && retryCount_ < maxRetries_)
            {
                ++retryCount_;
                // 延迟重试
                ScheduleRetry([this, onComplete]() {
                    Execute(onComplete);
                }, GetRetryDelay());
                return;
            }
            
            onComplete(success, error);
        });
    }
    
private:
    unsigned retryCount_{0};
    unsigned maxRetries_{3};
    
    unsigned GetRetryDelay() const
    {
        // 指数退避: 1s, 2s, 4s
        return 1000 * (1 << retryCount_);
    }
};
```

---

## 相关文档

- [native-bootstrap-loader.md](./native-bootstrap-loader.md) - 原始设计（v1）
- [INDEX.md](./INDEX.md) - 构建流程
- [resource-uuid-design.md](./resource-uuid-design.md) - UUID 设计

---

*最后更新: 2025-12-15*
