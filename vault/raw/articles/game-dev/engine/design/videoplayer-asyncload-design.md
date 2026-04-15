---
summary: "VideoPlayer async loading design to avoid main thread blocking on HTTPS video sources"
related_paths:
  - engine/Source/Urho3D/Video/**
last_updated: "2026-04-02"
---

# VideoPlayer AsyncLoad 异步加载设计方案

## 一、背景与动机

### 现状

`VideoPlayer::Load()` 在 Native 平台（Windows/Linux/Android/iOS）上是**同步阻塞**的，对于 HTTPS URL 视频源，主线程会被阻塞在网络连接、TLS 握手、格式探测等操作上。WASM 平台例外——浏览器 `<video>` 元素天然异步加载。

各平台 `Load()` 阻塞点分析：

| 平台 | 后端 | 阻塞操作 |
|------|------|----------|
| **FFmpeg** (Win/Linux/macOS) | `avformat_open_input` + `avformat_find_stream_info` | TCP+TLS+HTTP+格式探测 |
| **Android** (MediaCodec NDK) | `AMediaExtractor_setDataSource(url)` × 2（video+audio 各一个 extractor） | HTTP 连接+格式探测，执行两次 |
| **iOS** (AVFoundation) | `AVAsset loadValuesAsynchronouslyForKeys` + `dispatch_semaphore_wait` | 系统 API 本身异步，但代码用 semaphore 强制等成同步（超时 10s） |
| **WASM** (HTML5 Video) | 无阻塞 | `<video preload="auto">` 天然异步 |

### 目标

新增 `AsyncLoad()` 接口，将 `Load()` 的网络 I/O 和格式探测操作通过 `BackgroundWorkQueue` 线程池执行，主线程不阻塞。加载完成后通过 C++ 回调和可选的 Lua 回调通知调用方，同时 `IsReady()` 也会返回 true。

**保持 `Load()` 接口不变**，兼容现有代码。

---

## 二、API 设计

### C++ 接口

```cpp
/// Callback type for async load completion.
/// @param success True if loading succeeded, false on failure.
using AsyncLoadCallback = std::function<void(bool success)>;

class URHO3D_API VideoPlayer : public Object
{
public:
    // 现有接口（保持不变）
    bool Load(const String& source, int width = 1920, int height = 1080);
    void Play();
    bool IsReady() const;

    // === 新增接口 ===

    /// Asynchronously load video from URL/path.
    /// Loading happens on BackgroundWorkQueue (native) or natively async (WASM).
    /// @param source Video URL or path.
    /// @param width Initial texture width.
    /// @param height Initial texture height.
    /// @param callback Optional completion callback, called on main thread.
    void AsyncLoad(const String& source, int width = 1920, int height = 1080,
                   const AsyncLoadCallback& callback = nullptr);

    /// Return whether async loading is in progress.
    bool IsAsyncLoading() const { return asyncLoading_; }
};
```

### Lua 接口

```lua
--- 异步加载视频（立即返回，不阻塞主线程）
--- @param source string 视频 URL 或路径
--- @param width? number 纹理宽度（默认 1920）
--- @param height? number 纹理高度（默认 1080）
--- @param callback? function 加载完成回调 function(success: boolean)
function VideoPlayer:AsyncLoad(source, width, height, callback) end

--- 是否正在异步加载中
--- @return boolean
function VideoPlayer:IsAsyncLoading() end

--- 是否已就绪（同步 Load 或异步 AsyncLoad 完成后为 true）
--- @return boolean
function VideoPlayer.ready  -- 已有属性，语义不变
```

### 使用示例

```lua
local player = VideoPlayer()

-- 方式 1: 回调
player:AsyncLoad("https://cdn.example.com/video.mp4", 0, 0, function(success)
    if success then
        player:Play()
    else
        print("Video load failed")
    end
end)

-- 方式 2: 轮询 ready
player:AsyncLoad("https://cdn.example.com/video.mp4")

function Update(dt)
    player:Update()
    if player.ready and not player.playing then
        player:Play()
    end
end

-- 同步加载（原有，保持不变）
player:Load("https://cdn.example.com/video.mp4")
player:Play()
```

### C++ 使用示例

```cpp
auto* player = new VideoPlayer(context_);
player->AsyncLoad("https://cdn.example.com/video.mp4", 1920, 1080,
    [player](bool success) {
        if (success)
            player->Play();
        else
            URHO3D_LOGERROR("Video async load failed");
    });
```

---

## 三、`IsReady()` 语义统一

各平台 `IsReady()` 当前行为和 AsyncLoad 后的行为：

| 场景 | 当前行为 | AsyncLoad 后行为 |
|------|----------|-----------------|
| Native Load 未调用 | false | false |
| Native Load 成功返回 | true（立即） | true（不变） |
| Native AsyncLoad 调用中 | — | false |
| Native AsyncLoad 完成 | — | true |
| Native AsyncLoad 失败 | — | false |
| WASM Load 调用后 | 异步变 true（`readyState >= HAVE_CURRENT_DATA`） | 不变 |

Native 平台 `IsReady()` 修改：

```cpp
bool VideoPlayer::IsReady() const
{
    if (asyncLoading_)
        return false;
    return decoder_ && decoder_->IsOpen();
}
```

---

## 四、内部实现

> **实现原则：最小 diff**
> 拆分 `Load()` 时只做代码剪切/移动，保持原始格式（缩进、注释、空行、变量名）不变。不做任何格式调整、变量重命名或注释改写。目的是保持 `git blame` 可追溯。

### 4.1 异步加载数据结构

使用独立的数据结构持有后台任务的输入、输出和生命周期，遵循引擎 `BackgroundWorkQueue` 的 `selfRef_` 模式：

```cpp
/// Data shared between main thread and background worker.
struct AsyncLoadData
{
    // === 输入（主线程写入，后台线程只读）===
    String resolvedSource;
    int width{0};
    int height{0};
    SharedPtr<VideoDecoder> decoder;  // 主线程创建，后台线程调 Open

    // === 输出（后台线程写入，主线程在 completed 后读取）===
    int videoWidth{0};
    int videoHeight{0};
    bool success{false};

    // === 控制标志 ===
    volatile bool completed{false};   // 后台线程设为 true，主线程读取
    volatile bool cancelled{false};   // 主线程设为 true，后台线程检查后提前退出

    // === 生命周期（防止任务执行期间数据被释放）===
    std::shared_ptr<AsyncLoadData> selfRef;
};
```

### 4.2 Load 函数重构

将现有 `Load()` 拆分为 `PrepareLoad()` + `FinalizeLoad()`，AsyncLoad 复用这两段逻辑。

**最小改动原则**：拆分时只做代码剪切/移动，保持原始格式（缩进、注释、空行）不变，确保 git blame 可追溯。

#### 拆分方式

原始 `Load()` 代码（VideoPlayer.cpp:663-785）按行号剪切为三段：

| 新函数 | 原始行号 | 内容 |
|--------|---------|------|
| `PrepareLoad()` | 665-721 | 清理旧状态 + 创建 decoder + 解析 URL |
| `Load()` 中间 | 723-729 | `decoder_->Open()` 阻塞调用（不拆出） |
| `FinalizeLoad()` | 731-785 | 获取尺寸 + 初始化纹理 + 创建解码线程 + 创建音频 |

#### PrepareLoad

从 `Load()` 中剪切 665-721 行，**保持原始代码不变**，仅在开头新增 `CancelAsyncLoad()` 调用，末尾新增 `source_ = source`（原来在 731 行）：

```cpp
/// Prepare for loading: clean up previous state, create decoder, resolve URL.
/// Shared by Load() and AsyncLoad().
bool VideoPlayer::PrepareLoad(const String& source, String& resolvedSource)
{
    // Cancel any in-progress async load
    CancelAsyncLoad();

    // === 以下从 Load() 665-721 行原样剪切 ===

    // Clean up previous playback
    Stop();

    // Clean up previous resources
    if (decodeThread_)
    {
        decodeThread_->Stop();
        decodeThread_.Reset();
    }
    if (audioSource_)
    {
        audioSource_->Stop();
        audioSource_.Reset();
    }
    audioStream_.Reset();
    audioNode_.Reset();
    decoder_.Reset();

    // Reset state
    metadataLoaded_ = false;
    actualVideoWidth_ = 0;
    actualVideoHeight_ = 0;
    state_ = VIDEO_STOPPED;
    pendingFrame_ = nullptr;
    lastVideoPts_ = 0;

    // Create decoder
    decoder_ = VideoDecoder::Create(context_);
    if (!decoder_)
    {
        URHO3D_LOGERROR("VideoPlayer: Failed to create decoder");
        return false;
    }

    // Resolve source path
    resolvedSource = source;
    if (!source.StartsWith("http://") && !source.StartsWith("https://"))
    {
        // Not a URL, try to resolve via ResourceCache
        auto* cache = GetSubsystem<ResourceCache>();
        if (cache)
        {
            String resourcePath = cache->RouteResourcePath(source);
            String fullPath = cache->GetResourceFileName(resourcePath);
            if (!fullPath.Empty())
                resolvedSource = fullPath;
            else
            {
                resolvedSource = cache->RouteResourceURL(source);
                if (resolvedSource == source)
                {
                    URHO3D_LOGERRORF("VideoPlayer: Asset not found, source='%s'. Please check if the file exists locally or has been downloaded.", source.CString());
                    return false;
                }
            }
        }
    }

    // === 剪切结束 ===

    source_ = source;
    return true;
}
```

#### FinalizeLoad

从 `Load()` 中剪切 731-785 行，**保持原始代码不变**（`source_` 赋值已移到 `PrepareLoad`）：

```cpp
/// Finalize loading after decoder Open: init texture, decode thread, audio.
/// Shared by Load() and FinalizeAsyncLoad().
bool VideoPlayer::FinalizeLoad(int width, int height)
{
    // === 以下从 Load() 733-785 行原样剪切 ===

    // Get actual video dimensions
    actualVideoWidth_ = decoder_->GetVideoWidth();
    actualVideoHeight_ = decoder_->GetVideoHeight();
    metadataLoaded_ = true;

    // Use actual video dimensions if specified dimensions are 0
    int texWidth = (width > 0) ? width : actualVideoWidth_;
    int texHeight = (height > 0) ? height : actualVideoHeight_;

    // Initialize texture
    if (!texture_->Initialize(texWidth, texHeight))
    {
        URHO3D_LOGERROR("VideoPlayer: Failed to initialize texture");
        decoder_.Reset();
        return false;
    }

    // Create background decode thread for VIDEO ONLY
    // Audio is decoded in SDL audio thread via VideoAudioStream for lowest latency
    decodeThread_ = new VideoDecodeThread();
    decodeThread_->SetDecoder(decoder_);
    decodeThread_->SetMaxVideoQueueSize(15);  // 15 frames (~0.5s at 30fps)

    // Setup audio stream using DIRECT decoder access (new architecture)
    // Audio decoding happens in SDL audio callback thread, independent of video
    audioStream_ = new VideoAudioStream();
    audioStream_->SetDecoder(decoder_);  // Direct decode mode for audio

    // Update audio format based on decoder
    if (decoder_->HasAudio())
    {
        unsigned sampleRate = decoder_->GetAudioSampleRate();
        unsigned channels = decoder_->GetAudioChannels();
        if (sampleRate > 0 && channels > 0)
        {
            audioStream_->SetFormat(sampleRate, true, channels == 2);
        }
    }

    // Create a temporary node to hold the SoundSource component
    audioNode_ = new Node(context_);
    audioSource_ = audioNode_->CreateComponent<SoundSource>();
    if (audioSource_)
    {
        audioSource_->SetGain(muted_ ? 0.0f : volume_);
    }

    URHO3D_LOGINFOF("VideoPlayer: Loaded '%s' (%dx%d @ %.2ffps, duration: %.2fs, audio: %s, threaded decode)",
        source_.CString(), actualVideoWidth_, actualVideoHeight_,
        decoder_->GetFrameRate(), decoder_->GetDuration(),
        decoder_->HasAudio() ? "yes" : "no");

    // === 剪切结束 ===

    return true;
}
```

#### 重构后的 Load()

```cpp
bool VideoPlayer::Load(const String& source, int width, int height)
{
    String resolvedSource;
    if (!PrepareLoad(source, resolvedSource))
        return false;

    // 同步打开（阻塞点）
    if (!decoder_->Open(resolvedSource))
    {
        URHO3D_LOGERRORF("VideoPlayer: Failed to open '%s'", source.CString());
        decoder_.Reset();
        return false;
    }

    return FinalizeLoad(width, height);
}
```

### 4.3 VideoPlayer 新增成员

```cpp
private:
    // === Async loading state ===

    /// Whether async loading is in progress.
    bool asyncLoading_{false};

    /// Whether Play() was called during async loading (deferred play).
    bool pendingPlay_{false};

    /// Shared data for background work item.
    std::shared_ptr<AsyncLoadData> asyncLoadData_;

    /// Work item submitted to BackgroundWorkQueue.
    SharedPtr<WorkItem> asyncWorkItem_;

    /// Completion callback, called on main thread when async load finishes.
    /// Lua 回调也通过此字段传入（Lua 绑定层将 LuaFunction 包装为 std::function）。
    AsyncLoadCallback asyncLoadCallback_;

    /// Finalize async load results on main thread.
    bool FinalizeAsyncLoad();

    /// Cancel any in-progress async load.
    void CancelAsyncLoad();

    /// Static work function for BackgroundWorkQueue.
    static void AsyncLoadWorkFunction(const WorkItem* item, unsigned threadIndex);
```

### 4.4 使用 BackgroundWorkQueue

```cpp
void VideoPlayer::AsyncLoad(const String& source, int width, int height,
                            const AsyncLoadCallback& callback)
{
    // 复用 PrepareLoad：清理旧状态 + 创建 decoder + 解析 URL
    String resolvedSource;
    if (!PrepareLoad(source, resolvedSource))
    {
        if (callback)
            callback(false);
        return;
    }

    // 保存回调
    asyncLoadCallback_ = callback;

    // 构造异步加载数据
    auto data = std::make_shared<AsyncLoadData>();
    data->resolvedSource = resolvedSource;
    data->width = width;
    data->height = height;
    data->decoder = decoder_;  // PrepareLoad 已创建好，后台线程只调 Open
    decoder_.Reset();          // 转移所有权！主线程不再持有 decoder 引用
                               // 避免析构时 SharedPtr refcount 被两个线程同时修改（数据竞争）
    data->selfRef = data;      // 自引用，防止任务执行期间被释放
    asyncLoadData_ = data;

    // 提交到 BackgroundWorkQueue
    auto* bgQueue = GetSubsystem<BackgroundWorkQueue>();
    if (!bgQueue)
    {
        URHO3D_LOGERROR("VideoPlayer: BackgroundWorkQueue not available");
        decoder_.Reset();
        if (callback)
            callback(false);
        return;
    }

    asyncWorkItem_ = bgQueue->GetFreeItem();
    asyncWorkItem_->workFunction_ = AsyncLoadWorkFunction;
    asyncWorkItem_->aux_ = data.get();
    asyncWorkItem_->priority_ = 0;
    asyncWorkItem_->sendEvent_ = false;

    asyncLoading_ = true;
    bgQueue->AddWorkItem(asyncWorkItem_);
}
```

### 4.5 后台 Work Function

静态函数，在 BackgroundWorkQueue 的工作线程中执行：

```cpp
void VideoPlayer::AsyncLoadWorkFunction(const WorkItem* item, unsigned threadIndex)
{
    auto* data = static_cast<AsyncLoadData*>(item->aux_);

    // 检查是否已被取消（Open 前检查，因为 Open 可能耗时很长）
    if (data->cancelled)
    {
        data->completed = true;
        data->selfRef.reset();
        return;
    }

    // 打开视频源（耗时操作：网络连接 + TLS 握手 + 格式探测）
    // decoder 已在主线程创建好，这里只调 Open
    if (!data->decoder->Open(data->resolvedSource))
    {
        data->success = false;
        data->completed = true;
        data->selfRef.reset();
        return;
    }

    // 成功：记录视频尺寸
    data->videoWidth = data->decoder->GetVideoWidth();
    data->videoHeight = data->decoder->GetVideoHeight();
    data->success = true;
    data->completed = true;
    data->selfRef.reset();  // 释放自引用
}
```

### 4.6 主线程轮询与 Finalize

在 `Update()` 中每帧检查后台任务是否完成：

```cpp
void VideoPlayer::Update()
{
    // 检查异步加载是否完成
    if (asyncLoading_ && asyncLoadData_ && asyncLoadData_->completed)
    {
        if (asyncLoadData_->success)
        {
            FinalizeAsyncLoad();
        }
        else
        {
            // 加载失败
            URHO3D_LOGERRORF("VideoPlayer: Async load failed for '%s'",
                source_.CString());
            asyncLoading_ = false;

            // 触发回调（C++ 或 Lua 包装的 std::function）
            if (asyncLoadCallback_)
            {
                asyncLoadCallback_(false);
                asyncLoadCallback_ = nullptr;
            }
        }

        // 清理
        asyncLoadData_.reset();
        asyncWorkItem_.Reset();
    }

    // ... 原有 Update 逻辑（UpdateVideoFrame 等）...
}
```

`FinalizeAsyncLoad()` 在主线程执行，复用 `FinalizeLoad()` 完成 GPU 和音频初始化：

```cpp
bool VideoPlayer::FinalizeAsyncLoad()
{
    if (!asyncLoadData_ || !asyncLoadData_->decoder)
        return false;

    // 从后台任务接收 decoder 所有权（AsyncLoad 中已 Reset decoder_）
    decoder_ = asyncLoadData_->decoder;
    asyncLoadData_->decoder.Reset();

    // 复用 FinalizeLoad 初始化 texture/thread/audio
    bool success = FinalizeLoad(asyncLoadData_->width, asyncLoadData_->height);

    // 异步加载完成后立即启动解码线程，预缓冲帧数据
    // 这样 Play() 时不需要等待缓冲，可以零延迟播放
    if (success && decodeThread_)
        decodeThread_->Start();

    asyncLoading_ = false;

    // 失败时先清理 decoder，再触发回调
    // 因为 Lua 回调中可能直接调 Load()，需要保证状态干净
    if (!success)
        decoder_.Reset();

    // 触发回调（C++ 或 Lua 包装的 std::function）
    if (asyncLoadCallback_)
    {
        asyncLoadCallback_(success);
        asyncLoadCallback_ = nullptr;
    }

    return success;
}
```

### 4.7 取消异步加载

```cpp
void VideoPlayer::CancelAsyncLoad()
{
    if (!asyncLoading_)
        return;

    // 设置取消标志，后台任务检查后提前退出
    if (asyncLoadData_)
        asyncLoadData_->cancelled = true;

    // 不阻塞等待后台任务完成，直接释放主线程侧的引用。
    // 安全性保证：
    //   - asyncLoadData_ 是 std::shared_ptr，引用计数原子操作，跨线程 reset 安全
    //   - 后台任务通过 selfRef 持有 AsyncLoadData，任务结束后自行释放
    //   - decoder 所有权已在 AsyncLoad 中转移给 data->decoder（decoder_ 已 Reset），
    //     后台任务结束时 selfRef.reset() → AsyncLoadData 析构 → decoder 释放
    //   - AsyncLoadWorkFunction 是静态函数，不访问 VideoPlayer 成员，
    //     VideoPlayer 析构后后台任务继续执行不会有问题
    asyncLoading_ = false;
    pendingPlay_ = false;
    asyncLoadData_.reset();
    asyncWorkItem_.Reset();
    asyncLoadCallback_ = nullptr;
}
```

### 4.8 Play() 中处理异步状态

Native 和 WASM 的 `Play()` 是两个独立函数（VideoPlayer.cpp 中通过 `#ifdef __EMSCRIPTEN__` 分开）。

**设计原则**：`AsyncLoad` 的意义就是不阻塞，`Play()` 不应该在异步加载期间阻塞等待（否则和直接用 `Load()` 没区别）。全平台行为统一：异步加载期间调 `Play()`，设置 `pendingPlay_` 标志，加载完成后自动播放。

新增成员变量：

```cpp
/// Whether Play() was called during async loading (deferred play).
bool pendingPlay_{false};
```

Native 版 `Play()`（line 788）新增开头：

```cpp
void VideoPlayer::Play()
{
    // 异步加载期间：不阻塞，标记待播放，加载完成后自动 Play
    if (asyncLoading_)
    {
        pendingPlay_ = true;
        return;
    }

    // ... 原有 Play 逻辑 ...
}
```

`FinalizeAsyncLoad()` 成功后检查 `pendingPlay_`：

```cpp
bool VideoPlayer::FinalizeAsyncLoad()
{
    // ... FinalizeLoad + decodeThread_->Start() ...

    asyncLoading_ = false;

    if (!success)
        decoder_.Reset();

    if (asyncLoadCallback_)
    {
        asyncLoadCallback_(success);
        asyncLoadCallback_ = nullptr;
    }

    // 延迟播放：AsyncLoad 期间调了 Play()，现在加载完成，自动播放
    if (success && pendingPlay_)
    {
        pendingPlay_ = false;
        Play();
    }

    return success;
}
```

WASM 的 `Play()`（line 500）不需要改动——WASM 的 `AsyncLoad()` 直接调 `Load()` 创建 `<video>` 元素，`Play()` 调用 `<video>.play()`，浏览器自行处理缓冲。

---

## 五、析构函数处理

析构时必须确保后台任务不会访问已销毁的 VideoPlayer 对象。

关键点：`AsyncLoadWorkFunction` 通过 `AsyncLoadData*` 访问数据，**不访问 VideoPlayer 成员**（静态函数 + 独立数据结构），所以析构安全性取决于 `AsyncLoadData` 的生命周期。

```cpp
VideoPlayer::~VideoPlayer()
{
    // 取消异步加载（非阻塞，后台任务通过 selfRef 自行清理）
    CancelAsyncLoad();

#ifdef __EMSCRIPTEN__
    if (videoId_ >= 0)
        js_destroyVideo(videoId_);
#else
    // ... 原有清理逻辑 ...
    if (pendingFrame_ && decodeThread_)
    {
        decodeThread_->ReleaseVideoFrame(pendingFrame_);
        pendingFrame_ = nullptr;
    }
    if (decodeThread_)
    {
        decodeThread_->Stop();
        decodeThread_.Reset();
    }
    if (audioSource_)
    {
        audioSource_->Stop();
        audioSource_.Reset();
    }
    audioStream_.Reset();
    audioNode_.Reset();
    decoder_.Reset();
#endif
}
```

### 析构安全性分析

```
场景：VideoPlayer 析构时后台任务仍在运行

析构函数调用 CancelAsyncLoad():
  1. asyncLoadData_->cancelled = true        ← 通知后台任务提前退出
  2. asyncLoadData_.reset()                  ← 主线程释放引用（非阻塞）
  3. asyncWorkItem_.Reset()                  ← 主线程释放引用

后台任务（AsyncLoadWorkFunction）：
  - 不访问 VideoPlayer 的任何成员变量（静态函数）
  - 只通过 AsyncLoadData* (item->aux_) 操作
  - selfRef (std::shared_ptr) 保证 AsyncLoadData 在任务执行期间不被释放
  - decoder 所有权已转移给 data->decoder，VideoPlayer 析构时 decoder_ 为空

因此：
  - VideoPlayer 析构后，后台任务继续执行，只访问 AsyncLoadData（selfRef 保活）
  - 任务结束时 selfRef.reset() → AsyncLoadData 析构 → data->decoder 释放
  - 全程无 VideoPlayer 成员访问，无数据竞争
  - 安全 ✓
```

### 后续优化（可选）

可为 FFmpeg 添加 `interrupt_callback`，在其中检查 `cancelled` 标志，让 `decoder->Open()` 在网络阻塞中提前退出，减少后台任务的残留时间。

---

## 六、各平台实现细节

### 6.1 FFmpeg (Windows/Linux/macOS)

最简单，FFmpeg API 线程安全，`AsyncLoadWorkFunction` 无需特殊处理。

`FFmpegDecoder::Open()` 内部已启动 `PacketReadThread`（读 packet 的后台线程），所以 async load 完成后 packet 队列已在填充。

### 6.2 Android (MediaCodec NDK)

注意点：
- `AMediaExtractor_setDataSource` 线程安全
- `AMediaCodec_configure/start` 线程安全
- **JNI 线程安全**：`OpenNetworkSource()` 使用 `SDL_AndroidGetJNIEnv()`，SDL 内部对非主线程会自动调用 JVM `AttachCurrentThread`（将原生线程注册到 JVM），BackgroundWorkQueue 的工作线程同样适用，无需额外处理

### 6.3 iOS (AVFoundation)

iOS 的 `AVAsset loadValuesAsynchronouslyForKeys` 本身是异步 API，当前代码用 semaphore 强制等成同步。

**采用方案 A**：复用现有同步 `Open()`，在 BackgroundWorkQueue 工作线程中执行。semaphore 阻塞发生在工作线程，不影响主线程。

优点：
- 实现一致性（所有 Native 平台同一套 WorkFunction）
- 改动最小

**后续可优化为方案 B**：去掉 semaphore，用原生异步 completion handler 直接通知。

### 6.4 WASM (HTML5 Video)

WASM 的 `Load()` 已经是异步的（`<video>` 元素异步加载），`AsyncLoad()` 直接转发：

```cpp
#ifdef __EMSCRIPTEN__
void VideoPlayer::AsyncLoad(const String& source, int width, int height,
                            const AsyncLoadCallback& callback)
{
    asyncLoadCallback_ = callback;

    // WASM Load 本身不阻塞，直接调用
    bool result = Load(source, width, height);
    if (!result)
    {
        if (asyncLoadCallback_)
        {
            asyncLoadCallback_(false);
            asyncLoadCallback_ = nullptr;
        }
        return;
    }

    // 标记为异步加载中（等待 IsReady 变 true 时触发回调）
    asyncLoading_ = true;
}
#endif
```

WASM Update 中检测就绪并触发回调：

```cpp
// WASM Update() 中新增
if (asyncLoading_ && IsReady())
{
    asyncLoading_ = false;
    if (asyncLoadCallback_)
    {
        asyncLoadCallback_(true);
        asyncLoadCallback_ = nullptr;
    }
}
```

---

## 七、Lua 回调实现

### tolua++ 绑定

在 `VideoPlayer.pkg` 中新增：

```cpp
void AsyncLoad(const String source, int width = 1920, int height = 1080);
bool IsAsyncLoading() const;
tolua_readonly tolua_property__is_set bool asyncLoading;
```

回调通过**自定义 tolua 绑定**实现（因为 tolua++ 不直接支持函数参数）。

核心思路：Lua 绑定层将 Lua 函数包装为 `AsyncLoadCallback`（`std::function<void(bool)>`），直接传给 C++ 的 `AsyncLoad`。VideoPlayer 不需要知道回调来自 Lua 还是 C++。

```cpp
#define TOLUA_DISABLE_tolua_GraphicsLuaAPI_VideoPlayer_AsyncLoad00
static int tolua_GraphicsLuaAPI_VideoPlayer_AsyncLoad00(lua_State* tolua_S)
{
    VideoPlayer* self = (VideoPlayer*)tolua_tousertype(tolua_S, 1, 0);
    const char* source = tolua_tostring(tolua_S, 2, 0);
    int width = (int)tolua_tonumber(tolua_S, 3, 1920);
    int height = (int)tolua_tonumber(tolua_S, 4, 1080);

    AsyncLoadCallback callback = nullptr;

    // 第 5 个参数是可选的 Lua 回调函数
    if (lua_isfunction(tolua_S, 5))
    {
        // WeakPtr<LuaScript> 跟踪 lua_State 生命周期
        // SharedPtr<LuaFunction> 持有 Lua 函数引用
        WeakPtr<LuaScript> luaScriptWeak(LuaScript::GetFromState(tolua_S));
        SharedPtr<LuaFunction> luaCallback(new LuaFunction(tolua_S, 5));

        callback = [luaScriptWeak, luaCallback](bool success) {
            // lua_State 已销毁，跳过回调
            if (luaScriptWeak.Expired())
                return;
            if (luaCallback && luaCallback->IsValid())
            {
                luaCallback->BeginCall();
                luaCallback->PushBoolean(success);
                luaCallback->EndCall();
            }
        };
    }

    self->AsyncLoad(source, width, height, callback);

    return 0;
}
```

**生命周期保证**：

- `WeakPtr<LuaScript>` — 跟踪 `lua_State` 所属的 `LuaScript` 对象。异步回调触发时，若 `LuaScript` 已析构（`lua_State` 已销毁），`Expired()` 返回 true，安全跳过回调，避免 use-after-free。
- `SharedPtr<LuaFunction>` — 持有 Lua 函数的 registry 引用（`luaL_ref`），防止 Lua GC 回收。回调触发后 `asyncLoadCallback_ = nullptr` → 释放 lambda → 释放 `SharedPtr` → `LuaFunction` 析构时 `luaL_unref` 释放引用。
- 此模式与 `DownloadManager.pkg` 中的异步回调一致。

---

## 八、线程安全分析

| 操作 | 线程 | 线程安全？ | 备注 |
|------|------|-----------|------|
| `ResourceCache::RouteResourceURL` | 主线程 | 不安全 | 必须在 AsyncLoad() 入口处完成 |
| `VideoDecoder::Create()` | 主线程 | 安全 | 纯内存分配，主线程创建可立即检测平台支持 |
| `FFmpegDecoder::Open()` | 工作线程 | 安全 | FFmpeg 内部线程安全 |
| `AndroidDecoder::Open()` | 工作线程 | 需注意 | NDK API 线程安全；JNI 需 attach |
| `IOSDecoder::Open()` | 工作线程 | 安全 | @autoreleasepool + semaphore 在工作线程等待 |
| `texture_->Initialize()` | 主线程 | 必须主线程 | GPU 操作 |
| `SoundSource` 创建 | 主线程 | 必须主线程 | 音频系统操作 |
| `AsyncLoadData::completed` | 跨线程 | volatile | 单写者（工作线程），单读者（主线程） |
| `AsyncLoadData::cancelled` | 跨线程 | volatile | 单写者（主线程），单读者（工作线程） |
| `AsyncLoadData::decoder` | 跨线程 | 安全 | AsyncLoad 中 `decoder_.Reset()` 转移所有权，异步期间仅工作线程持有 SharedPtr，避免 refcount 数据竞争。FinalizeAsyncLoad 接收回 `decoder_` |

---

## 九、状态机

```
                    AsyncLoad()
    IDLE ──────────────────────────► ASYNC_LOADING
     │                                    │
     │ Load()                             │ 工作线程完成
     │ (同步)                             ▼
     │                              ASYNC_COMPLETE
     │                                    │
     │                                    │ FinalizeAsyncLoad() (主线程 Update/Play)
     ▼                                    ▼
   LOADED ◄───────────────────────── LOADED
     │
     │ Play()
     ▼
   PLAYING ──► PAUSED ──► PLAYING
     │
     ▼
   ENDED / STOPPED
```

对应 `IsReady()` 返回值：
- IDLE: false
- ASYNC_LOADING: false
- ASYNC_COMPLETE (未 finalize): false
- LOADED: true
- PLAYING/PAUSED/ENDED: true

---

## 十、边界情况处理

### 10.1 重复调用 AsyncLoad

```lua
player:AsyncLoad("video1.mp4")  -- 开始加载 video1
player:AsyncLoad("video2.mp4")  -- 取消 video1，开始加载 video2
```

实现：`AsyncLoad` 入口调 `CancelAsyncLoad()`，设 `cancelled=true` + 等待前一个任务完成，然后提交新任务。

### 10.2 AsyncLoad 期间调用 Load

```lua
player:AsyncLoad("video1.mp4")
player:Load("video2.mp4")  -- 同步加载 video2，取消异步加载
```

实现：`Load()` 入口增加 `CancelAsyncLoad()` 调用。

### 10.3 AsyncLoad 期间调用 Play

```lua
player:AsyncLoad("video.mp4")
player:Play()  -- 异步加载还没完成
```

实现：`Play()` 检测到正在异步加载，**不阻塞**，设置 `pendingPlay_ = true` 后立即返回。`FinalizeAsyncLoad` 成功后检查 `pendingPlay_` 并自动调 `Play()`。全平台行为一致，不会打破 AsyncLoad 的非阻塞语义。

### 10.4 AsyncLoad 失败

```lua
player:AsyncLoad("https://invalid.url/video.mp4", 0, 0, function(success)
    -- success = false
end)
```

后台 `decoder->Open()` 返回 false → `data->success = false, data->completed = true` → 主线程 `Update()` 检测到失败 → 触发回调 `callback(false)`。

### 10.5 VideoPlayer 析构时仍在异步加载

```lua
local player = VideoPlayer()
player:AsyncLoad("https://...")
player = nil  -- GC 回收
```

析构函数调 `CancelAsyncLoad()` → 设 `cancelled=true` → 释放引用（非阻塞）→ 后台任务通过 `selfRef` 自行清理。

关键安全保证：`AsyncLoadWorkFunction` 是静态函数，只通过 `AsyncLoadData*` 访问数据，**不访问 VideoPlayer 成员**。`selfRef` 保证数据在任务执行期间存活。

### 10.6 WASM AsyncLoad 后直接 Play

```lua
player:AsyncLoad("https://cdn.example.com/video.mp4")
player:Play()  -- WASM 下视频可能还没就绪
```

WASM 的 `Play()` 和 Native 的 `Play()` 是独立函数（`#ifdef __EMSCRIPTEN__` 分开）。WASM 的 `Play()` 直接调用 `<video>.play()`，浏览器自行处理缓冲，不阻塞。Native 的 `Play()` 设 `pendingPlay_` 延迟播放，也不阻塞。全平台行为一致。

---

## 十一、文件改动清单

| 文件 | 改动内容 |
|------|---------|
| `engine/Source/Urho3D/Graphics/VideoPlayer.h` | 新增 `AsyncLoadCallback` 类型别名、`AsyncLoad()`、`IsAsyncLoading()`、`CancelAsyncLoad()`；新增 `AsyncLoadData` 结构体；新增 async 相关成员变量 |
| `engine/Source/Urho3D/Graphics/VideoPlayer.cpp` | 实现 `AsyncLoad()`、`AsyncLoadWorkFunction()`、`FinalizeAsyncLoad()`、`CancelAsyncLoad()`；修改 `Update()`、`Play()`、`Load()`（加 CancelAsyncLoad）、析构函数 |
| `engine/Source/Urho3D/LuaScript/pkgs/Graphics/VideoPlayer.pkg` | 新增 `AsyncLoad`、`IsAsyncLoading` 绑定（含自定义 tolua 实现支持 Lua callback） |

**不需要改动的文件**：
- `VideoDecoder.h` / 各平台 Decoder — 不变，线程管理在 VideoPlayer 层
- `VideoTexture.h/cpp` — 不变
- `VideoDecodeThread.h/cpp` — 不变
- `BackgroundWorkQueue.h` — 不变（直接使用现有 API）

---

## 十二、后续优化（可选）

1. **FFmpeg interrupt_callback**：为 `AVFormatContext` 设置 `interrupt_callback`，在回调中检查 `cancelled` 标志，实现 `Open()` 阻塞期间的可中断退出（当前 `CancelAsyncLoad` 需等待 `Open` 自然完成/超时）。

2. **iOS 原生异步**：改造 `IOSDecoder::Open()` 为真正异步，去掉 semaphore，直接用 AVFoundation 的 completion handler。

3. **预缓冲控制**：`FinalizeAsyncLoad` 中已自动启动 `decodeThread_`。可额外暴露 `SetPrewarmFrameCount(unsigned count)` 控制预缓冲帧数。

4. **并发 AsyncLoad**：一个 VideoPlayer 实例只能加载一个视频。多个视频预热用多个 VideoPlayer 实例，天然并发（共用 BackgroundWorkQueue 线程池）。
